import platform
import psutil
import socket
import urllib.request
from datetime import datetime

from utils import format_bytes, format_uptime, progress_bar
from logger import get_logger

log = get_logger("system_info")


def run():
    log.info("Запущена подсистема: Информация о системе")

    print("python main.pyИНФОРМАЦИЯ О СИСТЕМЕ")

    # === Секция 1: Операционная система ===
    print("\n1. ОПЕРАЦИОННАЯ СИСТЕМА")  
    print(f"ОС:                  {platform.system()} {platform.release()}")
    print(f"Версия:              {platform.version()}")
    print(f"Ядро:                {platform.uname().release}")
    print(f"Разрядность:         {platform.architecture()[0]}")
    print(f"Имя компьютера:      {platform.node()}")
    print(
        f"Текущий пользователь: {psutil.users()[0].name if psutil.users() else 'N/A'}"
    )

    boot_time = psutil.boot_time()
    uptime_sec = int(datetime.now().timestamp() - boot_time)
    print(
        f"Последняя загрузка:  {datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"Аптайм:              {format_uptime(uptime_sec)}")
    log.info("Секция ОС собрана")

    # === Секция 2: Процессор ===
    print("\n2. ПРОЦЕССОР")
    cpu_model = platform.processor() or "Неизвестно"
    print(f"Модель CPU:          {cpu_model}")
    print(f"Физических ядер:     {psutil.cpu_count(logical=False)}")
    print(f"Логических потоков:  {psutil.cpu_count(logical=True)}")

    freq = psutil.cpu_freq()
    print(f"Текущая частота:     {freq.current:.1f} MHz")
    if freq.max:
        print(f"Максимальная:        {freq.max:.1f} MHz")

    cpu_total = psutil.cpu_percent(interval=1)
    print(f"Общая загрузка CPU:  {cpu_total:.1f}%")

    print("Загрузка по ядрам:")
    for i, percent in enumerate(psutil.cpu_percent(percpu=True, interval=0.1)):
        print(f"   Core {i:2d}: {progress_bar(percent, width=15)}")
    log.info(f"CPU usage: {cpu_total:.1f}%")

    # === Секция 3: Память ===
    print("\n3. ПАМЯТЬ")
    mem = psutil.virtual_memory()
    print(f"Общий RAM:           {format_bytes(mem.total)}")
    print(f"Используется:        {format_bytes(mem.used)}")
    print(f"Свободно:            {format_bytes(mem.available)}")
    print(f"Использование RAM:   {progress_bar(mem.percent)}")

    swap = psutil.swap_memory()
    print(f"\nSwap всего:          {format_bytes(swap.total)}")
    print(f"Swap используется:   {format_bytes(swap.used)}")
    print(f"Swap %:              {progress_bar(swap.percent)}")
    log.info("Память собрана")

    # === Секция 4: Сеть ===
    print("\n4. СЕТЬ")
    for iface, addrs in psutil.net_if_addrs().items():
        print(f"Интерфейс: {iface}")
        for addr in addrs:
            if addr.family == socket.AF_INET:
                print(f"   IPv4:  {addr.address}")
            elif addr.family == socket.AF_INET6:
                print(f"   IPv6:  {addr.address}")
            elif hasattr(psutil, "AF_LINK") and addr.family == psutil.AF_LINK:
                print(f"   MAC:   {addr.address}")

    # Внешний IP
    try:
        external_ip = (
            urllib.request.urlopen("https://api.ipify.org", timeout=5)
            .read()
            .decode()
            .strip()
        )
        print(f"\nВнешний IP:          {external_ip}")
    except Exception:
        print("\nВнешний IP:          (нет подключения к интернету)")
    log.info("Секция сеть собрана")

    print("\nИнформация о системе успешно выведена!")
    log.info("Подсистема system_info завершена успешно")
