import os
import sys
import logging
import tempfile
from logging.handlers import TimedRotatingFileHandler
import datetime


def get_application_root():
    if getattr(sys, "frozen", False):
        # When running from exe file (packaged with PyInstaller)
        return os.path.dirname(sys.executable)
    else:
        # When running from source code
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


APP_ROOT = get_application_root()

# Create logs directory, handle case of no write permissions
try:
    LOGS_DIR = os.path.join(APP_ROOT, "logs")
    os.makedirs(LOGS_DIR, exist_ok=True)
except PermissionError:
    # Use temp directory if logs directory cannot be created
    LOGS_DIR = tempfile.gettempdir()


class ColoredFormatter(logging.Formatter):
    """Format logs with colors for console"""

    # ANSI color codes
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    # Log level to color mapping
    COLORS = {
        logging.DEBUG: BLUE,
        logging.INFO: WHITE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: MAGENTA + BOLD,
    }

    def format(self, record):
        # Get appropriate color for log level
        levelcolor = self.COLORS.get(record.levelno, self.RESET)

        # Format timestamp
        timestamp = datetime.datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Create colored message with reduced spacing
        colored_message = (
            f"{self.CYAN}{timestamp}{self.RESET} | "
            f"{levelcolor}{record.levelname.ljust(5)}{self.RESET} | "
            f"{self.BOLD}{record.name}{self.RESET} | "
            f"{self.CYAN}{record.funcName}{self.RESET}:{self.CYAN}{record.lineno}{self.RESET} | "
            f"{levelcolor}{record.getMessage()}{self.RESET}"
        )

        return colored_message


class CustomAdapter(logging.LoggerAdapter):
    """Custom adapter to add module_name to log message without overriding 'name'"""

    def process(self, msg, kwargs):
        return msg, kwargs


# Initialize logging handlers
_console_handler = None
_file_handler = None


# Ensure logger is set up before first use
def setup_logger():
    global _console_handler, _file_handler

    # Configure the root logger
    root_logger = logging.getLogger("")
    root_logger.setLevel(logging.DEBUG)

    # Clear existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Format for file output
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-5s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Format with colors for console output
    console_formatter = ColoredFormatter()

    # Add console handler
    _console_handler = logging.StreamHandler(sys.stderr)
    _console_handler.setLevel(logging.INFO)
    _console_handler.setFormatter(console_formatter)
    root_logger.addHandler(_console_handler)

    # Add file handler with rotation
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(LOGS_DIR, f"app_{today}.log")

        _file_handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",  # Create new file at midnight
            interval=1,  # Each day
            backupCount=7,  # Keep logs for 7 days
        )
        _file_handler.setLevel(logging.DEBUG)
        _file_handler.setFormatter(file_formatter)
        root_logger.addHandler(_file_handler)
    except Exception as e:
        # Log error to console and set _file_handler to None explicitly
        print(f"Failed to set up file logging: {str(e)}")
        _file_handler = None

    return root_logger


# Make sure logger is initialized
setup_logger()


def get_logger(name="APP"):
    """Get a logger with the specified name"""
    # Ensure logger is initialized before use
    global _console_handler, _file_handler
    if _console_handler is None:
        setup_logger()

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Remove any existing handlers to prevent duplication
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Add our handlers
    if _console_handler:
        logger.addHandler(_console_handler)

    if _file_handler:
        logger.addHandler(_file_handler)

    # Disable propagation for all loggers
    logger.propagate = False

    return logger
