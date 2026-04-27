import matplotlib.pyplot as plt


def print_comparison(n, stats_dict):
    print("\n" + "=" * 50)
    print(f"Сравнение алгоритмов (N = {n})")
    print("=" * 50)
    print(f"{'Алгоритм':<15} {'Шагов (сравнений)':>20}")
    print("-" * 50)
    for algo, steps in stats_dict.items():
        print(f"{algo:<15} {steps:>20}")
    print("=" * 50)
    winner = min(stats_dict, key=stats_dict.get)
    print(f"Победитель по шагам: {winner}")
    print("=" * 50)


def plot_comparison(n, stats_dict):
    algos = list(stats_dict.keys())
    steps_list = list(stats_dict.values())
    plt.figure(figsize=(8, 5))
    bars = plt.bar(algos, steps_list, color=["#e74c3c", "#3498db", "#2ecc71"])
    plt.title(f"Сравнение алгоритмов (N = {n})")
    plt.ylabel("Количество сравнений")
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height + 5,
            str(int(height)),
            ha="center",
            va="bottom",
        )
    plt.tight_layout()
    plt.show()
