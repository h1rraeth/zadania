# auth.py
import hashlib
from storage import load_users, save_users


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def is_valid_username(username: str) -> bool:
    if len(username) < 3:
        return False
    return username.isalnum()  # только латинские буквы и цифры


def register():
    print("\n=== Регистрация ===")
    username = input("Введите логин: ").strip()

    if not is_valid_username(username):
        print(
            "Ошибка: Логин должен содержать только латинские буквы и цифры, минимум 3 символа."
        )
        return None

    users = load_users()
    if username in users:
        print("Ошибка: Такой логин уже занят.")
        return None

    password = input("Введите пароль (минимум 6 символов): ").strip()
    if len(password) < 6:
        print("Ошибка: Пароль должен быть не менее 6 символов.")
        return None

    password_hash = hash_password(password)

    users[username] = {
        "password_hash": password_hash,
        "balance": 0.0,
        "blocked": False,
        "failed_attempts": 0,
    }

    save_users(users)
    print(f"Пользователь {username} успешно зарегистрирован!")
    return username


def login():
    print("\n=== Вход в систему ===")
    username = input("Логин: ").strip()

    users = load_users()
    if username not in users:
        print("Ошибка: Пользователь не найден.")
        return None

    user = users[username]
    if user.get("blocked", False):
        print(
            "Аккаунт заблокирован из-за слишком большого количества неудачных попыток входа."
)
        return None

    password = input("Пароль: ").strip()
    if hash_password(password) != user["password_hash"]:
        user["failed_attempts"] += 1
        if user["failed_attempts"] >= 3:
            user["blocked"] = True
            print("Аккаунт заблокирован после 3 неудачных попыток.")
        else:
            attempts_left = 3 - user["failed_attempts"]
            print(f"Неверный пароль. Осталось попыток: {attempts_left}")
        save_users(users)
        return None

    # Успешный вход
    user["failed_attempts"] = 0
    save_users(users)
    print(f"Добро пожаловать, {username}!")
    return username
