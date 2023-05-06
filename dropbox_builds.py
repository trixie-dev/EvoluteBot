import dropbox
from datetime import datetime

# Встановіть свій токен доступу до API Dropbox
TOKEN = 'sl.Bd0A8JGTMsvVve3NCQfASjoSOyGtg6XYZ3QubKGyx6YSsTrfOBYZy-XlOI4Ggd-xMKnnAxZIgbbQ9nxF2aD0ufPlpuddVlmZMNRzjQy362jgWwgZ-NorG5z0BIvAutBZ9pyhZmO58oq_'

# Створіть клієнта Dropbox

# Вказівка на папку, з якої будемо завантажувати файли
folder_path = '/STABLE'
download_folder = 'files'

# Функція, що повертає ім'я найпершої папки по алфавіту знизу
def get_latest_folder_name(folder_path):
    client = dropbox.Dropbox(TOKEN)
    folder_names = []
    for entry in client.files_list_folder(folder_path).entries:
        if isinstance(entry, dropbox.files.FolderMetadata):
            folder_names.append(entry.name)
    if folder_names:
        return sorted(folder_names)[-1]
    return None


# Функція для завантаження вмісту папки
def download_folder_content(folder_path):
    client = dropbox.Dropbox(TOKEN)
    latest_folder_name = get_latest_folder_name(folder_path)
    if latest_folder_name:
        folder_path = f"{folder_path}/{latest_folder_name}"
        for entry in client.files_list_folder(folder_path).entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                _, res = client.files_download(f"{folder_path}/{entry.name}")
                data = res.content
                with open(f"{download_folder}/{entry.name}", "wb") as f:
                    f.write(data)
        print(f"[{datetime.now()}] Завантажено вміст папки")
    else:
        print("Папок не знайдено в папці")

# Виклик функції завантаження вмісту папки
