import sys
import platform

# Aliase src.db_connection et db_connection vers le MÊME module
# (le code de prod importe sans préfixe, les tests avec — sinon deux _db distincts)
import src.db_connection

sys.modules["db_connection"] = sys.modules["src.db_connection"]

if platform.system() == "Windows":
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
