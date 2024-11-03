import os
import sys
from pathlib import Path

if hasattr(sys, '_MEIPASS'):
    # Adds the PyInstaller temp directory to PATH
    os.environ['PATH'] = os.path.join(sys._MEIPASS) + os.pathsep + os.environ['PATH']

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSplashScreen, QTextEdit, QProgressDialog, QCheckBox, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import json
from transcriber import transcribe_audio

# Location where the config file will be saved
CONFIG_DIR = Path.home() / ".transcriber_app"
CONFIG_FILE = CONFIG_DIR / "config.json"

class TranscriberThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, file_path, api_key, send_to_openai):
        super().__init__()
        self.file_path = file_path
        self.api_key = api_key
        self.send_to_openai = send_to_openai

    def run(self):
        try:
            result = transcribe_audio(self.file_path, self.api_key, self.send_to_openai)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class TranscriberApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main window settings
        self.setWindowTitle('Transcriber')
        self.setGeometry(100, 100, 600, 400)

        # Set window icon
        self.setWindowIcon(QIcon('img/icon.ico'))

        layout = QVBoxLayout()

        # API key field
        self.label_api_key = QLabel('OpenAI API Key:')
        layout.addWidget(self.label_api_key)

        self.entry_api_key = QLineEdit(self)
        self.entry_api_key.setPlaceholderText('Enter your API key here...')
        self.entry_api_key.setText(self.load_api_key())
        layout.addWidget(self.entry_api_key)

        self.save_api_button = QPushButton('Save API Key', self)
        self.save_api_button.clicked.connect(self.save_api_key)
        layout.addWidget(self.save_api_button)

        # Audio file field
        self.label_file = QLabel('Audio File:')
        layout.addWidget(self.label_file)

        self.entry_file_path = QLineEdit(self)
        self.entry_file_path.setPlaceholderText('Select an audio file...')
        layout.addWidget(self.entry_file_path)

        self.browse_button = QPushButton('Select File', self)
        self.browse_button.clicked.connect(self.select_file)
        layout.addWidget(self.browse_button)

        # Checkbox to enable/disable sending to OpenAI
        self.send_to_openai_checkbox = QCheckBox('Send transcription to OpenAI', self)
        self.send_to_openai_checkbox.setChecked(True)  # Default is enabled
        layout.addWidget(self.send_to_openai_checkbox)

        # Button to start transcription
        self.transcribe_button = QPushButton('Transcribe', self)
        self.transcribe_button.clicked.connect(self.transcribe_audio)
        layout.addWidget(self.transcribe_button)

        # Text box to display the result
        self.text_output = QTextEdit(self)
        self.text_output.setPlaceholderText('The transcription will appear here...')
        layout.addWidget(self.text_output)

        self.setLayout(layout)

    def load_api_key(self):
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    return config.get("api_key", "")
        except Exception as e:
            print(f"Error loading API key: {e}")
        return ""

    def save_api_key(self):
        api_key = self.entry_api_key.text()
        if api_key:
            try:
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                with open(CONFIG_FILE, "w") as f:
                    json.dump({"api_key": api_key}, f)
                QMessageBox.information(self, "Success", "API key saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error saving API key: {e}")
        else:
            QMessageBox.warning(self, "Warning", "Please enter a valid API key.")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an audio file", "", "Audio Files (*.mp3 *.wav *.ogg *.m4a)")
        if file_path:
            self.entry_file_path.setText(file_path)

    def transcribe_audio(self):
        file_path = self.entry_file_path.text()
        api_key = self.entry_api_key.text()
        send_to_openai = self.send_to_openai_checkbox.isChecked()  # Check if sending to OpenAI is enabled

        if file_path and (api_key or not send_to_openai):
            # Create a progress dialog
            self.progress_dialog = QProgressDialog("Processing audio...", "Cancel", 0, 0, self)
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setAutoClose(False)
            self.progress_dialog.setAutoReset(False)
            self.progress_dialog.show()

            # Start transcription thread
            self.thread = TranscriberThread(file_path, api_key, send_to_openai)
            self.thread.finished.connect(self.on_transcription_finished)
            self.thread.error.connect(self.on_transcription_error)
            self.thread.start()

        else:
            QMessageBox.warning(self, "Warning", "Please select an audio file and enter the API key.")

    def on_transcription_finished(self, result):
        self.text_output.setPlainText(result)
        self.progress_dialog.close()

    def on_transcription_error(self, error_message):
        QMessageBox.critical(self, "Error", f"Error transcribing: {error_message}")
        self.progress_dialog.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Load splash screen image
    splash_pix = QPixmap('img/icon.png')  # image for the splash screen
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()

    # Update text on splash screen
    splash.showMessage("Loading application...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)

    ex = TranscriberApp()
    ex.show()

    # Close the splash screen
    splash.finish(ex)

    sys.exit(app.exec_())
