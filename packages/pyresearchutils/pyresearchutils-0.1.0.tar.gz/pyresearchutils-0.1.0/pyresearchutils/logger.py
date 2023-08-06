# TODO:build logger

import logging
import os
from datetime import datetime
from os import path
from pathlib import Path

LOGGER_NAME = 'Research'
COLOR_SEQ = "\033[1;%dm"
RESET_SEQ = "\033[0m"
BOLD_SEQ = "\033[1m"

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class Logger:
    # Logger has levels of verbosity.
    log_level_translate = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    LOG_PATH = None
    LOG_FILE = None
    CONSOLE = None

    @staticmethod
    def __check_path_create_dir(log_path: str):
        """
        Create a path if not exist. Otherwise, do nothing.
        Args:
            log_path: Path to create or verify that exists.

        """

        if not path.exists(log_path):
            Path(log_path).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def set_logger_level(log_level=logging.INFO):
        """
        Set log level to determine the logger verbosity.
        Args:
            log_level: Level of verbosity to set for the logger.

        """

        logger = Logger.get_logger()
        logger.setLevel(log_level)
        if Logger.CONSOLE is not None:
            Logger.CONSOLE.setLevel(log_level)

    @staticmethod
    def get_logger():
        """
        Returns: An instance of the logger.
        """
        return logging.getLogger(LOGGER_NAME)

    @staticmethod
    def set_log_file(log_folder: str = None):
        """
        Setting the logger log file path. The method gets the folder for the log file.
        In that folder, it creates a log file according to the timestamp.
        Args:
            log_folder: Folder path to hold the log file.

        """

        logger = Logger.get_logger()

        ts = datetime.now(tz=None).strftime("%d%m%Y_%H%M%S")

        FORMAT = "[%(asctime)s][$BOLD%(name)-20s$RESET][%(levelname)-18s]  %(message)s ($BOLD%(filename)s$RESET:%(lineno)d)"
        COLOR_FORMAT = formatter_message(FORMAT, True)
        formatter = ColoredFormatter(COLOR_FORMAT)

        text_formatter = logging.Formatter(
            '[%(asctime)s][%(name)-20s][%(levelname)-18s]  %(message)s (%(filename)s:%(lineno)d)')

        Logger.LOG_PATH = os.path.join(log_folder)
        log_name = os.path.join(Logger.LOG_PATH, f'research_logs_{ts}.log')

        Logger.__check_path_create_dir(Logger.LOG_PATH)

        fh = logging.FileHandler(log_name)
        fh.setLevel(logging.NOTSET)
        fh.setFormatter(text_formatter)
        logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        Logger.LOG_FILE = log_name
        Logger.CONSOLE = ch


def set_log_folder(folder: str, level: int = logging.INFO):
    """
    Set a directory path for saving a log file.

    Args:
        folder: Folder path to save the log file.
        level: Level of verbosity to set to the logger.

    """
    Logger.set_log_file(folder)
    Logger.set_logger_level(level)


def get_log_file():
    return Logger.LOG_FILE


def check_logger_path():
    if get_log_file() is None:
        logger_path = os.getcwd()
        set_log_folder(logger_path)
        warning(f"Logger is set automatically to {logger_path}")


########################################
# Delegating methods to wrapped logger
########################################
def critical(msg: str):
    """
    Log a message at 'critical' severity and raise an exception.
    Args:
        msg: Message to log.

    """
    check_logger_path()
    Logger.get_logger().critical(msg)
    raise Exception(msg)


def exception(msg: str):
    """
    Log a message at 'exception' severity and raise an exception.
    Args:
        msg: Message to log.

    """
    check_logger_path()
    Logger.get_logger().exception(msg)
    raise Exception(msg)


def debug(msg: str):
    """
    Log a message at 'debug' severity.

    Args:
        msg: Message to log.

    """
    check_logger_path()
    Logger.get_logger().debug(msg)


def info(msg: str):
    """
    Log a message at 'info' severity.

    Args:
        msg: Message to log.

    """
    check_logger_path()
    Logger.get_logger().info(msg)


def print(msg: str):
    check_logger_path()
    info(msg)


def warning(msg: str):
    """
    Log a message at 'warning' severity.

    Args:
        msg: Message to log.

    """
    check_logger_path()
    Logger.get_logger().warning(msg)


def error(msg: str):
    """
    Log a message at 'error' severity and raise an exception.

    Args:
        msg: Message to log.

    """
    check_logger_path()
    Logger.get_logger().error(msg)
    raise Exception(msg)
