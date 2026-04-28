import os

# Импортируем run() из всех модулей
from system_info import run as system_info_run
from process_manager import run as process_manager_run
from file_manager import run as file_manager_run
from resource_monitor import run as resource_monitor_run
from task_scheduler import run as task_scheduler_run
from logger import run as logger_run, show_logs
from utils import run as utils_run


def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 65)
        print("   ОС МЕНЕДЖЕР — Мониторинг и управление системой")
        print("=" * 65)
        print("1. Информация о системе")
        print("2. Менеджер процессов")
        print("3. Менеджер файлов")
        print("4. Мониторинг ресурсов")
        print("5. Планировщик задач")
        print("6. Просмотр логов")
        print("7. Тест вспомогательных функций (utils)")
        print("0. Выход")
        print("=" * 65)

        choice = input("Выберите пункт меню (0-7): ").strip()

        if choice == "0":
            print("Завершение работы программы...")
            break
        elif choice == "1":
            system_info_run()
        elif choice == "2":
            process_manager_run()
        elif choice == "3":
            file_manager_run()
        elif choice == "4":
            resource_monitor_run()
        elif choice == "5":
            task_scheduler_run()
        elif choice == "6":
            show_logs()
        elif choice == "7":
            utils_run()
        else:
            print("Ошибка: неверный пункт меню!")

        input("\nНажмите Enter для возврата в главное меню...")


if __name__ == "__main__":
    main()
