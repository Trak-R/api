"""FastStream application for the persistence worker."""

from faststream import FastStream

from trakr_persistence_worker import subscribers  # noqa: F401
from trakr_persistence_worker.broker import broker

app = FastStream(broker)
