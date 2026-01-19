import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def hello_world() -> str:
    logger.info("Executing hello_world function - Live tab verification test")
    return "Hello from Telnyx supervisor orchestration!"


if __name__ == "__main__":
    print(hello_world())
