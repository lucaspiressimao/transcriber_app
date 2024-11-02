import os
import sys
from pathlib import Path

if hasattr(sys, '_MEIPASS'):
    # Adiciona o diretório temporário do PyInstaller ao PATH
    os.environ['PATH'] = os.path.join(sys._MEIPASS) + os.pathsep + os.environ['PATH']

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QMessageBox, QProgressDialog, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import json
from transcriber import transcribe_audio

# Local onde o arquivo de configuração será salvo
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
        # Configurações da janela principal
        self.setWindowTitle('Estagiário digitador')
        self.setGeometry(100, 100, 600, 400)

        # Definindo o ícone da janela
        self.setWindowIcon(QIcon('img/icon.ico'))

        layout = QVBoxLayout()

        # Campo para a chave da API
        self.label_api_key = QLabel('Chave da API OpenAI:')
        layout.addWidget(self.label_api_key)

        self.entry_api_key = QLineEdit(self)
        self.entry_api_key.setPlaceholderText('Insira sua chave da API aqui...')
        self.entry_api_key.setText(self.load_api_key())
        layout.addWidget(self.entry_api_key)

        self.save_api_button = QPushButton('Salvar Chave API', self)
        self.save_api_button.clicked.connect(self.save_api_key)
        layout.addWidget(self.save_api_button)

        # Campo para o arquivo de áudio
        self.label_file = QLabel('Arquivo de áudio:')
        layout.addWidget(self.label_file)

        self.entry_file_path = QLineEdit(self)
        self.entry_file_path.setPlaceholderText('Selecione um arquivo de áudio...')
        layout.addWidget(self.entry_file_path)

        self.browse_button = QPushButton('Selecionar Arquivo', self)
        self.browse_button.clicked.connect(self.select_file)
        layout.addWidget(self.browse_button)

        # Checkbox para habilitar/desabilitar o envio para a OpenAI
        self.send_to_openai_checkbox = QCheckBox('Enviar transcrição para a OpenAI', self)
        self.send_to_openai_checkbox.setChecked(True)  # Padrão é habilitado
        layout.addWidget(self.send_to_openai_checkbox)

        # Botão para iniciar a transcrição
        self.transcribe_button = QPushButton('Transcrever', self)
        self.transcribe_button.clicked.connect(self.transcribe_audio)
        layout.addWidget(self.transcribe_button)

        # Caixa de texto para exibir o resultado
        self.text_output = QTextEdit(self)
        self.text_output.setPlaceholderText('A transcrição aparecerá aqui...')
        layout.addWidget(self.text_output)

        self.setLayout(layout)

    def load_api_key(self):
        try:
            if CONFIG_FILE.exists():
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    return config.get("api_key", "")
        except Exception as e:
            print(f"Erro ao carregar a chave da API: {e}")
        return ""

    def save_api_key(self):
        api_key = self.entry_api_key.text()
        if api_key:
            try:
                CONFIG_DIR.mkdir(parents=True, exist_ok=True)
                with open(CONFIG_FILE, "w") as f:
                    json.dump({"api_key": api_key}, f)
                QMessageBox.information(self, "Sucesso", "Chave da API salva com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar a chave da API: {e}")
        else:
            QMessageBox.warning(self, "Aviso", "Por favor, insira uma chave da API válida.")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo de áudio", "", "Audio Files (*.mp3 *.wav *.ogg *.m4a)")
        if file_path:
            self.entry_file_path.setText(file_path)

    def transcribe_audio(self):
        file_path = self.entry_file_path.text()
        api_key = self.entry_api_key.text()
        send_to_openai = self.send_to_openai_checkbox.isChecked()  # Verifica se o envio para a OpenAI está habilitado

        if file_path and (api_key or not send_to_openai):
            # Cria um diálogo de progresso
            self.progress_dialog = QProgressDialog("Processando o áudio...", "Cancelar", 0, 0, self)
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setAutoClose(False)
            self.progress_dialog.setAutoReset(False)
            self.progress_dialog.show()

            # Inicia a thread para transcrição
            self.thread = TranscriberThread(file_path, api_key, send_to_openai)
            self.thread.finished.connect(self.on_transcription_finished)
            self.thread.error.connect(self.on_transcription_error)
            self.thread.start()

        else:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um arquivo de áudio e insira a chave da API.")

    def on_transcription_finished(self, result):
        self.text_output.setPlainText(result)
        self.progress_dialog.close()

    def on_transcription_error(self, error_message):
        QMessageBox.critical(self, "Erro", f"Erro ao transcrever: {error_message}")
        self.progress_dialog.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TranscriberApp()
    ex.show()
    sys.exit(app.exec_())
