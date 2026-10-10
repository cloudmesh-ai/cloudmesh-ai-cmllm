import logging
import sys

def setup_logging(debug: bool = False):
    """Configures the global logging system for CMLLM."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

def get_logger(name: str):
    """Returns a logger instance for the given name."""
    return logging.getLogger(name)
