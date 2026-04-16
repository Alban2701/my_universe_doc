import asyncio
import platform
import traceback

if platform.system() == "Windows":  # Event Loop for compatibility between Windows and psycopg3
    asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )
import uvicorn
import os
import argparse
from dotenv import load_dotenv
import sys
from pathlib import Path
load_dotenv()
port = int(os.getenv("SERVER_PORT"))

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log-level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)"
    )
    parser.add_argument(
        "--reload", action="store_true", help="Enable auto-reload"
    )
    args = parser.parse_args()
    # available_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
    # if args.log_level.upper() not in available_levels:
    #     print(
    #         f"{args.log_level} not available as a log level. Please set the level to one of those : {available_levels}"
    #     )

    # os.environ["APP_LOG_LEVEL"] = args.log_level.upper()
    config = uvicorn.Config(
    "src.server:app",
    host="0.0.0.0",
    port=port,
    reload=args.reload
    )
    server = uvicorn.Server(config)
    try:
        asyncio.run(server.serve())
    except Exception as e:
        print(traceback.format_exc())
        print("Asking the server to stop, closing...")
    finally:
        print("Server Stopped")
        