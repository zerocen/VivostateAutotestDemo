import logging
import logging.handlers
import os
from utils.data_path_manager import data_path_manager


class Logger:
    logger = logging.getLogger("LOG")

    def __init__(self):
        self.logger.setLevel(logging.DEBUG)

        log_formatter = logging.Formatter("[%(asctime)s]  %(levelname)s  %(filename)s:%(lineno)d:%(funcName)s  -  "
                                          "%(message)s")

        if not os.path.exists(data_path_manager.log_dir):
            os.makedirs(data_path_manager.log_dir)

        file_handler = logging.handlers.RotatingFileHandler(
            f"{data_path_manager.log_dir}/test_log.log", mode="a", backupCount=10, encoding="utf-8")
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(logging.INFO)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)


logger = Logger().logger
