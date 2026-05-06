import asyncio
import websockets
from websockets import ServerConnection


async def handle_user(websocket: ServerConnection):
    """
    Обработчик WebSocket-соединения для одного пользователя.

    Логирует полученное сообщение и отправляет 5 ответных сообщений.
    """
    # Ожидаем получение сообщения от клиента
    async for message in websocket:
        # Логируем полученное сообщение в консоль
        print(f"Получено сообщение от пользователя: {message}")

        # Отправляем 5 ответных сообщений с порядковым номером
        for i in range(1, 6):
            response = f"{i} Сообщение пользователя: {message}"
            await websocket.send(response)
            # Небольшая задержка для имитации последовательной отправки
            await asyncio.sleep(0.1)


async def main():
    """
    Запуск WebSocket-сервера на порту 8765.
    """
    # Создаём сервер с обработчиком handle_user на localhost:8765
    server = await websockets.serve(handle_user, "localhost", 8765)

    print("WebSocket сервер запущен на ws://localhost:8765")
    print("Ожидание подключения и сообщений от клиентов...")

    # Ожидаем закрытия сервера (работает вечно до прерывания)
    await server.wait_closed()


if __name__ == "__main__":
    # Запускаем асинхронную main-функцию
    asyncio.run(main())
