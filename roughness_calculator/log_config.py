import os
import logging

def setup_logging():
    log_directory = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_directory, exist_ok=True)
    log_file_path = os.path.join(log_directory, 'app.log')

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                        filename=log_file_path,
                        filemode='w')
    logger = logging.getLogger()
    logger.info("Logger configured and ready to use.")

setup_logging()
