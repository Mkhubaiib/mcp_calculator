"""Central logging configuration."""
import logging

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

def configure_logging(level: str = "INFO"):
    logging.basicConfig(level=level, format=LOG_FORMAT)
    logging.getLogger("uvicorn").setLevel(level)
