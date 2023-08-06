import logging

from .file_logger import file_logging_handler
from .stash_logger import stash_logging_handler


def init_logging(app):
    # handler = stash_logging_handler(app)
    handler = file_logging_handler(app)
    root_logger = logging.getLogger("lnsirr_admin")
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
