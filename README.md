# README

## Descrição

Este projeto é um bot para Telegram que permite baixar e enviar vídeos ou áudios de URLs fornecidos. O bot é construído com o uso das bibliotecas `yt_dlp` para baixar a mídia e `python-telegram-bot` para interagir com a API do Telegram. As mensagens são estilizadas com um toque de Hoshimi Miyabi, personagem que adiciona um toque de personalidade ao bot.

## Funcionalidades

- **/start**: Inicia o bot e mostra uma mensagem de boas-vindas.
- **/download [URL] [video]**: Baixa e envia um vídeo do link fornecido.
- **/daudio [URL]**: Baixa e envia apenas o áudio do link fornecido.
- **/help**: Mostra uma mensagem de ajuda com os comandos disponíveis.
- **/commands**: Lista todos os comandos disponíveis.
- Respostas personalizadas para mensagens de saudação.

## Dependências

- `python-telegram-bot`: Biblioteca para criar bots do Telegram.
- `yt-dlp`: Biblioteca para download de vídeos e áudios de URLs.
- `ffmpeg`: Ferramenta para manipulação de áudio e vídeo.

## Configuração

### Windows

1. **Preparar o Ambiente**

   Execute `execute.bat` para instalar as dependências e rodar o bot.

### Linux

1. **Instalar Dependências**

   Primeiro, certifique-se de que o Python e o pip estão instalados. Em seguida, instale as dependências:

   ```sh
   sudo apt-get update
   sudo apt-get install -y python3-pip ffmpeg
   python3 -m pip install --upgrade pip
   python3 -m pip install python-telegram-bot sqlalchemy yt-dlp
   ```

2. **Preparar o Script**

   Salve o código do bot em um arquivo chamado `bot.py`. Para rodar o bot, execute:

   ```sh
   python3 bot.py
   ```

   Certifique-se de que `ffmpeg` está instalado e disponível no PATH.

## Configuração do Token do Telegram

Substitua o token `"seu_token_aqui"` pelo token do seu próprio bot do Telegram. O token pode ser obtido criando um bot através do BotFather no Telegram.

## Considerações Finais

Certifique-se de que o bot tem permissões apropriadas no Telegram e que o ambiente está corretamente configurado para garantir o funcionamento adequado.