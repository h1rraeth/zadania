import os
import time
import threading
import csv
from datetime import datetime

import psutil

from utils import format_bytes, progress_bar
from logger import get_logger

log = get_logger("resource_monitor")

stop_event = threading.Event()   # для остановки потоков


def live_monitor(interval=2):
    print("Запущен живой мониторинг. Нажми Enter или q для остановки...\n")
    
    while not stop_event.is_set():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # CPU
        cpu = psutil.cpu_percent(interval=0.5)
        print(f"CPU:      {progress_bar(cpu)}")
        
        # RAM
        mem = psutil.virtual_memory()
        print(f"RAM:      {progress_bar(mem.percent)}  {format_bytes(mem.used)} / {format_bytes(mem.total)}")
        
        # Swap
        swap = psutil.swap_memory()
        print(f"Swap:     {progress_bar(swap.percent)}")
        
        # Диски
        print("\nДиски:")
        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                print(f"  {part.mountpoint:12} {progress_bar(usage.percent)}")
            except:
                pass
        
        # Количество процессов
        print(f"\nПроцессов: {len(psutil.pids())}")
        
        # Топ-3 по CPU
        print("\nТоп-3 по CPU:")
        for p in sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda x: x.info['cpu_percent'], reverse=True)[:3]:
            print(f"   {p.info['name'][:25]:25} {p.info['cpu_percent']:.1f}%")
        
        time.sleep(interval)
    
    print("\nМониторинг остановлен")


def start_live_monitor():
    stop_event.clear()
    thread = threading.Thread(target=live_monitor, daemon=True)
    thread.start()
    
    # Ждём команды остановки
    try:
        user_input = input()
        if user_input.lower() in ['q', 'quit', 'exit']:
            pass
    except:
        pass
    
    stop_event.set()
    time.sleep(0.5)  # даём потоку завершиться
    log.info("Живой мониторинг остановлен")


def record_metrics(filename="metrics.csv", duration=30):
    print(f"Запись метрик в {filename} на {duration} секунд...")
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "cpu_percent", "ram_percent", "ram_used_gb", "net_sent_kb"])
        
        start_time = time.time()
        net_old = psutil.net_io_counters()
        
        while time.time() - start_time < duration:
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            net_new = psutil.net_io_counters()
            
            sent_kb = (net_new.bytes_sent - net_old.bytes_sent) / 1024
            net_old = net_new
            
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{cpu:.1f}",
                f"{mem.percent:.1f}",
                f"{mem.used / 1024 / 1024 / 1024:.2f}",
                f"{sent_kb:.1f}"
            ])
            
            time.sleep(2)
    
    print(f"Запись завершена. Файл: {filename}")
    log.info(f"Метрики записаны в {filename}")


def set_alert(cpu_threshold=80, ram_threshold=80):
    print(f"Установлены оповещения: CPU > {cpu_threshold}%, RAM > {ram_threshold}%")
    log.info("Запущены пороговые оповещения")
    
    last_alert = 0
    while not stop_event.is_set():
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        
        if (cpu > cpu_threshold or ram > ram_threshold) and (time.time() - last_alert > 60):
            msg = f"ВНИМАНИЕ! CPU: {cpu:.1f}% | RAM: {ram:.1f}%"
            print(f"\n🔴 {msg}")
            log.warning(msg)
            last_alert = time.time()
        
        time.sleep(5)


def run():
    while True:
        print("МОНИТОРИНГ РЕСУРСОВ")
        print("1. Живой мониторинг (обновление каждые 2 сек)")
        print("2. Записать метрики в CSV (30 секунд)")
        print("3. Включить оповещения (CPU/RAM)")
        print("0. Назад в главное меню")
        
        choice = input("\nВыбери действие: ").strip()
        
        if choice == '1':
            start_live_monitor()
        elif choice == '2':
            record_metrics()
        elif choice == '3':
            set_alert()
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")
        
        input("\nНажми Enter чтобы продолжить...")


if __name__ == "__main__":
    run()