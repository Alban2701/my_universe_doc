import sys
import platform

import src.db_connection

sys.modules["db_connection"] = sys.modules["src.db_connection"]

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
