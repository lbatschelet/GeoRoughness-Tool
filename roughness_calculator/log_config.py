import os
import logging


def setup_logging() -> None:
    """
    Sets up the logging for the application.

    This method creates a 'logs' directory if it doesn't exist, sets the log file path, and configures the logger.

    Raises:
        OSError: If there's an error creating the 'logs' directory or setting up the logger.
    """
    try:
        # Define the log directory
        log_directory = os.path.join(os.path.dirname(__file__), 'logs')
        # Create the log directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)
        # Define the log file path
        log_file_path = os.path.join(log_directory, 'app.log')

        # Configure the logger
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                            filename=log_file_path,
                            filemode='w')
        logger = logging.getLogger()
        logger.info("Logger configured and ready to use.")
    except OSError as e:
        # Log the error and raise the original exception
        logging.error("Error setting up the logger: " + str(e))
        raise
