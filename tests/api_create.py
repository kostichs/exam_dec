import random

import requests
from pydantic import BaseModel, ValidationError, field_validator
from enum import Enum
from typing import Union, Optional


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
    status: Union[PetEnum]


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
        """Connects to the server by id"""
        self.body["id"] = _id
        self.response = requests.post(self.url + url, json=self.body)
        return self.response.status_code

    def validate_model(self, is_list: bool):
        """Validates response.json according to the documentation Body.
        There can be a piece of Pet data or list of Pet objects.
        Validation of the list of Pets doesn't work at me, so, it is used here only one of the elements of the list"""
        if is_list:
            element = random.randint(0, len(self.response.json())-1)
            jsondata = self.response.json()[element]
        else:
            jsondata = self.response.json()
        try:
            Pet.model_validate(jsondata)
        except AssertionError as e:
            return False, e
        except ValidationError as e:
            return False, e
        else:
            return True, None

    def validate_model_pets(self):
        """Внимание: здесь проблема, не получилось сделать проверку на список Pet, все время провал.
        Поэтому я беру просто первый элемент этого списка для каждого статуса"""
        for el in range(len(self.response.json())):
            try:
                Pet.model_validate(self.response.json()[el])
            except AssertionError as e:
                return False, e
            except ValidationError as e:
                return False, e
            else:
                continue
        return True, None

    def change(self, url: str, _id: int, name: str):
        """Using requests.put to change the pet data"""
        self.body["id"] = _id
        self.body["name"] = name
        self.response = requests.put(self.url + url, json=self.body)
        return self.response.status_code

    def get_pet_status(self, url: str, status: str):
        """Looks for pet by status: available, pending or sold"""
        self.response = requests.get(self.url + url + '?status=' + status)
        # r'https://petstore.swagger.io/v2/pet/findByStatus?status=available'
        return self.response.status_code

    def get_pet_id(self, url: str, _id: str):
        """Looks for pet by id"""
        self.response = requests.get(f'{self.url}{url}{_id}')
        return self.response.status_code

    def post_by_id(self, url: str, _id: str, status: str, name: str):
        """Change pet datas by id"""
        self.body["status"] = status
        self.body["name"] = name
        self.response = requests.post(f'{self.url}{url}{_id}', json=self.body)
        print(self.response.json())
        return self.response.status_code

    def delete_by_id(self, url: str, _id) -> int:
        """Deletes pet by id"""
        self.response = requests.delete(f'{self.url}{url}{_id}')
        return self.response.status_code

    '''def validate_post_by_id(self) -> Union[bool, Any]:
            """It doesn't work. According to the documentation, this post request should return a body with 3 fields.
            However, I could not deal with it"""
        try:
            UpdBody.model_validate(self.response.json())
        except AssertionError as e:
            return False, e
        else:
            return True, None
    '''
