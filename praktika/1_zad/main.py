# main.py
from auth import register, login
from account import deposit, withdraw, transfer
from report import show_report

def main_menu():
    while True:
        print("\n=== Консольный банк ===")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("0. Выход")
        
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            username = login()
            if username:
                account_menu(username)
        elif choice == "2":
            register()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def account_menu(username: str):
    while True:
        print(f"\n=== Меню аккаунта [{username}] ===")
        print("1. Пополнить счёт")
        print("2. Снять средства")
        print("3. Перевести другому пользователю")
        print("4. Отчёт (баланс и история)")
        print("0. Выйти из аккаунта")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            deposit(username)
        elif choice == "2":
            withdraw(username)
        elif choice == "3":
            transfer(username)
        elif choice == "4":
            show_report(username)
        elif choice == "0":
            print(f"Вы вышли из аккаунта {username}.")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    from storage import ensure_directories
    ensure_directories()
    main_menu()