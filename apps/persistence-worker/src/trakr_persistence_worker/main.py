"""Entrypoint for the persistence worker."""

import asyncio

from trakr_core.logging import setup_logging

from trakr_persistence_worker.app import app


def main() -> None:
    setup_logging()
    asyncio.run(app.run())


if __name__ == "__main__":
    main()
