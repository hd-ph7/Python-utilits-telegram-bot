import random
import yt_dlp
import logging
import os
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuração básica de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Lista de mensagens com o toque de Hoshimi Miyabi
miyabi_messages = {
    'download_started': [
        "🔪 A missão de download começou! Com a precisão de uma espadachin e a determinação de uma líder, vamos garantir o sucesso!",
        "🌟 O download está em andamento! Com minhas habilidades de artes marciais, vou lutar contra qualquer erro!",
        "🎯 Iniciando o download com a seriedade de uma chefe de Seção 6! Nada vai parar nosso progresso!",
    ],
    'download_completed': [
        "🎉 A missão está completa! O download foi concluído com o êxito esperado de uma espadachin dedicada!",
        "🌸 O download foi bem-sucedido! Assim como protejo New Eridu, garanti que seu arquivo chegasse a salvo!",
        "🚀 Download finalizado! Como chefe da Seção 6, sempre cumpro minhas promessas com eficiência!",
    ],
    'download_error': [
        "⚔️ Houve um erro no download. Como uma líder, vou enfrentar esse desafio com coragem e resolver a situação!",
        "😿 O download falhou. Vou afiar minha espada e tentar novamente para garantir o sucesso da missão!",
        "💔 O download não teve sucesso. Mas não se preocupe, com minha determinação, vamos superar isso!",
    ],
    'upload_started': [
        "🚀 Iniciando o upload com a precisão de uma espadachin! Vou assegurar que seu arquivo seja enviado com segurança!",
        "📤 O upload está em andamento! Com a responsabilidade de uma líder, vou garantir que tudo corra bem!",
        "🎬 O upload está começando! Assim como protejo a cidade, vou proteger o processo de envio do seu arquivo!",
    ],
    'upload_completed': [
        "🎉 O upload foi um sucesso! Assim como construí um sistema inquebrável para New Eridu, garanti que seu arquivo chegasse!",
        "🌟 O upload foi concluído! Com minha determinação, assegurei que o arquivo chegasse intacto e seguro!",
        "✅ Upload finalizado com sucesso! Estou sempre pronta para enfrentar a próxima missão, se precisar de mim novamente!",
    ],
    'upload_error': [
        "⚔️ Enfrentamos um problema ao enviar o arquivo. Vou enfrentar isso com toda a minha determinação e resolver!",
        "😿 O upload falhou. Como uma chefe de Seção 6, vou enfrentar esse desafio e garantir que a missão seja cumprida!",
        "💔 O upload não teve sucesso. Vou me esforçar para superar esse obstáculo e completar a tarefa!",
    ],
    'greeting': [
        "🌞 Bom dia! Assim como protejo a cidade, estou aqui para garantir que sua jornada seja excelente!",
        "🌙 Boa noite! Que seus sonhos sejam tão fortes quanto minha determinação para defender a ordem!",
    ],
}

# Função para obter uma mensagem com o toque de Hoshimi Miyabi
def get_miyabi_message(event_type: str) -> str:
    return random.choice(miyabi_messages.get(event_type, ["Algo aconteceu, mas não sei o que!"]))

# Função para baixar e enviar mídia
async def download_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = context.args[0] if context.args else None
    media_type = context.args[1] if len(context.args) > 1 else 'video'
    user_id = update.message.from_user.id

    if not url:
        await update.message.reply_text("Por favor, forneça um link válido. Não temos uma bola de cristal aqui.")
        logger.warning(f"Usuário {user_id} forneceu um link inválido.")
        return

    # Define a pasta de download e o nome do arquivo com base no ID do usuário
    file_dir = 'downloads'
    os.makedirs(file_dir, exist_ok=True)
    file_name = f"{user_id}_{context.args[0].split('/')[-1]}"
    file_path = os.path.join(file_dir, file_name)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if media_type == 'video' else 'bestaudio/best',
        'outtmpl': file_path,
    }

    try:
        logger.info(f"Usuário {user_id} iniciou o download de mídia: {url}.")
        await update.message.reply_text(get_miyabi_message('download_started'))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        await update.message.reply_text(get_miyabi_message('download_completed'))
        logger.info(f"Download de {url} concluído com sucesso. Enviando arquivo para o usuário {user_id}.")

        with open(file_path, 'rb') as file:
            if media_type == 'video':
                await update.message.reply_video(video=InputFile(file, filename=file_name))
            else:
                await update.message.reply_audio(audio=InputFile(file, filename=file_name))
    
    except Exception as e:
        logger.error(f"Erro ao baixar a mídia do link {url} para o usuário {user_id}: {e}")
        await update.message.reply_text(get_miyabi_message('download_error'))
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Arquivo {file_path} removido após o envio.")

# Função para baixar e enviar apenas áudio
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = context.args[0] if context.args else None
    user_id = update.message.from_user.id

    if not url:
        await update.message.reply_text("Por favor, forneça um link válido. Não temos uma bola de cristal aqui.")
        logger.warning(f"Usuário {user_id} forneceu um link inválido.")
        return

    # Define a pasta de download e o nome do arquivo com base no ID do usuário
    file_dir = 'downloads'
    os.makedirs(file_dir, exist_ok=True)
    file_name = f"{user_id}_{context.args[0].split('/')[-1]}"
    file_path = os.path.join(file_dir, file_name)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
    }

    try:
        logger.info(f"Usuário {user_id} iniciou o download de áudio: {url}.")
        await update.message.reply_text(get_miyabi_message('download_started'))
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        await update.message.reply_text(get_miyabi_message('download_completed'))
        logger.info(f"Download de áudio de {url} concluído com sucesso. Enviando arquivo para o usuário {user_id}.")

        with open(file_path, 'rb') as file:
            await update.message.reply_audio(audio=InputFile(file, filename=file_name))
    
    except Exception as e:
        logger.error(f"Erro ao baixar o áudio do link {url} para o usuário {user_id}: {e}")
        await update.message.reply_text(get_miyabi_message('download_error'))
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Arquivo {file_path} removido após o envio.")

# Comando de início
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'Bem-vindo! Use /download [URL] [video/audio] para baixar e enviar um vídeo ou áudio do link fornecido. Estou aqui para garantir que a missão seja um sucesso, assim como defendo a cidade!'
    )
    logger.info(f"Usuário {update.message.from_user.id} iniciou o bot.")

# Comando de ajuda
async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "/start - Inicia o bot e mostra uma mensagem de boas-vindas com o toque de uma líder de Seção 6.\n"
        "/download [URL] [video/audio] - Baixa e envia um vídeo ou áudio do link fornecido. Vou usar minha precisão para garantir o sucesso da missão!\n"
        "/daudio [URL] - Baixa e envia apenas o áudio do link fornecido. Com minha habilidade, vou garantir a qualidade do áudio!"
    )
    await update.message.reply_text(help_text)
    logger.info(f"Usuário {update.message.from_user.id} solicitou ajuda.")

# Comando de listagem de comandos
async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    commands_text = (
        "Aqui estão os comandos disponíveis para você usar:\n\n"
        "/start - Inicia o bot e mostra uma mensagem de boas-vindas com o toque de uma chefe de Seção 6.\n"
        "/download [URL] [video/audio] - Baixa e envia um vídeo ou áudio do link fornecido. Com minha determinação e habilidades, você pode confiar na missão.\n"
        "/daudio [URL] - Baixa e envia apenas o áudio do link fornecido. Confie na minha precisão para entregar o áudio com qualidade.\n"
        "/help - Mostra essa mensagem de ajuda com a precisão de uma espadachin.\n"
        "/commands - Mostra todos os comandos disponíveis. Estou aqui para ajudar com a responsabilidade de uma líder!"
    )
    await update.message.reply_text(commands_text)
    logger.info(f"Usuário {update.message.from_user.id} solicitou a lista de comandos.")

# Função para responder a mensagens específicas
async def respond_to_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.lower()
    
    # Verifica saudações
    if 'bom dia' in message:
        await update.message.reply_text(get_miyabi_message('greeting'))
    elif 'boa noite' in message:
        await update.message.reply_text(get_miyabi_message('greeting'))

    # Verifica comandos não reconhecidos
    elif message.startswith('/'):
        await update.message.reply_text("Comando não reconhecido. Use /commands para ver a lista de comandos disponíveis.")

def main() -> None:
    application = ApplicationBuilder().token("seu_token_aqui").build()

    # Adiciona os handlers para os comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("download", download_media))
    application.add_handler(CommandHandler("daudio", download_audio))
    application.add_handler(CommandHandler("help", show_help))
    application.add_handler(CommandHandler("commands", list_commands))

    # Adiciona o handler para responder a mensagens específicas
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond_to_messages))

    application.run_polling()

if __name__ == '__main__':
    main()
