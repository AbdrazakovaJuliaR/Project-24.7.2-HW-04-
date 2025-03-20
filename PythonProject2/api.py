import requests
import json

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def post_add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод отправляет POST-запрос на добавление нового питомца с фото"""

        headers = {'auth_key': auth_key['key']}

        # Открываем файл и формируем данные для запроса
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        files = {'pet_photo': open(pet_photo, 'rb')}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=files)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text

        return status, result



    def put_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет PUT-запрос для обновления информации о питомце"""

        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.put(self.base_url + f'api/pets/{pet_id}', headers=headers, data=data)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text

        return status, result

    def delete_pet_info(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет DELETE-запрос для удаления питомца"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + f'api/pets/{pet_id}', headers=headers)

        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text

        return status, result







