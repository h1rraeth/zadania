import logging
from logging.handlers import RotatingFileHandler
import os

# Константы
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "os_manager.log")

# Создаём папку logs, если её нет
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(module_name: str) -> logging.Logger:
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    # Чтобы не дублировать handlers
    if not logger.handlers:
        handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=1_000_000,  # 1 МБ
            backupCount=3,
            encoding="utf-8",  # ← ВАЖНОЕ ИСПРАВЛЕНИЕ
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def show_logs(n: int = 50, level: str = None) -> None:
    if not os.path.exists(LOG_FILE):
        print("Лог-файл пока не создан.")
        return

    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        last_lines = lines[-n:]

        print(f"\n=== Последние {len(last_lines)} строк из лога ===\n")
        for line in last_lines:
            line = line.strip()
            if not line:
                continue
            if level is None or f"| {level.upper()} |" in line:
                print(line)
    except Exception as e:
        print(f"Ошибка чтения лога: {e}")


def run():
    print("ТЕСТ СИСТЕМЫ ЛОГИРОВАНИЯ")

    log = get_logger("test")

    log.info("Тестовое INFO сообщение")
    log.warning("Тестовое WARNING сообщение")
    log.error("Тестовое ERROR сообщение")
    log.critical("Тестовое CRITICAL сообщение")

    print("\nЛоги успешно записаны в logs/os_manager.log")
    print("Показываю последние 20 строк:")
    show_logs(n=20)


if __name__ == "__main__":
    run()
