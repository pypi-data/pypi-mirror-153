import contextlib
from dataclasses import dataclass, astuple, field as dc_field
from datetime import datetime
from typing import List, Callable, Any, AsyncContextManager, Union

import janus
from google.cloud import firestore
from google.cloud.firestore_v1.watch import DocumentChange, ChangeType
from proto.datetime_helpers import DatetimeWithNanoseconds

_OnSnapshotSpec = Callable[[List[firestore.DocumentSnapshot],
                            List[DocumentChange],
                            DatetimeWithNanoseconds], None]

Watchable = Union[firestore.Query,
                  firestore.DocumentReference,
                  firestore.CollectionReference]


@dataclass(order=True)
class Change:
    """Comparable dataclass for changes that compares using readtime, and avoids using other fields for comparison."""
    readtime: datetime
    change: DocumentChange = dc_field(compare=False)
    snapshot: firestore.DocumentSnapshot = dc_field(compare=False)

    # Add an iterator so that the dataclass can be unpacked like a tuple.
    def __iter__(self):
        return iter(astuple(self))


# a mixed sync-async queue; since Firestore doesn't expose an async interface for its change listeners, we use
# this queue to synchronously add data (on the background thread) and asynchronously get it out
ChangeQueue = janus.AsyncQueue[Change]


@contextlib.asynccontextmanager
async def change_queue(watched: Watchable) -> AsyncContextManager[ChangeQueue]:
    """ Returns an async context manager that wraps an async queue containing the changes for the given watchable. """
    q = janus.PriorityQueue[Change]()

    def callback(docs: List[firestore.DocumentSnapshot],
                 changes: List[DocumentChange],
                 read_time: DatetimeWithNanoseconds):
        for document, change in zip(docs, changes):
            if not q.closed:
                q.sync_q.put(Change(read_time, change, document))

    watcher = watched.on_snapshot(callback)  # start a watch on query using a background thread
    exception = None
    try:
        yield q.async_q
    except Exception as e:
        exception = e
        raise
    finally:
        q.close()
        watcher.close(reason=exception)


async def _changes(watchable: Watchable):
    """ Return an async source that contains the changes for the given watchable """
    async with change_queue(watchable) as q:
        try:
            while True:
                yield await q.get()
                q.task_done()
        except GeneratorExit:
            pass


async def field(watched: Watchable, *field_names: str, error_field: str = 'error') -> Any:
    """
    Return all the fields in field_names from watched or raise a RuntimeError if the 'error' field was set. Fields that
    don't exist in the watchable are simply ignored.
    """
    async for _, change, snapshot in _changes(watched):
        if change.type in {ChangeType.ADDED, ChangeType.MODIFIED}:
            data = snapshot.to_dict()
            if error_field in data:
                raise RuntimeError(data[error_field])
            result = {field_name: data[field_name] for field_name in field_names if field_name in data}
            if result:
                return result
            # probably got called for some other even we were not interested in; start waiting again
