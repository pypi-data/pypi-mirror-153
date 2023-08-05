import os
import sys
import datetime

from dotenv import load_dotenv
from loguru import logger

# Load variables from .env
load_dotenv()

# DEBUG settings
DEBUG: bool = bool(os.getenv("DEBUG", False))

# Constants
MAX_LICENSE_WAITING_TIME_SEC: int = 60
APPROVE_REQUEST_FREQUENCY: int = 10
HOST: str = os.getenv("HOST")
SERVER_URL: str = f"http://{HOST}/scripts"
LICENSE_CHECK_URL: str = SERVER_URL + '/licenses/checklicense'
LICENSE_APPROVE_URL: str = SERVER_URL + '/licenses/licenseapprove'
WORK_URL: str = SERVER_URL + '/products/secondary'
LICENSE_FILE_NAME: str = os.getenv("LICENSE_PATH")

#  ********** LOGGER CONFIG ********************************
PATH = os.getcwd()
if not os.path.exists('logs'):
    os.mkdir("logs")
today = datetime.datetime.today().strftime("%Y-%m-%d")
file_path = os.path.join(os.path.relpath(PATH, start=None), 'logs', today, 'secondary_client.log')
logger.remove()
LOG_LEVEL: str = "WARNING"
DEBUG_LEVEL: str = "DEBUG" if DEBUG else "INFO"
logger.add(sink=file_path, enqueue=True, level=LOG_LEVEL, rotation="50 MB")
logger.add(sink=sys.stdout, level=DEBUG_LEVEL)
logger.configure(
    levels=[
        dict(name="DEBUG", color="<white>"),
        dict(name="INFO", color="<fg #afffff>"),
        dict(name="WARNING", color="<light-yellow>"),
        dict(name="ERROR", color="<red>"),
    ]
)
#  ********** END OF LOGGER CONFIG *************************
