import pytest
from api_pet import ApiPet


@pytest.fixture(scope="function")
def create_pet_object(request):
    pet = ApiPet(request.cls.url_base)
    yield pet

