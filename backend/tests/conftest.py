import sys
import platform

# The app imports this module under the bare name `db_connection` (see
# src/server.py and src/repositories/base_repository.py), while the tests
# import it as `src.db_connection`. Import it HERE first, then alias the bare
# name to the same module object — otherwise `sys.modules["src.db_connection"]`
# doesn't exist yet when this (first-loaded) conftest runs, and the alias
# raises KeyError. Sharing a single module object is what lets the integration
# fixtures inject the test DB via `db_module._db = ...`.
import src.db_connection

sys.modules["db_connection"] = src.db_connection

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
