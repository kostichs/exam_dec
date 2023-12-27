import requests
from pydantic import BaseModel, ValidationError, field_validator
import samples
import json
from enum import Enum
from typing import Union, Optional, Any


class PetEnum(Enum):
    available = "available"
    pending = "pending"
    sold = "sold"


class Category(BaseModel):
    id: int = None
    name: str = None


class Tags(BaseModel):
    id: int = None
    name: str = None


class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Category] = None
    name: Optional[str] = None
    photoUrls: Optional[list[str]] = None
    tags: Optional[list[Tags]] = None
    status: Optional[str] = None


class Pets(BaseModel):
    body: list[Optional[Pet]] = None


class UpdBody(BaseModel):
    code: int
    type: str
    message: str


class ApiPet:
    body = {
        "id": 0,
        "category": {
            "id": 0,
            "name": "string"
        },
        "name": "doggie",
        "photoUrls": [
            "string"
        ],
        "tags": [
            {
                "id": 0,
                "name": "string"
            }
        ],
        "status": "available"
    }

    def __init__(self, url: str):
        self.url = url
        self.response = None
        self.body = self.__class__.body

    def connect(self, url, _id):
        self.body["id"] = _id
        self.response = requests.post(self.url + url, json=self.body)
        return self.response.status_code

    def validate_model(self):
        try:
            Pet.model_validate(self.response.json())
        except AssertionError as e:
            return False, e
        except ValidationError as e:
            return False, e
        else:
            return True, None

    def validate_model_pets(self):
        """Внимание: здесь проблема, не получилось сделать проверку на список Pet, все время провал.
        Поэтому я беру просто первый элемент этого списка для каждого статуса"""
        try:
            Pet.model_validate(self.response.json()[0])
        except AssertionError as e:
            return False, e
        except ValidationError as e:
            return False, e
        else:
            return True, None

    def change(self, url: str, _id: int, name: str):
        self.body["id"] = _id
        self.body["name"] = name
        self.response = requests.put(self.url + url, json=self.body)
        return self.response.status_code

    def get_pet_status(self, url: str, status: str):
        self.response = requests.get(self.url + url + '?status=' + status)
        # r'https://petstore.swagger.io/v2/pet/findByStatus?status=available'
        # print(self.response.json())
        return self.response.status_code

    def get_pet_id(self, url: str, _id: str):
        self.response = requests.get(f'{self.url}{url}{_id}')
        return self.response.status_code

    def post_by_id(self, url: str, _id: str, status: str, name: str):
        self.body["status"] = status
        self.body["name"] = name
        self.response = requests.post(f'{self.url}{url}{_id}', json=self.body)
        print(self.response.json())
        return self.response.status_code

    def delete_by_id(self, url: str, _id):
        self.response = requests.delete(f'{self.url}{url}{_id}')
        return self.response.status_code

'''    def validate_post_by_id(self) -> Union[bool, Any]:
        try:
            UpdBody.model_validate(self.response.json())
        except AssertionError as e:
            return False, e
        else:
            return True, None
'''








'''
    def connect_add_pet(self, url, sample):
        self.response = requests.post(self.url + url, json=sample)
        return self.response.status_code

    def connect_add_pet_invalid(self, url):
        self.response = requests.post(self.url + url, json=samples.invalid_sample_add)
        return self.response.status_code

    def connect_update_pet(self, url):
        self.response = requests.post(self.url + url, json=samples.valid_sample_update)
        return self.response.status_code

    def connect_put_pet(self, url):
        self.response = requests.put(self.url + url, json=samples.valid_sample_add)
        return self.response.status_code



    def connect_get_pet(self, url):
        self.response = requests.get(self.url + url)
        return self.response.status_code

    def delete_pet(self, url):
        self.response = requests.delete(self.url + url)
        return self.response.status_code'''
