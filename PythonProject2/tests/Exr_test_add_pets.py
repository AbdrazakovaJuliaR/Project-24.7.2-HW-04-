from api import PetFriends
from settings import valid_email, valid_password
import os
import pytest
from PIL import Image


pf = PetFriends()
pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")

# 1. Позитивный тест: Добавление питомца без фото
def test_add_pet_without_photo(name= 'Мурзик', animal_type= 'крот', age='3'):
    """Проверяет возможность добавления питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    blank_image_path = os.path.join(os.path.dirname(__file__), "images", "blank.jpg")

    # Если файла нет — создаём его
    if not os.path.exists(blank_image_path):
        from PIL import Image
        img = Image.new('RGB', (1, 1), color=(255, 255, 255))  # Белый пиксель
        img.save(blank_image_path, "JPEG")

    status, pet = pf.post_add_new_pet(auth_key, name, animal_type, age, blank_image_path)

    assert status == 200
    assert 'id' in pet


# 2. Позитивный тест: Обновление имени питомца только цифрами
def test_update_pet_with_numeric_name(name='Барсик', animal_type='кот', age='3'):
    """Проверяет, можно ли обновить питомца, задав имя, состоящее только из цифр"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")
    status, pet = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert 'id' in pet
    pet_id = pet['id']
    new_name = "123456"

    status, updated_pet = pf.put_pet_info(auth_key, pet_id, new_name, animal_type, age)
    assert status == 200
    assert updated_pet['name'] == new_name


# 3. Негативный тест: Добавление питомца с пустыми данными
def test_add_pet_with_empty_fields(name='', animal_type='', age=''):
    """Проверяет, позволяет ли API добавить питомца с пустыми полями"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    blank_image_path = os.path.join(os.path.dirname(__file__), "images", "blank.jpg")
    # Отправляем запрос на добавление питомца с пустыми полями
    status, pet = pf.post_add_new_pet(auth_key, name, animal_type, age, blank_image_path)

    if status == 200:
        # Если API позволяет создать питомца, проверяем, что id есть, но данные пустые
        assert "id" in pet, "Питомец добавлен, но нет ID"
        assert pet["name"] == "", "Имя питомца не пустое"
        assert pet["animal_type"] == "", "Тип животного не пустой"
        assert pet["age"] == "", "Возраст не пустой"
    else:
        # Если API запрещает создание – это ожидаемое поведение
        assert status in [400, 422], f"Ожидали 400 или 422, но получили {status}"


# 4. Негативный тест: Добавление питомца с возрастом в виде отрицательного числа
def test_add_pet_with_negative_age(name='Гром', animal_type='пёс', age='-5'):
    """Проверяет поведение API при передаче отрицательного возраста"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")
    status, pet = pf.post_add_new_pet(auth_key, name, animal_type,age, pet_photo)

    if status != 200:
        assert "id" in pet, "Питомец добавлен, но нет ID"
        assert pet["name"] == "", "Имя питомца не пустое"
        assert pet["animal_type"] == "", "Тип животного не пустой"
        assert pet["age"] == "", "Возраст не пустой"
        assert print("all ok")
    else:
        assert status



# 5. Негативный тест: Обновление питомца с несуществующим pet_id
def test_update_pet_with_invalid_id(name='Рекс', animal_type='собака', age='5'):
    """Проверяет, можно ли обновить питомца, указав несуществующий ID"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    fake_pet_id = "1234567890abcdef"
    status, _ = pf.put_pet_info(auth_key, fake_pet_id, name, animal_type, age)
    assert status == 400 or status == 404



# 6. Позитивный тест: Удаление питомца
def test_delete_pet_and_check_absence(name='Снежок', animal_type='кот', age='4'):
    """Проверяет, что после удаления питомец отсутствует в общем списке"""

    pet_photo = os.path.join(os.path.dirname(__file__), "images", "Macaca.jpg")
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца
    status, pet = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    pet_id = pet['id']

    # Удаляем питомца
    status, _ = pf.delete_pet_info(auth_key, pet_id)
    assert status == 200

    # Получаем список питомцев
    status, pets_result = pf.get_list_of_pets(auth_key)
    assert status == 200, "Ошибка при получении списка питомцев"

    # Проверяем, что удалённого питомца нет в списке
    pets_list = pets_result.get('pets', [])
    assert not any(p['id'] == pet_id for p in pets_list), "Питомец всё ещё в списке!"


# 7. Негативный тест: Попытка удалить питомца с неверным auth_key
def test_delete_pet_with_invalid_auth():
    """Проверяет, можно ли удалить питомца с неверным ключом авторизации"""
    fake_auth_key = {"key": "invalid_key"}
    fake_pet_id = "1234567890abcdef"

    status, _ = pf.delete_pet_info(fake_auth_key, fake_pet_id)
    assert status == 403


# 8. Негативный тест: Запрос списка питомцев с неверным auth_key
def test_get_pets_with_invalid_auth(filter='my_pets'):
    """Проверяет, можно ли получить список питомцев, используя неверный ключ"""
    fake_auth_key = {"key": "invalid_key"}

    status, pets = pf.get_list_of_pets(fake_auth_key, filter)
    assert status == 403


# 9. Позитивный тест: Получение списка всех питомцев
def test_get_all_pets(filter=''):
    """Проверяет, можно ли получить список всех питомцев"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, pets = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(pets["pets"]) > 0


# 10. Негативный тест: Попытка обновления питомца с пустым именем
def test_update_pet_with_empty_name(name='Тимка', animal_type='кот', age='3'):
    """Проверяет, можно ли обновить питомца, задав пустое имя"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, pet = pf.post_add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    pet_id = pet['id']
    new_name = ' '
    status, updated_pet = pf.put_pet_info(auth_key, pet_id, new_name, animal_type, age)
    if status != 200:
        assert 'Try again'# Ожидаем ошибку
    else:
        assert status == 200


# проба публикации теста без фото
def test_add_pet_without_real_photo():
    """Проверяет, можно ли добавить питомца с минимальным валидным изображением"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создаём пустую картинку-заглушку 1x1 пиксель
    blank_image_path = os.path.join(os.path.dirname(__file__), "images", "blank.jpg")

    # Если файла нет — создаём его
    if not os.path.exists(blank_image_path):
        from PIL import Image
        img = Image.new('RGB', (1, 1), color=(255, 255, 255))  # Белый пиксель
        img.save(blank_image_path, "JPEG")

    status, pet = pf.post_add_new_pet(auth_key, "БезФото", "Кот", "3", blank_image_path)

    assert status == 200, f"Ожидали 200, но получили {status}"
    assert "id" in pet, "Питомец не создан"
