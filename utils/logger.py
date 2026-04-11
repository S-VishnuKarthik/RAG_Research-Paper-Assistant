import logging
import os

def setup_logger(name="rag_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # File handler
        if not os.path.exists("logs"):
            os.makedirs("logs")

        fh = logging.FileHandler("logs/app.log")
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger