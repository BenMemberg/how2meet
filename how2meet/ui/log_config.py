import logging
from pathlib import Path


def get_logger(name, console_level=logging.DEBUG, file_level=logging.DEBUG, filename='output.log'):
    # Get the absolute path of the current file
    current_file = Path(__file__).resolve()

    # Get the parent directory of the current file
    parent_dir = current_file.parent

    # Create the output directory path
    output_dir = parent_dir / 'output'

    # Create the output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create the absolute path for the log file
    log_file = output_dir / filename

    # Create a logger for the specified name
    logger = logging.getLogger(name)

    # Set the logger's level to the lowest level you want to log
    logger.setLevel(min(console_level, file_level))

    # Set the level of logging for the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    # Set the level of logging for the file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(file_level)

    # Create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Add formatter to the handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
