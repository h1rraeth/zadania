# account.py
from storage import load_users, save_users, add_transaction

def get_user_data(username: str) -> dict:
    users = load_users()
    return users.get(username)

def update_balance(username: str, new_balance: float):
    users = load_users()
    if username in users:
        users[username]["balance"] = round(float(new_balance), 2)
        save_users(users)

def deposit(username: str):
    print("\n=== Пополнение счёта ===")
    try:
        amount = float(input("Введите сумму пополнения: "))
        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            return
    except ValueError:
        print("Ошибка: Введите корректную сумму.")
        return

    users = load_users()
    user = users[username]
    user["balance"] = round(user["balance"] + amount, 2)
    save_users(users)

    add_transaction(username, "deposit", amount)
    print(f"Счёт успешно пополнен на {amount:.2f} ₸. Новый баланс: {user['balance']:.2f} ₸")

def withdraw(username: str):
    print("\n=== Снятие средств ===")
    try:
        amount = float(input("Введите сумму для снятия: "))
        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            return
    except ValueError:
        print("Ошибка: Введите корректную сумму.")
        return

    users = load_users()
    user = users[username]

    if amount > user["balance"]:
        print("Ошибка: Недостаточно средств на счёте.")
        return

    user["balance"] = round(user["balance"] - amount, 2)
    save_users(users)

    add_transaction(username, "withdraw", amount)
    print(f"Сумма {amount:.2f} ₸ успешно снята. Новый баланс: {user['balance']:.2f} ₸")

def transfer(username: str):
    print("\n=== Перевод другому пользователю ===")
    recipient = input("Введите логин получателя: ").strip()

    if recipient == username:
        print("Ошибка: Нельзя переводить самому себе.")
        return

    users = load_users()
    if recipient not in users:
        print("Ошибка: Получатель не найден.")
        return

    try:
        amount = float(input("Введите сумму перевода: "))
        if amount <= 0:
            print("Сумма должна быть больше нуля.")
            return
    except ValueError:
        print("Ошибка: Введите корректную сумму.")
        return

    sender = users[username]
    if amount > sender["balance"]:
        print("Ошибка: Недостаточно средств для перевода.")
        return

    # Атомарная операция
    sender["balance"] = round(sender["balance"] - amount, 2)
    users[recipient]["balance"] = round(users[recipient]["balance"] + amount, 2)

    save_users(users)

    # Запись транзакций
    add_transaction(username, "transfer_out", amount, f"→ {recipient}")
    add_transaction(recipient, "transfer_in", amount, f"← {username}")

    print(f"Перевод на сумму {amount:.2f} ₸ пользователю {recipient} выполнен успешно.")
    print(f"Ваш новый баланс: {sender['balance']:.2f} ₸")