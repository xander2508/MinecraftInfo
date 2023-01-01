import json
import logging
import os

JSON_LOCATION = (
    os.path.dirname(os.path.abspath(__file__))
    + "/../DataStorage/Configuration/DataSourceLocations.json"
)

with open(JSON_LOCATION) as JsonFile:
    DataSource = json.load(JsonFile)
LogLevel = DataSource["LogLevel"]

if LogLevel == "INFO":
    logging.basicConfig(
        level=logging.INFO,
        filename="App.log",
        format="%(asctime)s %(levelname)s:%(message)s",
    )
elif LogLevel == "DEBUG":
    logging.basicConfig(
        level=logging.DEBUG,
        filename="App.log",
        format="%(asctime)s %(levelname)s:%(message)s",
    )
elif LogLevel == "WARN":
    logging.basicConfig(
        level=logging.WARN,
        filename="App.log",
        format="%(asctime)s %(levelname)s:%(message)s",
    )
elif LogLevel == "ERROR":
    logging.basicConfig(
        level=logging.ERROR,
        filename="App.log",
        format="%(asctime)s %(levelname)s:%(message)s",
    )
elif LogLevel == "CRITICAL":
    logging.basicConfig(
        level=logging.CRITICAL,
        filename="App.log",
        format="%(asctime)s %(levelname)s:%(message)s",
    )

logger = logging.getLogger(__name__)


def LogError(error: str, file: str, func: str) -> None:
    logger.critical(str(file) + " : " + str(func) + " : " + str(error))


def LogInfo(info: str, file: str, func: str) -> None:
    logger.info(str(file) + " : " + str(func) + " : " + str(info))
