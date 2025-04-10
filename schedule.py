import os
import subprocess
import logging

def create_task_if_needed():
    logging.info("Создание задач планировщика...")
    print("Создание задач планировщика...")

    task_names = [
        ("GiveMeAKissBot_morning_kiss_Repeat", "12:00"),
        ("GiveMeAKissBot_evening_kiss_Repeat", "18:00")
    ]

    exe_path = os.path.abspath("GiveMeAKissBot.exe")
    run_command = f'cmd /c start "" /min "{exe_path}"'

    schtasks_path = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "System32", "schtasks.exe")

    if not os.path.exists(schtasks_path):
        logging.warning("schtasks.exe не найден. Убедитесь, что скрипт запущен с правами администратора.")
        return

    for name, time in task_names:
        try:
            check = subprocess.run([
                schtasks_path, "/Query", "/TN", name
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if check.returncode == 0:
                logging.info(f"Задача уже существует: {name}")
                print(f"Для удаления задачи выполните: stop_bot.bat")
                continue

            result = subprocess.run([
                schtasks_path,
                "/Create",
                "/SC", "DAILY",
                "/TN", name,
                "/TR", run_command,
                "/ST", time,
                "/F"
            ], capture_output=True, text=True, shell=False)

            if result.returncode == 0:
                logging.info(f"Задача создана: {name}")
                print(f"Запуск автоматически в {time}")
                print(f"Для удаления задач выполните: stop_bot.bat")
            else:
                logging.warning(f"Не удалось создать задачу: {name}")
                logging.warning(f"STDOUT: {result.stdout.strip() or '<пусто>'}")
                logging.warning(f"STDERR: {result.stderr.strip() or '<пусто>'}")

        except Exception as e:
            logging.warning(f"Ошибка при создании задачи {name}: {e}")

    # Создание stop_bot.bat
    stop_path = os.path.abspath("stop_bot.bat")
    with open(stop_path, "w", encoding="utf-8") as f:
        f.write(f"@echo off\n")
        for name, _ in task_names:
            f.write(f'"{schtasks_path}" /Delete /TN "{name}" /F\n')
        f.write("echo GiveMeAKissBot задачи удалены из планировщика\n")
        f.write("pause\n")

    logging.info(f"Для удаления задач выполните: {stop_path}")
