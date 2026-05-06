import asyncio
import websockets


async def client():
    """
    WebSocket-клиент, который:
    1. Подключается к серверу на ws://localhost:8765
    2. Отправляет одно сообщение "Привет, сервер!"
    3. Получает 5 ответных сообщений и выводит их в консоль
    """
    uri = "ws://localhost:8765"  # Адрес WebSocket-сервера

    print(f"Подключение к серверу {uri}...")

    # Устанавливаем соединение с сервером
    # async with гарантирует автоматическое закрытие соединения после завершения
    async with websockets.connect(uri) as websocket:
        # Отправляем одно сообщение серверу
        message = "Привет, сервер!"
        print(f"Отправка сообщения: {message}")
        await websocket.send(message)

        # Получаем 5 ответных сообщений от сервера
        print("Получены ответы от сервера:")
        print("-" * 40)

        for i in range(5):
            response = await websocket.recv()
            print(response)

        print("-" * 40)
        print("Все 5 сообщений успешно получены")


async def main():
    """
    Основная функция с обработкой возможных ошибок подключения
    """
    try:
        await client()
    except ConnectionRefusedError:
        print("Ошибка: Не удалось подключиться к серверу.")
        print("Убедитесь, что WebSocket-сервер запущен на ws://localhost:8765")
        print("Запустите сервер командой: python -m websocket_users_server")
    except websockets.exceptions.ConnectionClosed:
        print("Ошибка: Соединение с сервером было разорвано")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    # Запускаем асинхронную клиентскую функцию
    asyncio.run(main())
