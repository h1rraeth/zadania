import matplotlib.pyplot as plt

# Глобальные фигура и ось
fig = None
ax = None

def init_visualizer():
    global fig, ax
    if fig is None:
        fig, ax = plt.subplots(figsize=(14, 7))
        plt.ion()

def draw(array, comparing=[], sorted_indices=[], title="", step_count=0, delay=0.06):
    global fig, ax
    init_visualizer()
    
    ax.clear()
    n = len(array)
    
    # Цвета по ТЗ
    colors = ['#3498db'] * n                     # обычный — синий
    for idx in comparing:
        if 0 <= idx < n:
            colors[idx] = '#e74c3c'              # сравниваемые — красный
    for idx in sorted_indices:
        if 0 <= idx < n:
            colors[idx] = '#2ecc71'              # отсортированные — зелёный
    
    bars = ax.bar(range(n), array, color=colors, edgecolor='black', linewidth=0.7)
    
    # Значения над столбцами (для N ≤ 30)
    if n <= 30:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax.set_title(f"{title} — Шаг: {step_count} | Элементов: {n}", fontsize=16, pad=20)
    ax.set_xlabel("Индекс")
    ax.set_ylabel("Значение")
    if array:
        ax.set_ylim(0, max(array) * 1.12)
    
    plt.draw()
    plt.pause(delay)