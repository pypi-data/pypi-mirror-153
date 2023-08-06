""""Client library for folding proteins using Cradle's implementation of Alphafold.

Example::
    from cradlebio import alphafold

    creds_path = 'path to JSON firebase credentials obtained from https://auth.internal.cradle.bio/'
    fasta_file = 'path to fasta file containing proteins to be folded'
    sequences = await alphafold.predict_async(creds_path, fasta_file)

    for sequence in sequences:
        print(f'PDB file for folded sequence {sequence.name} is {await sequence.pdb()}')
"""
from dataclasses import dataclass
from datetime import datetime
import logging
import os.path
from typing import Dict, List

from Bio import SeqIO
from google.cloud import firestore

from cradlebio import auth
from cradlebio import watch

CRADLE_GCS_BUCKET = 'cradle-bio.appspot.com'
JOBS = 'jobs'  # the name of the subcollection where jobs are stored in Firebase


class MsaException(Exception):
    """Indicator class for a server-side error during Multiple Sequence Alignment (MSA)"""
    pass


class PdbException(Exception):
    """Indicator class for a server-side error during sequence folding"""
    pass


class Sequence:
    """A protein sequence that is being folded by AlphaFold"""

    _doc: firestore.DocumentReference
    job_id: str
    user_id: str
    seq: str
    id: str
    name: str
    _a3m_path: str
    _pdb_path: str

    def __init__(self, document: firestore.DocumentReference):
        # The Firebase document corresponding to the current sequence. This is the document that is being watched
        # in order to determine when the MSA job and the structure prediction jobs are done. The relevant fields are:
        #   a3m: set to the path of the MSA alignment results, after a successful MSA alignment (not set if MSA fails)
        #   a3m_error: an error message indicating why MSA failed (not set if MSA is successful)
        #   pdb: set to the path of the predicted PDB structure, after a successful structure prediction
        #       (not set if structure prediction fails)
        #   pdb_error: an error message indicating why structure prediction failed
        #       (not set if structure prediction is successful)
        self._doc = document
        self._a3m_path = None
        self._pdb_path = None

    def __str__(self) -> str:
        snapshot = self._doc.get()
        return f'Id: {self.id}, {snapshot.to_dict()}'

    @property
    def id(self):
        return self._doc.id

    @property
    def name(self):
        return self._doc.get(['name']).get('name')

    @property
    def seq(self):
        return self._doc.get(['seq']).get('seq')

    @property
    def job_id(self):
        return self._doc.parent.parent.id

    @property
    def user_id(self):
        # the path to a sequence is 'users/<user_id>/jobs/<job_id>/sequences/<sequence_id>'
        return self._doc._path[-5]

    def to_dict(self):
        return self._doc.get().to_dict()

    async def a3m(self) -> str:
        """Wait for the MSA job to finish and return the path to the a3m data."""
        if not self._a3m_path:
            result = await watch.field(self._doc, 'a3m', 'a3m_error')
            if 'a3m' in result:
                self._a3m_path = result['a3m']
            elif 'a3m_error' in result:
                logging.error(f'Error performing MSA for {self.name}: {result["a3m_error"]}')
                raise MsaException(result["a3m_error"])
            else:
                logging.error(f'Unknown error performing MSA for {self.name}: no result provided by server')
                raise MsaException('No result provided by server')
        return self._a3m_path

    async def pdb(self):
        """"Wait for the folding to finish and return a path to the GCS blob that contains the PDB file"""
        # First wait for the MSA (and stop if the MSA resulted in an error)
        if not self._a3m_path:
            await self.a3m()
        if not self._pdb_path:
            pdb_result = await watch.field(self._doc, 'pdbs', 'pdb_path', 'pdb_error')
            if 'pdb_error' in pdb_result:
                logging.error(f'Error folding {self.name}: {pdb_result["pdb_error"]}')
                raise PdbException(pdb_result["pdb_error"])
            self._pdb_path = pdb_result['pdb_path']
            self._pdbs = pdb_result['pdbs']
        return self._pdbs


@dataclass
class Job:
    """A protein-folding job"""
    id: str
    job_data: Dict[str, any]
    sequences: List[Sequence]


def _get_job_id(fasta_file: str):
    """Build and return the job name string for a given fasta file that is being folded."""
    return datetime.today().strftime('%Y-%m-%d-%H:%M:%S_') + os.path.basename(fasta_file)


def parse_fasta(fasta_file: str, db_client: firestore.Client, uid: str,
                job_doc: firestore.DocumentReference):
    """
    Parses the given fasta file and creates a Firebase document for each sequence under
    job_id/sequences/<sequence_name> with status 'PENDING'
    """
    logging.info(f'Parsing and uploading proteins in {fasta_file}')

    # parse the proteins in the FASTA file and write them as a batch to Firestore
    batch: firestore.WriteBatch = db_client.batch()
    fasta_sequences = SeqIO.parse(fasta_file, 'fasta')

    result: List[Sequence] = []
    for i, fasta in enumerate(fasta_sequences):
        # since colabfold_search names sequences in the file starting with 0, we adopt
        # the same convention for convenience
        sequence_id = str(i)
        sequence_doc: firestore.DocumentReference = job_doc.collection('sequences').document(sequence_id)
        batch.create(sequence_doc, {'status': 'PENDING', 'seq': str(fasta.seq), 'name': str(fasta.id)})
        result.append(Sequence(sequence_doc))

        if (i + 1) % 500 == 0:  # a batch supports at most 500 operations
            batch.commit()
            batch = db_client.batch()
    batch.commit()
    logging.info(f'{i} proteins successfully parsed and uploaded for processing.')
    return result


def predict(creds: auth.IdentityPlatformTokenCredentials, fasta_file: str) -> List[Sequence]:
    """
    Returns a list of sequences corresponding to the entries in fasta_file.
    The method synchronously copies the fasta file to GCS and then awaits until the fasta file is parsed
    on the server side before returning a list of Sequence instances corresponding to the entries in the fasta files.
    """
    if not os.path.exists(fasta_file):
        raise FileNotFoundError(f'Could not find FASTA file: {fasta_file}')
    job_id = _get_job_id(fasta_file)
    db_client: firestore.Client = auth.get_client(creds)
    user_document: firestore.DocumentReference = auth.get_user_document(creds)

    # create a new job for the user and a Firestore entry pointing at the FASTA file on GCS;
    # this signals the AFAAS sever to start processing the newly uploaded FASTA file
    job_doc = user_document.collection(JOBS).document(job_id)
    if job_doc.get().exists:
        raise RuntimeError(f'Duplicate session {job_id} when predicting structure for: {fasta_file}')
    if os.path.getsize(fasta_file) > 5e5:
        raise ValueError(f'Input file is too large: {fasta_file}. Max size is 500KB.')

    job_doc.create({'creation_time': {".sv": "timestamp"}})
    result = parse_fasta(fasta_file, db_client, creds.uid, job_doc)

    # only update teh status to PENDING after sequences are parsed, otherwise the server sees no sequences
    job_doc.update({'status': 'PENDING'})
    return result


def get_jobs(creds: auth.IdentityPlatformTokenCredentials) -> List[Job]:
    """Return a list of alphafold jobs for the current user"""
    user_doc = auth.get_user_document(creds)
    # a sub-collection of all jobs for current user (list of documents)
    jobs_collection = user_doc.collection(JOBS)
    jobs: List[Job] = []
    for job in jobs_collection.stream():
        # using job.get('sequences') doesn't work (I assume because listing subcollections is relatively
        # new in the client lib, and it's still buggy). Firebase does "shallow fetching" by default, so sub-collections
        # are not fetched, when the document is created, and they forgot this fact when implementing the get() method
        job_data = job.to_dict()
        # all sequences for current job (list of documents)
        sequences_collection = user_doc.collection(JOBS).document(job.id).collection('sequences')
        sequences = [Sequence(sequence) for sequence in sequences_collection.stream()]
        jobs.append(Job(job.id, job_data, sequences))
    return jobs


def get_job_by_id(creds: auth.IdentityPlatformTokenCredentials, job_id: str) -> Job:
    """Return the job with the given id for the authenticated user"""
    user_doc: firestore.DocumentReference = auth.get_user_document(creds)
    jobs_collection: firestore.CollectionReference = user_doc.collection(JOBS)  # all jobs for current user
    job: firestore.DocumentReference = jobs_collection.document(job_id)
    sequences_collection: firestore.CollectionReference = job.collection('sequences')  # all sequences for current job
    sequences = [Sequence(sequence) for sequence in sequences_collection.stream()]
    return Job(job_id, job.get().to_dict(), sequences)
