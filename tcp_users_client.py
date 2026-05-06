import socket


def tcp_users_client():
    """
    TCP-клиент, который отправляет сообщение серверу и получает историю
    """
    # Создаем TCP-сокет
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        server_address = ('localhost', 12345)
        client_socket.connect(server_address)
        print(f"Подключен к серверу {server_address[0]}:{server_address[1]}")

        # Отправляем сообщение серверу
        message = "Привет, сервер!"
        client_socket.send(message.encode())
        print(f"Отправлено сообщение: {message}")

        # Получаем ответ от сервера (всю историю)
        response = client_socket.recv(1024).decode()
        print(f"Ответ от сервера:\n{response}")

    except ConnectionRefusedError:
        print("Ошибка: Сервер не запущен. Пожалуйста, сначала запустите сервер.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Закрываем соединение
        client_socket.close()
        print("Соединение закрыто")


if __name__ "__main__":
    tcp_users_client()
    