import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.addHandler(stream_handler)
        root_logger.setLevel(logging.INFO)
