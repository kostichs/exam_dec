import pytest
from api_create import ApiPet


@pytest.fixture(scope="function")
def create_pet_object(request):
    pet = ApiPet(request.cls.url_base)
    yield pet






@pytest.fixture
def check_add_pet(request):
    pet = ApiPet(request.cls.url_base)
    yield pet

'''
@pytest.fixture
def add_pet(request, check_add_pet):
    return check_add_pet.connect(request.cls.add_url)
'''

@pytest.fixture
def check_put_pet(request):
    pet = ApiPet(request.cls.url_base)
    yield pet


@pytest.fixture
def check_get_pet(request):
    pet = ApiPet(request.cls.url_base)
    yield pet


@pytest.fixture
def check_deleting_pet(request):
    pet = ApiPet(request.cls.url_base)
    yield pet
