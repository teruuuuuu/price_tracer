import os
import logging


LOG_DIR = os.environ.get("LOG_DIR", "./")
LOG_FILENAME = os.path.join(LOG_DIR, 'app.log')
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILENAME)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(stream_handler)
