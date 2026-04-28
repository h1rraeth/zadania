import psutil
import platform
import os
from datetime import datetime

from utils import print_table, confirm
from logger import get_logger

log = get_logger("process_manager")


def list_processes(sort_by="cpu", filter_user=None, min_cpu=None, min_ram=None):
    processes = []
    for proc in psutil.process_iter(
        [
            "pid",
            "name",
            "status",
            "cpu_percent",
            "memory_info",
            "username",
            "create_time",
        ]
    ):
        try:
            p = proc.info
            ram_mb = p["memory_info"].rss / 1024 / 1024 if p.get("memory_info") else 0.0
            start_time = (
                datetime.fromtimestamp(p["create_time"]).strftime("%H:%M:%S")
                if p.get("create_time")
                else "N/A"
            )

            # Применяем фильтры
            if filter_user and p.get("username") != filter_user:
                continue
            if min_cpu is not None and p.get("cpu_percent", 0) < min_cpu:
                continue
            if min_ram is not None and ram_mb < min_ram:
                continue

            processes.append(
                [
                    p["pid"],
                    p["name"][:25],
                    p["status"],
                    f"{p.get('cpu_percent', 0):.1f}%",
                    f"{ram_mb:.1f} MB",
                    p.get("username") or "N/A",
                    start_time,
                ]
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
            continue

    # Сортировка
    col_map = {"pid": 0, "name": 1, "cpu": 3, "ram": 4}
    if sort_by in col_map:
        processes.sort(
            key=lambda x: x[col_map[sort_by]], reverse=(sort_by in ["cpu", "ram"])
        )

    headers = ["PID", "Имя", "Статус", "CPU %", "RAM", "Пользователь", "Запуск"]
    print_table(headers, processes)
    log.info(f"Выведено {len(processes)} процессов (sort_by={sort_by})")


def find_by_name(name):
    processes = []
    for proc in psutil.process_iter(["pid", "name", "cpu_percent", "memory_info"]):
        try:
            if name.lower() in proc.info["name"].lower():
                p = proc.info
                ram_mb = (
                    p["memory_info"].rss / 1024 / 1024 if p.get("memory_info") else 0.0
                )
                processes.append(
                    [
                        p["pid"],
                        p["name"],
                        f"{p.get('cpu_percent', 0):.1f}%",
                        f"{ram_mb:.1f} MB",
                    ]
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    headers = ["PID", "Имя", "CPU %", "RAM"]
    print_table(headers, processes)
    log.info(f"Найдено {len(processes)} процессов по имени '{name}'")


def process_details(pid):
    try:
        p = psutil.Process(pid)
        print(f"\n Детали процесса PID={pid} — {p.name()}")
        print(f"Путь к файлу:     {p.exe()}")
        print(f"Рабочая папка:    {p.cwd()}")
        print(f"Статус:           {p.status()}")
        print(f"CPU:              {p.cpu_percent(interval=0.1):.1f}%")
        print(f"RAM:              {p.memory_info().rss / 1024 / 1024:.1f} MB")

        print("\nОткрытые файлы:")
        for f in p.open_files()[:8]:
            print(f"   {f.path}")

        print("\nСетевые соединения:")
        for conn in p.connections()[:5]:
            print(f"   {conn.laddr} → {conn.raddr or '—'}")

        print(f"\nДочерние процессы: {len(p.children())} шт.")
        print(f"Переменных окружения: {len(p.environ())}")
        log.info(f"Просмотрены детали PID={pid} ({p.name()})")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print(" Нет доступа или процесс не существует")
        log.error(f"Нет доступа к PID={pid}")


def kill_process(pid, force=False):
    if pid == os.getpid():
        print(" Нельзя завершить саму эту программу!")
        return
    try:
        p = psutil.Process(pid)
        name = p.name()

        # Защита от системных процессов
        if pid < 100 or p.username() in ["SYSTEM", "root", "NT AUTHORITY\\SYSTEM"]:
            if not confirm(
                f" Процесс {name} (PID={pid}) выглядит системным. Завершить?"
            ):
                return

        if force:
            p.kill()
            print(f" Принудительно завершён: {name} (PID={pid})")
            log.info(f"Принудительно завершён {name} (PID={pid})")
        else:
            p.terminate()
            print(f" Мягко завершён: {name} (PID={pid})")
            log.info(f"Мягко завершён {name} (PID={pid})")
    except Exception as e:
        print(f" Ошибка: {e}")
        log.error(f"Не удалось завершить PID={pid} — {e}")


def suspend_process(pid):
    """Приостановка процесса"""
    try:
        p = psutil.Process(pid)
        if platform.system() == "Windows":
            p.suspend()
        else:
            p.send_signal(psutil.signal.SIGSTOP)
        print(f" Приостановлен PID={pid}")
        log.info(f"Приостановлен PID={pid}")
    except Exception as e:
        print(f" Ошибка: {e}")


def resume_process(pid):
    """Возобновление процесса"""
    try:
        p = psutil.Process(pid)
        if platform.system() == "Windows":
            p.resume()
        else:
            p.send_signal(psutil.signal.SIGCONT)
        print(f" Возобновлён PID={pid}")
        log.info(f"Возобновлён PID={pid}")
    except Exception as e:
        print(f" Ошибка: {e}")


def set_priority(pid, level):
    try:
        p = psutil.Process(pid)
        p.nice(level)
        print(f"Приоритет PID={pid} изменён на {level}")
        log.info(f"Установлен приоритет {level} для PID={pid}")
    except Exception as e:
        print(f"Ошибка: {e}")


def run():
    while True:
        print("МЕНЕДЖЕР ПРОЦЕССОВ")
        print("1. Показать список всех процессов")
        print("2. Поиск процесса по имени")
        print("3. Детали процесса (по PID)")
        print("4. Завершить процесс (мягко)")
        print("5. Принудительно завершить (KILL)")
        print("6. Приостановить процесс")
        print("7. Возобновить процесс")
        print("0. Вернуться в главное меню")
        print("-" * 65)

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            list_processes()
        elif choice == "2":
            name = input("Введите часть имени процесса: ").strip()
            if name:
                find_by_name(name)
        elif choice == "3":
            try:
                pid = int(input("Введите PID: "))
                process_details(pid)
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "4":
            try:
                pid = int(input("Введите PID: "))
                kill_process(pid)
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "5":
            try:
                pid = int(input("Введите PID: "))
                kill_process(pid, force=True)
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "6":
            try:
                pid = int(input("Введите PID: "))
                suspend_process(pid)
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "7":
            try:
                pid = int(input("Введите PID: "))
                resume_process(pid)
            except ValueError:
                print("Нужно ввести число!")
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    run()
