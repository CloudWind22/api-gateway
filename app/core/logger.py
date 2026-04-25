#app/core/logger.py
import logging

def setup_logger():
    logger = logging.getLogger("gateway")

    logger.setLevel(logging.INFO)

    #控制台输出
    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

logger = setup_logger()