import logging
import logging.handlers
from os import path, makedirs
from src.config import Config

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

class ExcludeModuleFilter(logging.Filter):
    def __init__(self, excluded_module: str, name = ""):
        super().__init__(name)
        self.excluded_module = excluded_module

    def filter(self, record):
        return not record.name.startswith(self.excluded_module)
        

def setup_logging():
    from src.main import LOG_DIR

    # Ensure Log File Exists
    makedirs(path.join(LOG_DIR), exist_ok=True)
    with open(path.join(LOG_DIR, "amalgam.log"), "w") as f:
        f.write("")

    # Define Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Define Filters
    websockets_thread_filter = ExcludeModuleFilter("AsyncWebsocketThread")
    websockets_filter = ExcludeModuleFilter("AsyncWebsocketHandler")
    lmstudio_filter = ExcludeModuleFilter("SyncLMStudioWebsocket")
    comtypes_filter = ExcludeModuleFilter("comtypes")

    # Handle Formatting
    date_format = "%Y-%m-%d %H:%M:%S"

    console_formatter = ConsoleFormatter(
        f"%(levelname)s: {RESET} %(message)s",
        datefmt=date_format
    )

    formatter = logging.Formatter(
        "%(asctime)s: %(name)s - %(levelname)s: %(message)s | %(funcName)s",
        datefmt=date_format
    )

    # Logs in Console
    console_handler = logging.StreamHandler()

    try:
        if Config.get_nested_data(["debug_logs", "console"]):
            console_handler.setLevel(logging.DEBUG)
        else:
            console_handler.setLevel(logging.INFO)
    except AttributeError:
        console_handler.setLevel(logging.INFO)
    
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(comtypes_filter)
    console_handler.addFilter(websockets_filter)
    console_handler.addFilter(websockets_thread_filter)
    console_handler.addFilter(lmstudio_filter)
    root_logger.addHandler(console_handler)
    
    # Logs in Files
    file_handler = logging.handlers.TimedRotatingFileHandler(
        path.join(LOG_DIR, "amalgam.log"),
        when="M",
        interval=30,
        backupCount=6
    )

    try:
        if Config.get_nested_data(["debug_logs", "console"]):
            file_handler.setLevel(logging.DEBUG)
        else:
            file_handler.setLevel(logging.INFO)
    except AttributeError:
        file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(formatter)
    file_handler.addFilter(comtypes_filter)
    file_handler.addFilter(websockets_filter)
    root_logger.addHandler(file_handler)

    root_logger.info("Logger Activated")