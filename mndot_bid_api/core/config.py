import subprocess

from starlette.config import Config
from starlette.datastructures import Secret

config = Config()

APP_TITLE = config("APP_TITLE", default="MnDOT Bid API").replace('"', "")
APP_VERSION = (
    subprocess.run(["poetry", "version", "--short"], capture_output=True)
    .stdout.decode()
    .strip()
)

API_KEY = config("API_KEY", cast=Secret)
API_KEY_NAME = "Access-Token"

DB_DIR = config("DB_DIR", default="./data")
DB_FILE = config("DB_FILE", default="dev-api.db")
DB_URL = f"sqlite:///{DB_DIR}/{DB_FILE}"

CSV_DIR = config("CSV_DIR", default="./data/csv")
