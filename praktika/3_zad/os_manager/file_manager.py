import os
import shutil
import hashlib
import zipfile
from pathlib import Path
from datetime import datetime

from utils import format_bytes, print_table, confirm
from logger import get_logger

log = get_logger("file_manager")

current_dir = os.getcwd()  # текущая папка


def list_dir():
    path = Path(current_dir)
    rows = []
    for item in sorted(path.iterdir()):
        stat = item.stat()
        size = format_bytes(stat.st_size) if item.is_file() else "<DIR>"
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
        typ = "DIR" if item.is_dir() else "FILE"
        rows.append([item.name, typ, size, mtime])

    print(f"\nТекущая папка: {current_dir}")
    print_table(["Имя", "Тип", "Размер", "Изменён"], rows)
    log.info(f"Просмотр папки: {current_dir}")


def change_dir():
    """Сменить папку"""
    global current_dir
    path = input("Куда перейти (или ..): ").strip()
    try:
        if path == "..":
            new_path = Path(current_dir).parent
        else:
            new_path = Path(path).resolve()

        if new_path.is_dir():
            current_dir = str(new_path)
            print(f"Перешли в: {current_dir}")
            log.info(f"Смена папки → {current_dir}")
        else:
            print("Такой папки нет")
    except Exception as e:
        print(f"Ошибка: {e}")


def show_tree():
    print(f"\nДерево папок (до 3 уровней):")
    print(current_dir)
    _tree(Path(current_dir), "")


def _tree(path: Path, prefix: str):
    items = sorted(path.iterdir(), key=lambda x: x.is_file())
    for i, item in enumerate(items):
        last = i == len(items) - 1
        print(f"{prefix}{'└── ' if last else '├── '}{item.name}")
        if item.is_dir() and len(prefix) < 12:  # ограничение глубины
            _tree(item, prefix + ("    " if last else "│   "))


def create_file():
    name = input("Имя нового файла: ").strip()
    if name:
        try:
            Path(current_dir, name).touch()
            print(f"Файл создан: {name}")
            log.info(f"Создан файл {name}")
        except Exception as e:
            print(f"Ошибка: {e}")


def create_dir():
    name = input("Имя новой папки: ").strip()
    if name:
        try:
            os.makedirs(os.path.join(current_dir, name), exist_ok=True)
            print(f"Папка создана: {name}")
            log.info(f"Создана папка {name}")
        except Exception as e:
            print(f"Ошибка: {e}")


def copy_item():
    src = input("Что копировать: ").strip()
    dst = input("Куда (имя или .): ").strip() or "."
    try:
        shutil.copy2(os.path.join(current_dir, src), os.path.join(current_dir, dst))
        print("Скопировано")
        log.info(f"Скопировано {src}")
    except Exception as e:
        print(f"Ошибка: {e}")


def move_item():
    src = input("Что переместить/переименовать: ").strip()
    dst = input("Новое имя: ").strip()
    try:
        shutil.move(os.path.join(current_dir, src), os.path.join(current_dir, dst))
        print("Готово")
        log.info(f"Перемещено {src} → {dst}")
    except Exception as e:
        print(f"Ошибка: {e}")


def delete_item():
    name = input("Что удалить: ").strip()
    path = os.path.join(current_dir, name)
    if os.path.isfile(path):
        try:
            os.remove(path)
            print("Файл удалён")
            log.info(f"Удалён файл {name}")
        except Exception as e:
            print(f"Ошибка: {e}")
    elif os.path.isdir(path):
        if confirm(f"Удалить папку '{name}' со всем содержимым?"):
            try:
                shutil.rmtree(path)
                print("Папка удалена")
                log.info(f"Удалена папка {name}")
            except Exception as e:
                print(f"Ошибка: {e}")


def search():
    pattern = input("Шаблон для поиска (например *.py): ").strip() or "*.*"
    path = Path(current_dir)
    results = list(path.rglob(pattern))
    rows = [
        [str(p.relative_to(current_dir)), "DIR" if p.is_dir() else "FILE"]
        for p in results
    ]
    print_table(["Путь", "Тип"], rows)
    log.info(f"Поиск '{pattern}' — найдено {len(results)}")


def dir_stats():
    path = Path(current_dir)
    total_size = 0
    files = 0
    dirs = 0
    for item in path.rglob("*"):
        if item.is_file():
            files += 1
            total_size += item.stat().st_size
        else:
            dirs += 1
    print(f"\nСтатистика папки {current_dir}")
    print(f"Файлов: {files}")
    print(f"Папок:  {dirs}")
    print(f"Размер: {format_bytes(total_size)}")


def file_hash():
    name = input("Имя файла для хэша: ").strip()
    if not name:
        return
    try:
        data = Path(current_dir, name).read_bytes()
        print("MD5:   ", hashlib.md5(data).hexdigest())
        print("SHA256:", hashlib.sha256(data).hexdigest())
        log.info(f"Хэши посчитаны для {name}")
    except Exception as e:
        print(f"Ошибка: {e}")


def create_zip():
    name = input("Имя архива (.zip): ").strip()
    if name:
        try:
            with zipfile.ZipFile(
                os.path.join(current_dir, name), "w", zipfile.ZIP_DEFLATED
            ) as zf:
                for root, _, files in os.walk(current_dir):
                    for f in files:
                        zf.write(
                            os.path.join(root, f),
                            os.path.relpath(os.path.join(root, f), current_dir),
                        )
            print("ZIP-архив создан")
            log.info(f"Создан ZIP: {name}")
        except Exception as e:
            print(f"Ошибка: {e}")


def run():
    global current_dir
    while True:
        print("ФАЙЛОВЫЙ МЕНЕДЖЕР")
        print(f"Папка: {current_dir}")
        print("1. Показать файлы")
        print("2. Сменить папку")
        print("3. Показать дерево")
        print("4. Создать файл")
        print("5. Создать папку")
        print("6. Копировать")
        print("7. Переместить/переименовать")
        print("8. Удалить")
        print("9. Поиск по шаблону")
        print("10. Статистика папки")
        print("11. Хэш файла (MD5+SHA256)")
        print("12. Создать ZIP")
        print("0. Назад в главное меню")

        choice = input("\nВыбери действие: ").strip()

        if choice == "1":
            list_dir()
        elif choice == "2":
            change_dir()
        elif choice == "3":
            show_tree()
        elif choice == "4":
            create_file()
        elif choice == "5":
            create_dir()
        elif choice == "6":
            copy_item()
        elif choice == "7":
            move_item()
        elif choice == "8":
            delete_item()
        elif choice == "9":
            search()
        elif choice == "10":
            dir_stats()
        elif choice == "11":
            file_hash()
        elif choice == "12":
            create_zip()
        elif choice == "0":
            break
        else:
            print("Неверный выбор!")

        input("\nНажми Enter чтобы продолжить...")


if __name__ == "__main__":
    run()
