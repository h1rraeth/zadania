import random
import matplotlib.pyplot as plt
from visualizer import draw
from algorithms.bubble import bubble_sort
from algorithms.selection import selection_sort
from algorithms.insertion import insertion_sort
from stats import print_comparison, plot_comparison


def get_user_input():
    while True:
        try:
            n = int(input("\nВведите количество элементов N (2-100): "))
            if 2 <= n <= 100:
                return n
            print("Ошибка: N должно быть от 2 до 100.")
        except ValueError:
            print("Ошибка: введите целое число.")


def choose_algorithm():
    print("\nВыберите алгоритм:")
    print("1. Сортировка пузырьком")
    print("2. Сортировка выбором")
    print("3. Сортировка вставками")
    print("4. Запустить все три алгоритма")
    while True:
        ch = input("Ваш выбор (1-4): ").strip()
        if ch in ["1", "2", "3", "4"]:
            return int(ch)
        print("Неверный выбор.")


def main():
    print("=== Визуальная сортировка ===")
    n = get_user_input()
    choice = choose_algorithm()

    # Генерация случайного массива
    original = [random.randint(1, 100) for _ in range(n)]
    random.shuffle(original)
    print(f"\nИсходный массив: {original}")

    if choice == 4:
        print("\nЗапуск всех трёх алгоритмов на одном массиве...")
        stats_dict = {}

        _, steps1 = bubble_sort(original[:], draw, "Сортировка пузырьком")
        stats_dict["Пузырёк"] = steps1

        _, steps2 = selection_sort(original[:], draw, "Сортировка выбором")
        stats_dict["Выбор"] = steps2

        _, steps3 = insertion_sort(original[:], draw, "Сортировка вставками")
        stats_dict["Вставки"] = steps3

        print_comparison(n, stats_dict)
        plot_comparison(n, stats_dict)
    else:
        titles = {
            1: "Сортировка пузырьком",
            2: "Сортировка выбором",
            3: "Сортировка вставками",
        }
        funcs = {1: bubble_sort, 2: selection_sort, 3: insertion_sort}

        algo_name = titles[choice]
        _, steps = funcs[choice](original[:], draw, algo_name)
        print(f"\n{algo_name} завершена за {steps} шагов.")

    print("\nПрограмма завершена. Закройте окно matplotlib.")
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
