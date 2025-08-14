import os
import socket
import logging
from datetime import datetime

class AccessLogger:
    LOG_FILE = 'drive_access.log'
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler(self.LOG_FILE)
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def log_access(self, username, action, drive_path):
        hostname = socket.gethostname()
        msg = f'{username}@{hostname} - {action} - {drive_path}'
        self.logger.info(msg)