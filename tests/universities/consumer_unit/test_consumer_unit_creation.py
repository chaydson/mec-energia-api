import json
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

TESTSERVER_ADDR = 'http://testserver/api/universities/'
ENDPOINT = '/api/consumer-units/'

@pytest.mark.django_db
class TestConsumerUnitsEndpoint:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)
        
        self.client = APIClient()
        self.client.login(
            email = self.user_dict['email'], 
            password = self.user_dict['password'])

        self.consumer_unit_to_be_created = {
            'name': 'Faculdade do Gama',
            'code': '111111111',
            'created_on': '2022-10-02',
            'is_active': True,
            'university': self.university.id
        }


    def test_create_consumer_unit(self):
        response = self.client.post(ENDPOINT, self.consumer_unit_to_be_created)
        created_consumer_unit = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert created_consumer_unit['name'] == self.consumer_unit_to_be_created['name']
        assert created_consumer_unit['university'] == self.consumer_unit_to_be_created['university']