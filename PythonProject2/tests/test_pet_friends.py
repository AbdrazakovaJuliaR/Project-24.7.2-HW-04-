from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email,valid_password)
    status, result = pf.get_list_of_pets(auth_key,filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_add_new_pet(name='Барсик', animal_type='кот', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем абсолютный путь к файлу Macaca.jpg
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")

    status, result = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200, "Ошибка: Неверный статус код"
    assert result['name'] == name, "Ошибка: Имя питомца не совпадает"

def test_put_pet_info(name='Барсик', animal_type='кот', age='3'):
    """Проверяет обновление информации о питомце"""

    # Сначала добавляем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")
    status, pet = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert 'id' in pet

    # Обновляем данные питомца
    pet_id = pet['id']
    new_name = "НовоеИмя"
    new_animal_type = "лабрадор"
    new_age = "4"

    status, updated_pet = pf.put_pet_info(auth_key, pet_id, new_name, new_animal_type, new_age)

    assert status == 200
    assert updated_pet['name'] == new_name
    assert updated_pet['animal_type'] == new_animal_type
    assert updated_pet['age'] == new_age

def test_delete_pet():
    """Проверяет удаление питомца из базы"""

    # Сначала добавляем питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")
    status, pet = pf.post_add_new_pet(auth_key, "Барсик", "кот", "3", pet_photo)

    assert status == 200
    assert 'id' in pet

    pet_id = pet['id']

    # Удаляем питомца
    status, _ = pf.delete_pet_info(auth_key, pet_id)
    assert status == 200

    # Проверяем, что питомец удален — получаем список питомцев и убеждаемся, что его там нет
    status, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in [p['id'] for p in my_pets['pets']]

    #для метода с неправильным паролем можно использовать рандом рандинт, но изначально его необходимо импортировать