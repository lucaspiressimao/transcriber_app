# Virtual environment name
VENV = venv

# Project dependencies
REQUIREMENTS = requirements.txt

# Main script to compile
MAIN_SCRIPT = src/ui.py

# Generated executable name
EXE_NAME = "Digitador"
EXE_NAME_WIN = "Digitador.exe"

# Icon paths
ICON_PATH = img/icon.png
ICON_SET = img/icon.iconset
ICON_MAC = img/icon.icns
ICON_WIN = img/icon.ico

# Binary paths for ffmpeg
FFMPEG_PATH = libs
FFMPEG_PATH_MAC = $(FFMPEG_PATH)/mac
FFMPEG_PATH_WINDOWS = $(FFMPEG_PATH)/windows

# PyInstaller parameters
PYINSTALLER_FLAGS = --onefile --windowed
PYINSTALLER_FLAGS_WIN = --onefile --noconsole
PYINSTALLER_LIBS_MAC = --add-binary "$(FFMPEG_PATH_MAC)/ffmpeg:." --add-binary "$(FFMPEG_PATH_MAC)/ffprobe:."
PYINSTALLER_LIBS_WINDOWS = --add-binary "$(FFMPEG_PATH_WINDOWS)/ffmpeg.exe:." --add-binary "$(FFMPEG_PATH_WINDOWS)/ffprobe.exe:."
HIDDEN_IMPORT = --hidden-import=PyQt5 --hidden-import=PyQt5.QtWidgets --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtCore
BUILD_ICON = --icon=$(ICON_MAC)
BUILD_ICON_WIN = --icon=$(ICON_WIN)
BUILD_NAME = --name $(EXE_NAME)
BUILD_WIN_NAME = --name $(EXE_NAME_WIN)

# Output paths
DIST_DIR = dist/*
BIN_DIR_WINDOWS = bin/windows/*
BIN_DIR_MAC = bin/mac/*

WINE_PYTHON_PATH := $(shell find ~/.wine/drive_c/users -name "python.exe" | head -n 1)
WINE_PYTHONINSTALLER_PATH := $(shell find ~/.wine/drive_c/users -name "pyinstaller.exe" | head -n 1)

.PHONY: init venv install install-wine-deps run-local compile-windows compile-linux clear-mac-build generate-mac-icons compile-mac move_compiled_mac build-mac clean build-windows

# Initialize virtual environment and install dependencies
init: venv install

# Create virtual environment
venv:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi

# Install dependencies in virtual environment
install: venv
	$(VENV)/bin/pip install -r $(REQUIREMENTS)
	$(VENV)/bin/pip install pyinstaller watchdog

# Install dependencies in Wine environment
install-wine-deps:
	WINEARCH=win64 WINEPREFIX=~/.wine winecfg
	WINEPREFIX=~/.wine wine "$(WINE_PYTHON_PATH)" -m ensurepip
	WINEPREFIX=~/.wine wine "$(WINE_PYTHON_PATH)" -m pip install --upgrade pip
	WINEPREFIX=~/.wine wine "$(WINE_PYTHON_PATH)" -m pip install --upgrade pyinstaller
	WINEPREFIX=~/.wine wine "$(WINE_PYTHON_PATH)" -m pip install -r $(REQUIREMENTS)

# Run project locally with file change monitoring
run-local: clean install
	$(VENV)/bin/watchmedo auto-restart --patterns="*.py" --recursive -- $(VENV)/bin/python $(MAIN_SCRIPT)

# Compile for Windows using Wine on macOS, adding --collect-all to include full PyQt5
compile-windows: install-wine-deps
	WINEPREFIX=~/.wine wine $(WINE_PYTHONINSTALLER_PATH) $(PYINSTALLER_FLAGS_WIN) $(BUILD_ICON_WIN) $(PYINSTALLER_LIBS_WINDOWS) $(BUILD_WIN_NAME) --collect-all PyQt5 --collect-binaries PyQt5.Qt5 "$(MAIN_SCRIPT)" $(HIDDEN_IMPORT)

# Move compiled executable to bin/windows
move_compiled_windows:
	mkdir -p bin/windows
	mv $(DIST_DIR) bin/windows/

# Compile for Windows and move executable
build-windows: compile-windows move_compiled_windows

# Compile for Linux
compile-linux: clean install
	$(VENV)/bin/pyinstaller $(PYINSTALLER_FLAGS) $(BUILD_NAME) $(MAIN_SCRIPT)

# Clear icons and macOS builds
clear-mac-build:
	rm -rf $(ICON_MAC) $(ICON_SET)/* $(BIN_DIR_MAC)

# Generate necessary icons for macOS
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

# Compile for macOS
compile-mac: clean clear-mac-build install generate-mac-icons
	$(VENV)/bin/pyinstaller $(PYINSTALLER_FLAGS) $(BUILD_ICON) $(PYINSTALLER_LIBS_MAC) $(BUILD_NAME) $(MAIN_SCRIPT)

# Move compiled application to bin/mac
move_compiled_mac:
	mkdir -p bin/mac
	mv dist/$(EXE_NAME).app bin/mac/

# Compile for macOS, move application, and clear icons
build-mac: compile-mac move_compiled_mac clear-mac-build

# Clean up PyInstaller and virtual environment generated files
clean:
	rm -rf $(VENV) build __pycache__ *.spec Dockerfile
	rm -rf $(DIST_DIR) $(BIN_DIR_WINDOWS) $(BIN_DIR_MAC)
