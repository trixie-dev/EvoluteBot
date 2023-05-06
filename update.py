import evolute_bot
import dropbox_builds as db
import os
from datetime import datetime
from evolute_bot import send_file, FILES_PATH

CHAT_ID = None

def main():
    print(f"[{datetime.now()}] Checking for new files...")
    with open('chat_id.txt', 'r') as f:
        CHAT_ID = f.read()
    latest_folder = db.get_latest_folder_name(db.folder_path) # 040523
    with open('latest_folder.txt', 'r') as f:
        if latest_folder != f.read():
            LATEST_FOLDER = latest_folder
            # remove all files from FILES_PATH
            for i in os.listdir(FILES_PATH):
                os.remove(f"{FILES_PATH}/{i}")
                
            db.download_folder_content(db.folder_path)
            
            for i in os.listdir(FILES_PATH):
                send_file(chat_id=CHAT_ID, file_path=f"{FILES_PATH}\\{i}")
            
            with open('latest_folder.txt', 'w') as f:
                f.write(latest_folder)

main()