from clients.courses.courses_client import (
    CoursesClient,
    get_courses_client,
    CourseSchema,
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
)

__all__ = [
    'CoursesClient',
    'get_courses_client',
    'CourseSchema',
    'CreateCourseRequestDict',
    'CreateCourseResponseDict',
]
