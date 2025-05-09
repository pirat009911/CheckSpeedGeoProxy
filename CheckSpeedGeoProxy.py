import requests
import threading
import time
import geoip2.database
from queue import Queue
import re

# Параметры
PROXY_FILE = 'proxies.txt'  # Файл со списком прокси
OUTPUT_FILE = 'working_proxies.txt'  # Файл для записи рабочих прокси
GEOIP_DB_PATH = 'GeoLite2-Country.mmdb'  # Путь к базе GeoLite2
NUM_THREADS = 30  # Количество потоков

# Очередь для прокси
proxy_queue = Queue()
working_proxies = []
total_proxies = 0
lock = threading.Lock()


# Функция для проверки прокси
def check_proxy(proxy):
    global total_proxies
    try:
        # Определяем формат прокси
        if not re.match(r"^(http|socks4|socks5)://", proxy):
            proxy = f"http://{proxy}"

        proxies = {"http": proxy, "https": proxy}

        # Проверяем прокси
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=5)
        if response.status_code == 200:
            with lock:
                # Получение геолокации
                reader = geoip2.database.Reader(GEOIP_DB_PATH)
                try:
                    ip_address = proxy.split('://')[-1].split(':')[0]
                    response_geo = reader.country(ip_address)  # Используем метод country
                    iso_code = response_geo.country.iso_code  # Получаем ISO код страны
                    working_proxies.append(f"{proxy} | {iso_code}")  # Сохраняем прокси и ISO код
                    print(f"Рабочий прокси найден: {proxy} | ISO код: {iso_code}")
                except Exception as geo_error:
                    print(f"Не удалось получить геолокацию для {proxy}: {geo_error}")
    except Exception as e:
        print(f"Ошибка проверки прокси {proxy}: {e}")
    finally:
        with lock:
            total_proxies -= 1


# Функция для обновления прогресса
def update_progress():
    while total_proxies > 0:
        time.sleep(1)
        with lock:
            progress = (len(working_proxies) / (total_proxies + len(working_proxies))) * 100 if total_proxies + len(
                working_proxies) > 0 else 100
            print(f"Прогресс: {progress:.2f}% | Всего найдено рабочих прокси: {len(working_proxies)}")


# Основная функция
def main():
    global total_proxies
    with open(PROXY_FILE, 'r') as f:
        proxies = f.read().splitlines()

    total_proxies = len(proxies)

    # Запуск потока для обновления прогресса
    progress_thread = threading.Thread(target=update_progress)
    progress_thread.start()

    # Запуск потоков для проверки прокси
    threads = []
    for proxy in proxies:
        thread = threading.Thread(target=check_proxy, args=(proxy,))
        threads.append(thread)
        thread.start()

    # Ожидание завершения всех потоков
    for thread in threads:
        thread.join()

    # Запись рабочих прокси в файл
    with open(OUTPUT_FILE, 'w') as f:
        for proxy in working_proxies:
            f.write(proxy + '\n')

    print("Проверка завершена.")


if __name__ == "__main__":
    main()
