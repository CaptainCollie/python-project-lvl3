import sys

from loguru import logger

logger_ = logger
logger.remove()
logger_.add(sys.stderr, level='ERROR')
