import os
from dotenv import load_dotenv

dirname = os.path.abspath(__file__)

try:
    load_dotenv(dotenv_path=os.path.join(dirname, "..", ".env"))
except FileNotFoundError:
    pass

DB_NAME = os.getenv("DB_FILENAME") or "db.sqlite"
DB_PATH = os.path.join((os.path.dirname(dirname)), "data", DB_NAME)
