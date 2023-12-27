import allure


class TestApiExam:
    url_base = 'https://petstore.swagger.io/v2'

    def setup_class(self):
        self.obj = None
        self.add_url = '/pet'
        self.get_url = '/pet/findByStatus'
        self.get_id_url = '/pet/92854776000'

    @allure.title('Creating')
    @allure.description('Check adding a new pet')
    def test_post_request(self, check_add_pet):
        """with allure.step('Check status code'):
            assert check_add_pet.connect_add_pet_invalid(self.add_url) == 405, "Wrong response"""
        with allure.step('Check status code'):
            assert check_add_pet.connect_add_pet(self.add_url) == 200, "Wrong response"
        with allure.step('Validate model'):
            obj = check_add_pet.validate_model()
            assert obj[0], obj[1]

    @allure.title('Updating')
    @allure.description('Check updating a pet')
    def test_put_request(self, check_put_pet):
        with allure.step('Check status code'):
            assert check_put_pet.connect_put_pet(self.add_url) == 200, "Wrong response"
        with allure.step('Validate model'):
            obj = check_put_pet.validate_model()
            assert obj[0], obj[1]

    @allure.title('Finds Pets by status')
    @allure.description('Multiple status values can be provided with comma separated strings')
    def test_get_request(self, check_get_pet):
        with allure.step('Check status code'):
            assert check_get_pet.connect_get_pet(self.get_url) == 200, "Unsuccessful response"
        with allure.step('Check data structure'):
            obj = check_get_pet.validate_model()
            assert obj[0], obj[1]
        '''with allure.step('Check invalid get request'):
            assert check_get_pet.connect_get_pet_invalid(self.get_url) == 400, "It should fail"'''
        with allure.step('Check data structure'):
            obj = check_get_pet.validate_model()
            assert obj[0], obj[1]

    @allure.title('Finds Pets by Id')
    @allure.description('Find Pet by Id')
    def test_get_pet_id(self, check_get_pet):
        with allure.step('Check status code'):
            assert check_get_pet.connect_get_pet(self.get_id_url) == 200, "Pet not found"
        with allure.step('Check data structure'):
            obj = check_get_pet.validate_model()
            assert obj[0], obj[1]
        with allure.step('Check if there is no such id'):
            assert check_get_pet.connect_get_pet(self.get_id_url + '2') == 404, "Pet should be not found"

    @allure.title('Updating')
    @allure.description('Updates a pet in the store form data')
    def test_update_pet_by_id(self, check_add_pet):
        with allure.step('Check status code'):
            assert check_add_pet.connect_update_pet(self.get_id_url) == 200, "Invalid input"

    @allure.title('Deleting')
    @allure.description('Checks deleting a pet by id')
    def test_delete(self, check_deleting_pet):
        with allure.step('Check status code'):
            assert check_deleting_pet.delete_pet(self.get_id_url) == 400, "Valid ID supplied"
