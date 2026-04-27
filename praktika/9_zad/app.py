from utils import add, subtract, multiply, divide

def calculator():
    print("Простой калькулятор")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    
    choice = input("Выберите операцию (1/2/3/4): ")
    try:
        num1 = float(input("Первое число: "))
        num2 = float(input("Второе число: "))
    except ValueError:
        print("Ошибка: введите числа!")
        return

    if choice == '1':
        print(f"Результат: {add(num1, num2)}")
    elif choice == '2':
        print(f"Результат: {subtract(num1, num2)}")
    elif choice == '3':
        print(f"Результат: {multiply(num1, num2)}")
    elif choice == '4':
        try:
            print(f"Результат: {divide(num1, num2)}")
        except ValueError as e:
            print(e)
    else:
        print("Неверный выбор!")

if __name__ == "__main__":
    calculator()