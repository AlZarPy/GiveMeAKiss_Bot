import logging
import sys
import io
import asyncio
from config import create_or_load_config
from bot import run_bot
from schedule import create_task_if_needed

# Настройка кодировки для Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("story_bot.log"), logging.StreamHandler()]
)

if __name__ == "__main__":
    config = create_or_load_config()

    try:
        create_task_if_needed()
    except Exception as e:
        logging.warning(f"Не удалось зарегистрировать задачу: {e}")

    asyncio.run(run_bot(config["api_id"], config["api_hash"]))
    input("\nЗадача выполнена, нажмите Enter, чтобы выйти...")