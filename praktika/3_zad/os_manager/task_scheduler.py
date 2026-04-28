import os
import subprocess
import threading
import time
from datetime import datetime

from utils import confirm
from logger import get_logger

log = get_logger("task_scheduler")

# Глобальный список задач
tasks = []          # каждая задача — словарь
task_threads = {}   # храним потоки по имени задачи


def add_task():
    name = input("Имя задачи: ").strip()
    if not name or any(t['name'] == name for t in tasks):
        print("Имя пустое или уже занято!")
        return

    command = input("Команда для выполнения: ").strip()
    if not command:
        print("Команда не может быть пустой!")
        return

    print("\nТип задачи:")
    print("1. once   — выполнить один раз (через N секунд)")
    print("2. repeat — повторять каждые N секунд")
    typ = input("Выбери тип (1 или 2): ").strip()

    if typ == '1':
        task_type = "once"
        try:
            param = int(input("Через сколько секунд запустить? (по умолчанию 5): ") or 5)
        except:
            param = 5
    else:
        task_type = "repeat"
        try:
            param = int(input("Интервал в секундах (минимум 5): ") or 10)
            if param < 5 and not confirm("Интервал меньше 5 секунд. Продолжить?"):
                return
        except:
            param = 10

    task = {
        "name": name,
        "command": command,
        "type": task_type,
        "param": param,
        "status": "ожидает",
        "last_run": None,
        "output": ""
    }
    tasks.append(task)
    print(f"Задача '{name}' добавлена!")
    log.info(f"Добавлена задача '{name}' ({task_type})")

    # Запускаем в фоне
    start_task_thread(task)


def start_task_thread(task):
    def runner():
        while True:
            try:
                result = subprocess.run(
                    task["command"],
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                task["last_run"] = datetime.now().strftime("%H:%M:%S")
                task["output"] = result.stdout + result.stderr
                task["status"] = "выполнена" if result.returncode == 0 else "ошибка"
                
                log.info(f"Задача '{task['name']}' выполнена (код {result.returncode})")
                
                if task["type"] == "once":
                    break  # один раз и всё
            except Exception as e:
                task["output"] = f"Ошибка: {e}"
                task["status"] = "ошибка"
            
            if task["type"] == "repeat":
                time.sleep(task["param"])
            else:
                break

    thread = threading.Thread(target=runner, daemon=True)
    thread.start()
    task_threads[task["name"]] = thread


def list_tasks():
    if not tasks:
        print("Нет активных задач.")
        return
    rows = []
    for t in tasks:
        rows.append([
            t["name"],
            t["type"],
            t["command"][:35],
            t["status"],
            t["last_run"] or "—"
        ])
    from utils import print_table
    print_table(["Имя", "Тип", "Команда", "Статус", "Последний запуск"], rows)


def delete_task():
    name = input("Имя задачи для удаления: ").strip()
    for i, t in enumerate(tasks):
        if t["name"] == name:
            tasks.pop(i)
            if name in task_threads:
                # просто удаляем ссылку (daemon=True — поток умрёт сам)
                del task_threads[name]
            print(f" Задача '{name}' удалена")
            log.info(f"Удалена задача '{name}'")
            return
    print(" Задача не найдена")


def show_task_output():
    name = input("Имя задачи: ").strip()
    for t in tasks:
        if t["name"] == name:
            print(f"\nВывод задачи '{name}':")
            print("-" * 60)
            print(t.get("output") or "Пока нет вывода")
            return
    print(" Задача не найдена")


def run():
    while True:
        print("ПЛАНИРОВЩИК ЗАДАЧ")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Удалить задачу")
        print("4. Показать вывод задачи")
        print("0. Назад в главное меню")
        
        choice = input("\nВыбери действие: ").strip()
        
        if choice == '1':
            add_task()
        elif choice == '2':
            list_tasks()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            show_task_output()
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")
        
        input("\nНажми Enter чтобы продолжить...")


if __name__ == "__main__":
    run()