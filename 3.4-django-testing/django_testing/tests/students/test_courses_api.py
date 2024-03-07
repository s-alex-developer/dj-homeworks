import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture()
def courses_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_retrieve_courses(api_client, courses_factory,):

    """ Проверка получения первого курса (retrieve-логика) """

    # Arrange
    course = courses_factory(_quantity=1)
    course_id = course[0].id

    # Act
    response = api_client.get(f"/api/v1/courses/{course_id}/")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data['id'] == course_id


@pytest.mark.django_db
def test_list_courses(api_client, courses_factory):

    """ Проверка получения списка курсов (list-логика) """

    # Arrange
    quantity = 3
    courses = courses_factory(_quantity=quantity)

    # Act
    response = api_client.get("/api/v1/courses/")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data[0]['id'] == courses[0].id
    assert data[quantity-1]['name'] == courses[quantity-1].name
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_courses_filter_id(api_client, courses_factory):

    """ Проверка фильтрации списка курсов по id """

    # Arrange
    course = courses_factory(_quantity=1)
    course_id = course[0].id

    # Act
    response = api_client.get(f"/api/v1/courses/?id={course_id}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data[0]['id'] == course_id


@pytest.mark.django_db
def test_courses_filter_name(api_client, courses_factory):

    """ Проверка фильтрации списка курсов по name """

    # Arrange
    course = courses_factory(_quantity=1)
    course_name = course[0].name

    # Act
    response = api_client.get(f"/api/v1/courses/?name={course_name}")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data[0]['name'] == course[0].name


@pytest.mark.django_db
def test_course_create(api_client):

    """ Tест успешного создания курса """

    # Arrange
    course_name = "Тестовый курс: POST-запроса к API"

    # Act
    response = api_client.post('/api/v1/courses/',
                               data={'name': course_name},
                               format='json')
    last_added_course = Course.objects.last()

    # Assert
    assert response.status_code == 201
    assert response.data['name'] == last_added_course.name


@pytest.mark.django_db
def test_course_update(api_client, courses_factory):

    """ Тест успешного обновления курса """

    # Arrange
    course = courses_factory(_quantity=1)

    course_id = course[0].id
    start_name = course[0].name
    new_name = "Тестовый курс: PATCH-запроса к API"

    # Act
    response = api_client.patch(f'/api/v1/courses/{course_id}/',
                                data={'name': new_name},
                                format='json')
    # Assert
    assert response.status_code == 200
    assert response.data['name'] == new_name
    assert response.data['name'] != start_name


@pytest.mark.django_db
def test_course_delete(api_client, courses_factory):

    """ Тест успешного удаления курса """

    # Arrange
    course = courses_factory(_quantity=1)
    course_id = course[0].id

    # Act
    delete_response = api_client.delete(f'/api/v1/courses/{course_id}/',
                                        format='json')

    # Assert
    assert delete_response.status_code == 204
    assert len(Course.objects.filter(pk=course_id)) == 0


# <<<<<<<<<<<<<<<<<<< ДОПОЛНИТЕЛЬНОЕ ЗАДАНИЕ >>>>>>>>>>>>>>>>>>>> #

@pytest.mark.parametrize(
    'students_count,status_code', [
        (19, 201),
        (20, 201),
        (21, 400)
    ]
)
@pytest.mark.django_db
def test_max_students_at_course(client, students_factory, students_count, status_code):

    # Arrange
    students = students_factory(_quantity=students_count)
    student_ids = [stud.id for stud in students]
    data = {"name": 'Test', "students": student_ids}
    response = client.post('/api/v1/courses/', data=data)
    assert response.status_code == status_code