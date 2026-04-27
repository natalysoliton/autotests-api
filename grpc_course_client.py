import grpc

import course_service_pb2
import course_service_pb2_grpc


def main():
    # Устанавливаем соединение с сервером
    channel = grpc.insecure_channel('localhost:50051')
    stub = course_service_pb2_grpc.CourseServiceStub(channel)

    # Отправляем запрос
    request = course_service_pb2.GetCourseRequest(course_id="api-course")
    response = stub.GetCourse(request)

    # Выводим полученный ответ
    print(response)


if __name__ == "__main__":
    main()
