import os
import logging
from logging.handlers import RotatingFileHandler


class AppLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        self.logger = logging.getLogger("app")
        self.logger.setLevel(logging.INFO)

        # [2025-10-01 18:45:12,346] [WARNING] [app] - Like that
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s"
        )

        # File
        logs_dir = os.path.join(os.getcwd(), "app", "logs")
        os.makedirs(logs_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            # Max size 5 MB and max 5 old files
            os.path.join(logs_dir, "app.log"),
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setFormatter(formatter)

        # Console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

    def get_logger(self):
        return self.logger
