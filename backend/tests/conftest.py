import sys
import platform


sys.modules["db_connection"] = sys.modules["src.db_connection"]

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
