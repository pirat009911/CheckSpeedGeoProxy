---

````markdown
# Proxy Checker with GeoIP 🌍🕵️‍♂️

Скрипт на Python для проверки списка прокси-серверов на работоспособность и определения их геолокации по IP.

---

## 📌 Возможности

- Поддержка `http`, `socks4`, `socks5` прокси
- Многопоточная проверка (по умолчанию 30 потоков)
- Определение страны прокси с помощью базы данных MaxMind GeoLite2
- Вывод рабочих прокси и ISO-кода страны
- Отчёт в файл `working_proxies.txt` с указанием страны

---

## 📁 Структура проекта

<pre>
📁 project-root/
├── main.py                  # Основной скрипт
├── proxies.txt              # Входной файл со списком прокси
├── working_proxies.txt      # Выходной файл с рабочими прокси и кодами стран
├── GeoLite2-Country.mmdb    # База GeoIP (не включена в репозиторий)
├── requirements.txt
└── .gitignore
</pre>

---

## ⚙️ Установка

1. Установите Python 3.8+
2. Установите зависимости:

```bash
pip install -r requirements.txt
````

3. Скачайте базу GeoLite2:

* Зарегистрируйтесь и скачайте базу отсюда:
  👉 [https://dev.maxmind.com/geoip/geolite2-free-geolocation-data](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data)
* Поместите файл `GeoLite2-Country.mmdb` в корень проекта

---

## 📥 Подготовка

Создайте файл `proxies.txt` и добавьте туда список прокси в любом из поддерживаемых форматов:

```
123.45.67.89:8080
socks5://11.22.33.44:1080
http://55.66.77.88:3128
```

---

## 🚀 Запуск

```bash
python main.py
```

После выполнения рабочие прокси будут записаны в `working_proxies.txt`, каждая строка будет содержать прокси и ISO-код страны:

```
http://123.45.67.89:8080 | RU
socks5://11.22.33.44:1080 | DE
```

---




