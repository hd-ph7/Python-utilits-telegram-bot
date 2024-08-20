@echo off
setlocal

REM Nome do arquivo oculto que servirá como flag
set "FLAG_FILE=%~dp0.installed"
set "FFMPEG_INSTALLED_FLAG=%~dp0.ffmpeg_installed"

REM Caminho do arquivo 7z do ffmpeg e diretório de extração
set "FFMPEG_7Z=%~dp0ffmpeg.7z"
set "FFMPEG_INSTALL_DIR=C:\ffmpeg"
set "FFMPEG_BIN_DIR=%FFMPEG_INSTALL_DIR%\bin"
set "SEVEN_ZIP_EXE=%~dp07zr.exe"

REM Verifica se o ffmpeg está instalado
if exist "%FFMPEG_INSTALLED_FLAG%" (
    echo ffmpeg já está instalado.
) else (
    echo Verificando se o ffmpeg está instalado...
    where ffmpeg >nul 2>&1
    if %errorlevel% neq 0 (
        echo ffmpeg não encontrado. Instalando o ffmpeg...

        REM Verifica se o diretório de instalação do ffmpeg já existe
        if not exist "%FFMPEG_INSTALL_DIR%" (
            echo Extraindo ffmpeg para %FFMPEG_INSTALL_DIR%...
            REM Usa 7zr.exe para extrair o arquivo .7z
            "%SEVEN_ZIP_EXE%" x "%FFMPEG_7Z%" -o"%FFMPEG_INSTALL_DIR%" -y
        )

        REM Adiciona ffmpeg ao PATH permanentemente
        setx PATH "%PATH%;%FFMPEG_BIN_DIR%"
        echo ffmpeg instalado e adicionado ao PATH.
        echo Instalacao do ffmpeg concluida. > "%FFMPEG_INSTALLED_FLAG%"
    ) else (
        echo ffmpeg já está instalado.
        echo Instalacao do ffmpeg concluida. > "%FFMPEG_INSTALLED_FLAG%"
    )
)

REM Verifica se o pip está disponível
echo Verificando se o pip está disponível...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Pip não encontrado. Certifique-se de que o Python está instalado corretamente.
    pause
    exit /b
)

REM Verifica se as bibliotecas Python já foram instaladas
if exist "%FLAG_FILE%" (
    echo Bibliotecas Python já instaladas.
) else (
    echo Verificando bibliotecas Python...
    echo Instalando as bibliotecas necessárias...
    python -m pip install --upgrade pip
    python -m pip install python-telegram-bot sqlalchemy yt-dlp

    REM Cria um arquivo oculto para marcar que as bibliotecas foram instaladas
    echo. > "%FLAG_FILE%"
    echo Bibliotecas Python instaladas com sucesso.
)

REM Executa o script Python
echo Executando o script Python...
python bot.py

REM Pausa para exibir qualquer mensagem de erro ou saída do script
pause
