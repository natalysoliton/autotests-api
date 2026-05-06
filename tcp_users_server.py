import socket
import threading


def tcp_users_server():
    """
    TCP-сервер, который сохраняет историю сообщений и отправляет её клиентам
    """
    # Создаем TCP-сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Привязываем к адресу и порту
    server_address = ('localhost', 12345)
    server_socket.bind(server_address)

    # Начинаем слушать входящие подключения (максимум 10 в очереди)
    server_socket.listen(10)
    print(f"Сервер запущен и ждет подключений на {server_address[0]}:{server_address[1]}")

    # Список для хранения всех сообщений от клиентов
    messages_history = []

    def handle_client(client_socket, client_address):
        """
        Обработка подключенного клиента
        """
        # Логируем подключение нового клиента
        print(f"Пользователь с адресом: {client_address} подключился к серверу")

        try:
            # Получаем данные от клиента
            data = client_socket.recv(1024).decode()

            # Логируем полученное сообщение
            print(f"Пользователь с адресом: {client_address} отправил сообщение: {data}")

            # Добавляем сообщение в историю
            messages_history.append(data)

            # Формируем ответ: вся история сообщений, каждое с новой строки
            if messages_history:
                response = '\n'.join(messages_history)
            else:
                response = "История сообщений пуста"

            # Отправляем историю клиенту
            client_socket.send(response.encode())

        except Exception as e:
            print(f"Ошибка при обработке клиента {client_address}: {e}")
        finally:
            # Закрываем соединение с клиентом
            client_socket.close()
            print(f"Соединение с {client_address} закрыто")

    try:
        while True:
            # Принимаем соединение от клиента
            client_socket, client_address = server_socket.accept()

            # Обрабатываем клиента в отдельном потоке (для поддержки нескольких подключений)
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address)
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\nСервер остановлен пользователем")
    finally:
        server_socket.close()


if __name__ '__main__':
    tcp_users_server()
