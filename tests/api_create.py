import requests
from pydantic import BaseModel, ValidationError, field_validator
import samples
from typing import Union
from enum import Enum, IntEnum


class PetEnum(Enum):
    available: 'available'
    pending: 'pending'
    sold: 'sold'


class Pet(BaseModel):
    id: int
    category: dict[str, Union[int, str]]
    name: str
    photoUrls: list[str]
    tags: list[dict[str, Union[int, str]]]
    status: str

    '''@field_validator("status")
    @classmethod
    def check_status(cls, value):
        if value == PetEnum.available or \
                value == PetEnum.pending or \
                value == PetEnum.sold:
            return value'''


class ApiPet:
    def __init__(self, url):
        self.url = url
        self.response = None

    def connect_add_pet(self, url):
        self.response = requests.post(self.url + url, json=samples.valid_sample_add)
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

    def validate_model(self):
        try:
            Pet.model_validate(self.response.json())
        except AssertionError as e:
            return False, e
        except ValidationError as e:
            return False, e
        else:
            return True, None

    def connect_get_pet(self, url):
        self.response = requests.get(self.url + url)
        return self.response.status_code

    def delete_pet(self, url):
        self.response = requests.delete(self.url + url)
        return self.response.status_code
