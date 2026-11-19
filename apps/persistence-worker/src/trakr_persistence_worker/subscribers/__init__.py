"""Kafka subscribers.

Import handler modules from this package so their `@broker.subscriber` decorators
register when the application starts. Each subscriber should set
`group_id=CONSUMER_GROUP_ID` from `trakr_persistence_worker.broker`.
"""
from trakr_persistence_worker.subscribers import telemetry
