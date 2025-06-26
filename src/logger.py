import logging
import logging.handlers
from os import path, makedirs

# Logger Console Colours
CYAN = "\033[0;36m"
BLUE = "\033[0;34m"
YELLOW = "\033[0;33m"
RED = "\033[0;31m"
BOLD = "\033[1m"
RESET = "\033[0m"

LOG_COLOURS = {
    logging.DEBUG: CYAN,
    logging.INFO: BLUE,
    logging.WARNING: YELLOW,
    logging.ERROR: RED,
    logging.CRITICAL: BOLD + RED
}

class ConsoleFormatter(logging.Formatter):
    def __init__(self, fmt = None, datefmt = None, style = "%"):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        log_colour = LOG_COLOURS.get(record.levelno, RESET)

        formatted = super().format(record)

        return f"{log_colour}{formatted}{RESET}"

def setup_logging():
    from src.main import LOG_DIR

    # Ensure Log File Exists
    makedirs(path.join(LOG_DIR), exist_ok=True)
    with open(path.join(LOG_DIR, "amalgam.log"), "w") as f:
        f.write("")

    # Define Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Handle Formatting
    date_format = "%Y-%m-%d %H:%M:%S"

    console_formatter = ConsoleFormatter(
        "%(levelname)s: %(message)s",
        datefmt=date_format
    )

    formatter = logging.Formatter(
        "%(asctime)s: %(name)s - %(levelname)s: %(message)s | %(funcName)s",
        datefmt=date_format
    )

    # Logs in Console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    root_logger.addHandler(console_handler)
    
    # Logs in Files
    file_handler = logging.handlers.TimedRotatingFileHandler(
        path.join(LOG_DIR, "amalgam.log"),
        when="midnight",
        interval=1,
        backupCount=7
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)

    root_logger.info("Logger Activated")