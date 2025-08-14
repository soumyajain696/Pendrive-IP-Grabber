#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSettings
from utils.encryption import DriveEncryption
from utils.logger import AccessLogger

class DriveManager(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('company', 'pendrive_protector')
        self.logger = AccessLogger()
        self.encryption = DriveEncryption()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        status_label = QLabel('Current Status:')
        status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(status_label)
        
        self.detection_group = self._create_detection_group()
        layout.addWidget(self.detection_group)
        
        action_buttons = self._create_action_buttons()
        layout.addWidget(action_buttons)
        
        self.setLayout(layout)
        
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Drive Protector')

    def _create_detection_group(self):
        group_box = QGroupBox('Drive Detection')
        layout = QVBoxLayout()
        
        self.detected_drives = QListWidget()
        self.detected_drives.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.detected_drives)
        
        refresh_button = QPushButton('Refresh Drives', self)
        refresh_button.clicked.connect(self.scan_drives)
        layout.addWidget(refresh_button)
        
        group_box.setLayout(layout)
        return group_box
    
    def scan_drives(self):
        # Platform-specific drive scanning logic
        try:
            if sys.platform.startswith('linux'):
                drives = [f'/media/{d}' for d in os.listdir('/media')]
            elif sys.platform == 'darwin':
                drives = sorted(os.listdir('/Volumes'))
            elif sys.platform == 'win32':
                import win32api
                drives = win32api.GetLogicalDriveStrings()
                drives = [drives[i:i+3] for i in range(0, len(drives), 4)]
            else:
                drives = ['Unknown']
                
            self.detected_drives.clear()
            self.detected_drives.addItems(drives)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Drive scan failed: {str(e)}')

        
app = QApplication([])
window = DriveManager()
window.show()
sys.exit(app.exec_())