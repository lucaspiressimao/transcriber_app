# Nome do ambiente virtual
VENV = venv

# Dependências do projeto
REQUIREMENTS = requirements.txt

# Nome do arquivo principal para compilar
MAIN_SCRIPT = ui.py

# Nome do executável gerado
EXE_NAME = "Digitador"
EXE_NAME_WIN = "Digitador.exe"

# Caminhos de ícones
ICON_PATH = img/icon.png
ICON_SET = img/icon.iconset
ICON_MAC = img/icon.icns
ICON_WIN = img/icon.ico

# Caminhos binários para ffmpeg
FFMPEG_PATH = libs
FFMPEG_PATH_MAC = $(FFMPEG_PATH)/mac
FFMPEG_PATH_WINDOWS = $(FFMPEG_PATH)/windows

# Parâmetros do PyInstaller
PYINSTALLER_FLAGS = --onefile --windowed
PYINSTALLER_FLAGS_WIN = --onefile --noconsole
PYINSTALLER_LIBS_MAC = --add-binary "$(FFMPEG_PATH_MAC)/ffmpeg:." --add-binary "$(FFMPEG_PATH_MAC)/ffprobe:."
PYINSTALLER_LIBS_WINDOWS = --add-binary "$(FFMPEG_PATH_WINDOWS)/ffmpeg.exe:." --add-binary "$(FFMPEG_PATH_WINDOWS)/ffprobe.exe:."
HIDDEN_IMPORT = --hidden-import=PyQt5 --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtCore
BUILD_ICON = --icon=$(ICON_MAC)
BUILD_ICON_WIN = --icon=$(ICON_WIN)
BUILD_NAME = --name $(EXE_NAME)
BUILD_WIN_NAME = --name $(EXE_NAME_WIN)

# Caminho das bibliotecas de Qt no ambiente PyQt5
QT_PATH = "C:\\users\\lucaspiressimao\\AppData\\Local\\Programs\\Python\\Python39\\lib\\site-packages\\PyQt5\\Qt5\\bin"

# Caminhos de saída
DIST_DIR = dist/*
BIN_DIR_WINDOWS = bin/windows/*
BIN_DIR_MAC = bin/mac/*

.PHONY: init venv install install-wine-deps run-local compile-windows compile-linux clear-mac-build generate-mac-icons compile-mac move_compiled_mac build-mac clean build-windows

# Inicializa o ambiente virtual e instala as dependências
init: venv install

# Cria o ambiente virtual
venv:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi

# Instala as dependências dentro do ambiente virtual
install: venv
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	$(VENV)/bin/pip install pyinstaller watchdog

# Instala as dependências no ambiente Wine
install-wine-deps:
	WINEARCH=win64 WINEPREFIX=~/.wine winecfg
	WINEPREFIX=~/.wine wine "/Users/lucaspiressimao/.wine/drive_c/users/lucaspiressimao/AppData/Local/Programs/Python/Python39/python.exe" -m ensurepip
	WINEPREFIX=~/.wine wine "/Users/lucaspiressimao/.wine/drive_c/users/lucaspiressimao/AppData/Local/Programs/Python/Python39/python.exe" -m pip install --upgrade pip
	WINEPREFIX=~/.wine wine "/Users/lucaspiressimao/.wine/drive_c/users/lucaspiressimao/AppData/Local/Programs/Python/Python39/python.exe" -m pip install --upgrade pyinstaller
	WINEPREFIX=~/.wine wine "/Users/lucaspiressimao/.wine/drive_c/users/lucaspiressimao/AppData/Local/Programs/Python/Python39/python.exe" -m pip install -r $(REQUIREMENTS)

# Executa o projeto localmente com monitoramento de alterações
run-local: clean install
	$(VENV)/bin/watchmedo auto-restart --patterns="*.py" --recursive -- $(VENV)/bin/python $(MAIN_SCRIPT)

# Compila para Windows usando Wine no macOS, com coletor total de dependências
compile-windows: install-wine-deps
	WINEPREFIX=~/.wine wine "/Users/lucaspiressimao/.wine/drive_c/users/lucaspiressimao/AppData/Local/Programs/Python/Python39/Scripts/pyinstaller.exe" \
	$(PYINSTALLER_FLAGS_WIN) $(BUILD_ICON_WIN) $(PYINSTALLER_LIBS_WINDOWS) $(BUILD_WIN_NAME) \
	--collect-all PyQt5 --collect-submodules PyQt5 --copy-metadata PyQt5 --recursive-copy-metadata PyQt5 \
	--paths=$(QT_PATH) "$(MAIN_SCRIPT)" $(HIDDEN_IMPORT) --debug all

# Move o executável compilado para a pasta bin/windows
move_compiled_windows:
	mkdir -p bin/windows
	mv $(DIST_DIR) bin/windows/

# Compila para Windows e move o executável
build-windows: compile-windows move_compiled_windows

# Compila para Linux
compile-linux: clean install
	$(VENV)/bin/pyinstaller $(PYINSTALLER_FLAGS) $(BUILD_NAME) $(MAIN_SCRIPT)

# Limpa os ícones e builds do macOS
clear-mac-build:
	rm -rf $(ICON_MAC) $(ICON_SET)/* $(BIN_DIR_MAC)

# Gera os ícones necessários para macOS
generate-mac-icons:
	sips -z 16 16     $(ICON_PATH) --out $(ICON_SET)/icon_16x16.png
	sips -z 32 32     $(ICON_PATH) --out $(ICON_SET)/icon_16x16@2x.png
	sips -z 32 32     $(ICON_PATH) --out $(ICON_SET)/icon_32x32.png
	sips -z 64 64     $(ICON_PATH) --out $(ICON_SET)/icon_32x32@2x.png
	sips -z 128 128   $(ICON_PATH) --out $(ICON_SET)/icon_128x128.png
	sips -z 256 256   $(ICON_PATH) --out $(ICON_SET)/icon_128x128@2x.png
	sips -z 256 256   $(ICON_PATH) --out $(ICON_SET)/icon_256x256.png
	sips -z 512 512   $(ICON_PATH) --out $(ICON_SET)/icon_256x256@2x.png
	sips -z 512 512   $(ICON_PATH) --out $(ICON_SET)/icon_512x512.png
	cp $(ICON_PATH) $(ICON_SET)/icon_512x512@2x.png
	iconutil -c icns $(ICON_SET)

# Compila para macOS
compile-mac: clean clear-mac-build install generate-mac-icons
	$(VENV)/bin/pyinstaller $(PYINSTALLER_FLAGS) $(BUILD_ICON) $(PYINSTALLER_LIBS_MAC) $(BUILD_NAME) $(MAIN_SCRIPT)

# Move o aplicativo compilado para a pasta bin/mac
move_compiled_mac:
	mkdir -p bin/mac
	mv dist/$(EXE_NAME).app bin/mac/

# Compila para macOS, move o aplicativo e limpa os ícones
build-mac: compile-mac move_compiled_mac clear-mac-build

# Limpa os arquivos gerados pelo PyInstaller e ambiente virtual
clean:
	rm -rf $(VENV) build __pycache__ *.spec Dockerfile
	rm -rf $(DIST_DIR) $(BIN_DIR_WINDOWS) $(BIN_DIR_MAC)
