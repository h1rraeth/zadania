# report.py
from storage import load_users, load_transactions


def show_report(username: str):
    users = load_users()
    user = users.get(username)
    if not user:
        print("Ошибка: Пользователь не найден.")
        return

    transactions = load_transactions(username)
    recent = transactions[-10:]  # последние 10

    print("\n" + "=" * 55)
    print(f"Пользователь: {username}")
    print(f"Баланс: {user['balance']:.2f} ₸")
    print("=" * 55)

    if not recent:
        print("История транзакций пуста.")
        print("=" * 55)
        return

    print(f"{'Дата и время':<20} {'Тип':<18} {'Сумма':<10} Примечание")
    print("-" * 55)

    type_names = {
        "deposit": "Пополнение",
        "withdraw": "Снятие",
        "transfer_out": "Перевод исх.",
        "transfer_in": "Перевод вх.",
    }

    for t in recent:
        type_name = type_names.get(t["type"], t["type"])
        amount_str = f"{t['amount']:.2f}"
        print(f"{t['date']:<20} {type_name:<18} {amount_str:<10} {t['note']}")

    print("=" * 55)
