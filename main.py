import logging
import os
import sys
import io
import asyncio

# Определяем базовую директорию (где находится .exe или .py)
BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))

# Меняем текущую директорию на базовую
os.chdir(BASE_DIR)

# Настройка кодировки для Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Путь к лог-файлу рядом с исполняемым файлом
log_path = os.path.join(BASE_DIR, "story_bot.log")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_path, encoding="utf-8-sig"),
        logging.StreamHandler(sys.stdout)
    ]
)

from config import create_or_load_config
from bot import run_bot
from schedule import create_task_if_needed

if __name__ == "__main__":
    config = create_or_load_config()

    try:
        create_task_if_needed()
    except Exception as e:
        logging.warning(f"Не удалось зарегистрировать задачу: {e}")

    asyncio.run(run_bot(config["api_id"], config["api_hash"]))
    input("\nЗадача выполнена, нажмите Enter, чтобы выйти...")
