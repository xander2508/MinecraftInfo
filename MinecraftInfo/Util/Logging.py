import logging


logging.basicConfig(
    level=logging.DEBUG,
    filename="App.log",
    format="%(asctime)s %(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)


def LogError(error: str, file: str, func: str) -> None:
    logger.error(str(file) + " : " + str(func) + " : " + str(error))


def LogInfo(info: str, file: str, func: str) -> None:
    logger.info(str(file) + " : " + str(func) + " : " + str(info))
