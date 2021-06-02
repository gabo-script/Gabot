import pyshorteners
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction, MessageEntity

# Formato de información del bot por consola
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s,'
)

logger = logging.getLogger()


# Respuesta a /start
def start(update, context):

    user_name = update.effective_user['first_name']
    id = update.effective_user['id']

    logger.info(f'El usuario {id} se ha conectado')

    update.message.reply_text(
        parse_mode='HTML',
        text=f'Bienvenido, <b>{user_name}</b>'
    )


# Respuesta a /botinfo
def getBotInfo(update, context):

    chat = update.message.chat
    id = update.effective_user['id']
    logger.info(f'El usuario {id} ha solicitado información del bot')

    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )

    chat.send_message(
        parse_mode='HTML',
        text='Soy un bot creado por <b>Gabriel Chonate</b>'
    )


# Acortador de URL
def inputUrl(update, context):

    url = update.message.text
    id = update.effective_user['id']
    chat = update.message.chat
    logger.info(f'El usuario {id} ha enviado un enlace')

    # Acortar URL
    s = pyshorteners.Shortener()
    short = s.chilpit.short(url)
    'http://chilp.it/TEST'

    # Barra de estado
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )

    # Enviar URL acortado
    chat.send_message(
        text=f'Tu URL recortada es {short}'
    )


# Respuesta si es texto
def validate(update, context):

    chat = update.message.chat
    id = update.effective_user['id']

    logger.info(f'El usuario {id} ha enviado un texto')
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    chat.send_message(
        text='No logro entenderte'
    )


if __name__ == '__main__':

    # Conexión a telegram
    updater = Updater(token=os.environ['TOKEN'], use_context=True)
    dp = updater.dispatcher

    # Comandos
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('botinfo', getBotInfo))

    # Respuesta si es enlace 
    dp.add_handler(MessageHandler(
        Filters.entity(MessageEntity.URL) |
        Filters.entity(MessageEntity.TEXT_LINK),
        inputUrl
    ))

    # Respuesta si es texto
    dp.add_handler(MessageHandler(Filters.text, validate))

    updater.start_polling()  # Rastrear mensajes entrantes
    print('Bot running')
    updater.idle()  # Finalizar bot con Ctrl + c
