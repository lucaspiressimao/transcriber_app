Transcriber App

Descrição

O Transcriber App é um aplicativo desenvolvido em Python que permite transcrever áudios para texto utilizando inteligência artificial. Ele suporta arquivos de áudio em formatos comuns, como MP3, WAV e OGG, e realiza a transcrição utilizando a API da OpenAI, com um refinamento baseado no modelo Whisper. O aplicativo é simples de usar, com uma interface gráfica intuitiva construída com a biblioteca Tkinter.

Funcionalidades

Carregamento de Arquivos: Suporte para arquivos de áudio nos formatos MP3, WAV e OGG.
Transcrição de Áudio: Transcreve áudio para texto usando a API da OpenAI.
Interface Gráfica: Interface amigável e fácil de usar, desenvolvida com Tkinter.
Estrutura do Projeto

transcriber_app/

transcriber.py: Script principal com a lógica de transcrição
ui.py: Script para a interface gráfica (UI)
requirements.txt: Lista de dependências do projeto
Makefile: Arquivo Makefile para automação de tarefas
README.md: Este arquivo README com informações sobre o projeto
Como Funciona

Seleção de Arquivo: O usuário seleciona um arquivo de áudio no seu computador utilizando o botão "Selecionar Arquivo".
Transcrição: O usuário clica em "Transcrever", e o aplicativo processa o áudio, enviando-o para a API da OpenAI, onde é transcrito para texto.
Exibição do Texto: O texto transcrito é exibido na interface gráfica, onde pode ser copiado ou salvo conforme necessário.
Requisitos

Python 3.x: Certifique-se de que o Python 3 esteja instalado.
API Key da OpenAI: O aplicativo usa a API da OpenAI para transcrição. Você precisará de uma chave de API válida.
Como Configurar o Ambiente

Para facilitar o processo de configuração do ambiente e compilação do aplicativo para diferentes sistemas operacionais, foi criado um Makefile. Siga os passos abaixo:

Criar o ambiente virtual e instalar dependências:
No terminal, dentro da pasta do projeto, execute:

csharp
Copy code
make init
Este comando cria um ambiente virtual chamado venv e instala todas as dependências listadas no arquivo requirements.txt.
Compilar para Windows:
Se você estiver em um sistema Windows, use o comando:

go
Copy code
make compile-windows
Isso gerará um executável para Windows na pasta dist.
Compilar para Linux:
Se você estiver em um sistema Linux, use o comando:

go
Copy code
make compile-linux
Isso gerará um executável para Linux na pasta dist.
Compilar para macOS:
Se você estiver em um sistema macOS, use o comando:

go
Copy code
make compile-mac
Isso gerará um executável para macOS na pasta dist.
Limpar arquivos temporários:
Para remover o ambiente virtual e os arquivos temporários gerados durante a compilação, use:

go
Copy code
make clean
Tutorial de Compilação e Uso

Compilação
Windows: Execute make compile-windows em um sistema Windows.
Linux: Execute make compile-linux em um sistema Linux.
macOS: Execute make compile-mac em um sistema macOS.
Cada comando gerará um executável na pasta dist, correspondente ao sistema operacional utilizado.

Uso do Aplicativo
Abra o aplicativo: Clique no executável gerado (transcriber-windows.exe, transcriber-linux, transcriber-mac) para abrir o aplicativo.
Selecione o arquivo de áudio: Use o botão "Selecionar Arquivo" para escolher um arquivo de áudio que deseja transcrever.
Transcreva o áudio: Após selecionar o arquivo, clique em "Transcrever" para iniciar a transcrição. O texto transcrito será exibido na caixa de texto.
Copie ou salve o texto: O texto transcrito pode ser copiado da caixa de texto para ser utilizado conforme necessário.
Considerações

Compilação Cruzada: O PyInstaller deve ser executado no sistema operacional correspondente ao destino. Ou seja, para gerar um executável para Windows, você deve executar o make compile-windows em um sistema Windows. O mesmo vale para Linux e macOS.
API Key: Substitua "SUA_CHAVE_API" no arquivo transcriber.py pela sua chave de API da OpenAI antes de executar o aplicativo.
Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

brew install --cask xquartz   # Requerido para o Wine
brew install --cask wine-stable
curl -o python-installer.exe https://www.python.org/ftp/python/3.9.9/python-3.9.9-amd64.exe
WINEPREFIX=~/.wine wine python-installer.exe