import os
import asyncio
import ssl
import urllib.parse

async def download_image(url, save_path):
    try:
        # Разбираем URL для получения хоста и пути
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.netloc
        path = parsed_url.path

        # Отключаем проверку SSL-сертификатов
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Устанавливаем соединение
        reader, writer = await asyncio.open_connection(host, 443, ssl=ssl_context)

        # Отправляем HTTP-запрос
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        writer.write(request.encode())
        await writer.drain()

        # Читаем ответ
        response = await reader.read()
        writer.close()
        await writer.wait_closed()

        # Проверяем статус ответа
        if response.startswith(b"HTTP/1.1 200 OK"):
            # Извлекаем тело ответа (изображение)
            headers, body = response.split(b"\r\n\r\n", 1)
            filename = os.path.join(save_path, os.path.basename(url))
            with open(filename, 'wb') as f:
                f.write(body)
            return url, "Успех"
        else:
            return url, "Ошибка"
    except Exception:
        return url, f"Ошибка"

def table_links(results):
    # Заголовки таблицы
    headers = ["Ссылка", "Статус"]

    # Данные для таблицы
    data = [
        [url, status]
        for url, status in results
    ]

    # Определяем максимальную длину для каждого столбца
    max_lens = [max(len(str(row[i])) for row in data + [headers]) + 2 for i in range(len(headers))]

    # Функция для создания строки таблицы
    def create_row(cells, max_lens):
        return "| " + " | ".join(str(cell).ljust(max_len) for cell, max_len in zip(cells, max_lens)) + " |"

    # Создаём верхнюю границу таблицы
    def create_border(max_lens):
        return "+-" + "-+-".join("-" * max_len for max_len in max_lens) + "-+"

    # Создаём таблицу
    border = create_border(max_lens)
    table = [border]
    table.append(create_row(headers, max_lens))
    table.append(border)

    for row in data:
        table.append(create_row(row, max_lens))
    table.append(border)

    # Возвращаем таблицу как строку
    return "\n".join(table)

async def main():

    folder_path = "img"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Запрашиваем путь для сохранения изображений
    save_path = input("Введите путь для сохранения изображений: ").strip()
    while not os.path.isdir(save_path) or not os.access(save_path, os.W_OK):
        print("Некорректный путь или нет доступа для записи. Попробуйте снова.")
        save_path = input("Введите путь для сохранения изображений: ").strip()

    tasks = []
    while True:
        url = input("Введите ссылку на изображение (или нажмите Enter для завершения): ").strip()
        if not url:
            break
        # Создаём задачу для скачивания
        task = asyncio.create_task(download_image(url, save_path))
        tasks.append(task)


    results = await asyncio.gather(*tasks)
    print(table_links(results))


if __name__ == "__main__":
    asyncio.run(main())