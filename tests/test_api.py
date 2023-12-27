import allure
import pytest


class TestApiExam:
    url_base = 'https://petstore.swagger.io/v2'

    def setup_class(self):
        self.obj = None
        self.add_url = '/pet'
        self.url_status = '/pet/findByStatus'
        self.get_id_url = '/pet/'

    @allure.title("Connection to add new pet")
    @allure.description("Check connection response and validate data structure with several parameters")
    @pytest.mark.parametrize("_id", [0, 1, 4, -33333, 32, 34])
    def test_create_pet(self, create_pet_object, _id):
        with allure.step('Check status code'):
            assert create_pet_object.connect(self.add_url, _id) == 200, "Invalid connection response"
        with allure.step('Check data structure'):
            response = create_pet_object.validate_model()
            assert response[0], response[1]

    @allure.title("Connection to update an existing pet")
    @allure.description("Check connection response and validate data structure")
    @pytest.mark.parametrize("_id, name", [(21321351, "aaaaa"), (1, "bbbb"), (22222, "ddddef"), (-33333, "zzzzz"),
                                           (44444, 'sergey'), (43987743589, "valera")])
    def test_change_pet(self, create_pet_object, _id, name):
        with allure.step('Check status code'):
            assert create_pet_object.change(self.add_url, _id, name) == 200, "Invalid connection response"
        with allure.step('Check data structure'):
            response = create_pet_object.validate_model()
            assert response[0], response[1]

    @allure.title("Connection to find pets by status")
    @allure.description("Check connection response and validate data structure")
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_get_pet_by_status(self, create_pet_object, status):
        with allure.step("check status code"):
            assert create_pet_object.get_pet_status(self.url_status, status) == 200, "Invalid connection response"
        with allure.step('Check data structure'):
            response = create_pet_object.validate_model_pets()
            assert response[0], response[1]

    @allure.title("Connection to find pets by id")
    @allure.description("Check valid response and validate data structure")
    @pytest.mark.parametrize("_id", [22222, 44444, 43987743589])
    def test_get_pet_by_id(self, create_pet_object, _id):
        with allure.step("check status code"):
            assert create_pet_object.get_pet_id(self.get_id_url, str(_id)) == 200, "Invalid connection response"
        with allure.step('Check data structure'):
            response = create_pet_object.validate_model()
            assert response[0], response[1]

    @allure.title("Connection to find pets by invalid id")
    @allure.description("Check relevant response and validate data structure")
    @pytest.mark.xfail
    @pytest.mark.parametrize("_id", [0, -222, 0000, -1])
    def test_get_by_invalid_id(self, create_pet_object, _id):
        with allure.step("check status code"):
            assert create_pet_object.get_pet_id(self.get_id_url, str(_id)) == 200, f'{_id} does not exist'

    @allure.title("Updates a pet in the store with form data")
    @allure.description("Check relevant response and validate data structure")
    @pytest.mark.parametrize("_id", [4, 32, 34])
    def test_update_pet_by_id(self, create_pet_object, _id):
        with allure.step('Check status code'):
            assert create_pet_object.get_pet_id(self.get_id_url, str(_id)) == 200, f'{_id} does not exist'
        with allure.step('Validation response data structure'):
            response = create_pet_object.validate_model()
            assert response[0], response[1]

    @allure.title("Delete a pet from the store")
    @allure.description("Check relevant response")
    @pytest.mark.parametrize("_id", [4, 32, 34])
    def test_delete_by_id(self, create_pet_object, _id):
        with allure.step('Check status code'):
            assert create_pet_object.delete_by_id(self.get_id_url, str(_id)) == 200, f'{_id} does not exist'

    @allure.title("Delete a pet from the store")
    @allure.description("Check relevant response")
    @pytest.mark.xfail(strict=True)
    @pytest.mark.parametrize("_id", [4, 32, 34])
    def test_delete_non_existed_pet(self, create_pet_object, _id):
        with allure.step('Check status code'):
            assert create_pet_object.delete_by_id(self.get_id_url, str(_id)) == 200, f'{_id} still exists'

