# Transcriber App

## Description

The Transcriber App is a Python application that transcribes audio to text using artificial intelligence. It supports common audio formats like MP3, WAV, and OGG, and performs transcription using the OpenAI API with a refinement based on the Whisper model. The app is easy to use, featuring an intuitive graphical interface built with the Tkinter library.

## Features

- **File Loading**: Supports audio files in MP3, WAV, and OGG formats.
- **Audio Transcription**: Transcribes audio to text using the OpenAI API.
- **Graphical Interface**: User-friendly GUI developed with Tkinter.

## Project Structure

```plaintext
transcriber_app/
├── src/
├──── transcriber.py         # Main script with transcription logic
├──── ui.py                  # Script for the graphical interface (UI)
├── requirements.txt       # Project dependencies
├── Makefile               # Makefile for task automation
└── README.md              # This README file with project information
```

## How It Works

1. **File Selection**: Users select an audio file on their computer using the "Select File" button.
2. **Transcription**: Click "Transcribe" to process the audio, which is sent to the OpenAI API and transcribed to text.
3. **Text Display**: The transcribed text is displayed in the GUI for copying or saving as needed.

## Requirements

- **Python 3.x**: Make sure Python 3 is installed.
- **OpenAI API Key**: The app uses the OpenAI API for transcription. You’ll need a valid API key.

## Setting Up the Environment

To streamline the setup and compilation process for different operating systems, a Makefile has been created. Follow the steps below:

### 1. Creating the Virtual Environment and Installing Dependencies
In the terminal, within the project folder, execute:

```bash
make init
```

This command creates a virtual environment named `venv` and installs all dependencies listed in `requirements.txt`.

### 2. Compiling for Windows
If you’re on a Windows system, use:

```bash
make build-windows
```

This will create a Windows executable in the `dist` folder.

### 3. Compiling for Linux
For Linux, use:

```bash
make build-linux
```

This generates a Linux executable in the `dist` folder.

### 4. Compiling for macOS
For macOS, use:

```bash
make build-mac
```

This will create a macOS executable in the `dist` folder.

### 5. Cleaning Temporary Files
To remove the virtual environment and temporary files created during compilation, use:

```bash
make clean
```

## Cross-Compilation Setup for macOS to Windows
If you want to compile the application for Windows on macOS, use Wine to simulate a Windows environment. Below are the prerequisites and setup steps:

### Install Wine on macOS
```bash
brew install --cask xquartz   # Required by Wine
brew install --cask wine-stable
```

### Install Python in Wine

1. Download the Python installer:
   ```bash
   curl -o python-installer.exe https://www.python.org/ftp/python/3.9.9/python-3.9.9-amd64.exe
   ```

2. Install Python in the Wine environment:
   ```bash
   WINEPREFIX=~/.wine wine python-installer.exe
   ```

### Windows Build Setup

Run the following command in the project root to compile the executable for Windows:

```bash
make build-windows
```

This will produce a `Digitador.exe` executable in the `bin/windows` directory.

## Usage Guide

### Run the Application
Open the generated executable (`Digitador.exe` on Windows, `transcriber-linux` on Linux, or `transcriber-mac` on macOS).

### Select an Audio File
Use the "Select File" button to choose an audio file for transcription.

### Start Transcription
Click "Transcribe" to start processing the audio file. The transcribed text will appear in the text box.

### Copy or Save the Text
The transcribed text can be copied or saved as needed.

## Notes
- **Cross-Compilation**: PyInstaller must be run on the operating system for which you’re generating the executable. For example, use `make compile-windows` on a Windows system to produce a Windows executable. However, you can compile for Windows on macOS using Wine with the instructions above.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
