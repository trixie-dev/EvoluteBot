import telegram
import telegram.ext
import dropbox_builds as db
from datetime import datetime
import time
import os

TOKEN = '6027313496:AAH67YmKNZNDoh3SmD0PFEHQ7co7dX91NdE'
CHAT_ID = None
LAST_FOLDER = None
FILES_PATH = "C:\\Users\\mckin\\Desktop\\files"

bot = telegram.Bot(token=TOKEN)

def send_file(chat_id, file_path):
    """Функція для надсилання файлу у чат"""
    try:
        with open(file_path, 'rb') as f:
            bot.send_document(chat_id=chat_id, document=f)
    except FileNotFoundError:
        bot.send_message(chat_id=chat_id, text="Файл не знайдено :(")

def handle_message(update, context):
    """Функція-обробник вхідного повідомлення"""
    # Отримуємо id чату з файлу chat_id.txt
    with open('chat_id.txt', 'r') as f:
        CHAT_ID = f.read()
    message_text = update.message.text
    bot.send_message(chat_id=CHAT_ID, text="One moment please...")
    # Якщо користувач надіслав команду /file, надішлемо файл
    if message_text == '/file':
        # disk D file: 
        db.download_folder_content(db.folder_path)
        # надіслати всі файли з FILES_PATH
        for i in os.listdir(FILES_PATH):
            send_file(chat_id=CHAT_ID, file_path=f"{FILES_PATH}\\{i}")
    else:
        bot.send_message(chat_id=chat_id, text="Невідома команда :(")

def setup(update, context):
    """Функція для збереження group chat id"""
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    # Зберігаємо group chat id у файл
    with open('chat_id.txt', 'w') as f:
        f.write(str(CHAT_ID))
    bot.send_message(chat_id=CHAT_ID, text=f"Group chat id збережено! + {CHAT_ID}")

if __name__ == '__main__':
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler('setup', setup))  # Додаємо обробник команди /setup
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    updater.start_polling()
    with open('chat_id.txt', 'r') as f:
        CHAT_ID = f.read()
    while True:
        print(f"[{datetime.now()}] Checking for new files...")
        last_folder = db.get_latest_folder_name(db.folder_path) # 040523
        with open('last_folder.txt', 'r') as f:
            if last_folder != f.read():
                LAST_FOLDER = last_folder
                # remove all files from FILES_PATH
                for i in os.listdir(FILES_PATH):
                    os.remove(f"{FILES_PATH}\\{i}")
                    
                db.download_folder_content(db.folder_path)
                
                for i in os.listdir(FILES_PATH):
                    send_file(chat_id=CHAT_ID, file_path=f"{FILES_PATH}\\{i}")
                
                with open('last_folder.txt', 'w') as f:
                    f.write(last_folder)
        time.sleep(40)


