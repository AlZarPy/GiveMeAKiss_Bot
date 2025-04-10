import json
import os

LIKE_STORAGE_FILE = "like_storage.json"

# Функция для загрузки или создания файла хранения времени лайков
def load_like_storage():
    if not os.path.exists(LIKE_STORAGE_FILE):
        print(f"{LIKE_STORAGE_FILE} не найден. Создаю новый.")
        return {}
    with open(LIKE_STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Функция для сохранения времени последней реакции в файл
def save_like_storage(like_storage):
    with open(LIKE_STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(like_storage, f, indent=4, ensure_ascii=False)
