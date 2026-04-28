def format_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.2f} {unit}" if unit != "B" else f"{int(n)} B"
        n /= 1024
    return f"{n:.2f} TB"


def format_uptime(seconds: int) -> str:
    days = seconds // 86400
    hours = (seconds % 86400) // 3600
    minutes = (seconds % 3600) // 60
    if days > 0:
        return f"{days} дн. {hours} ч. {minutes} мин."
    elif hours > 0:
        return f"{hours} ч. {minutes} мин."
    else:
        return f"{minutes} мин."


def progress_bar(percent: float, width: int = 20) -> str:
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percent:.1f}%"


def print_table(headers: list, rows: list) -> None:
    if not rows:
        print("Нет данных для отображения.")
        return

    # Определяем максимальную ширину каждого столбца
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    # Заголовок
    header_line = " | ".join(
        f"{str(h):<{col_widths[i]}}" for i, h in enumerate(headers)
    )
    print(header_line)
    print("-" * len(header_line))

    # Строки
    for row in rows:
        print(" | ".join(f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)))


def confirm(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ["y", "yes", "да"]:
            return True
        elif answer in ["n", "no", "нет"]:
            return False
        else:
            print("Пожалуйста, введите 'y' или 'n'.")


def run():
    print("=" * 60)
    print("ТЕСТ ВСПОМОГАТЕЛЬНЫХ ФУНКЦИЙ")
    print("=" * 60)

    print("1. format_bytes:")
    print("   1023  →", format_bytes(1023))
    print("   1024  →", format_bytes(1024))
    print("  1_500_000 →", format_bytes(1_500_000))
    print("2_000_000_000 →", format_bytes(2_000_000_000))

    print("\n2. format_uptime:")
    print("   3600 сек →", format_uptime(3600))
    print(" 86400 сек →", format_uptime(86400))
    print("172800 сек →", format_uptime(172800))

    print("\n3. progress_bar:")
    print("   0%  →", progress_bar(0))
    print("  45% →", progress_bar(45))
    print(" 100% →", progress_bar(100))

    print("\n4. print_table:")
    headers = ["Имя", "Возраст", "Город"]
    rows = [["Артём", 28, "Астана"], ["Мария", 25, "Алматы"], ["Иван", 35, "Москва"]]
    print_table(headers, rows)

    print("\n5. confirm (ответь y или n):")
    if confirm("Тест подтверждения"):
        print("Ты подтвердил действие!")
    else:
        print("Действие отменено.")


if __name__ == "__main__":
    run()
