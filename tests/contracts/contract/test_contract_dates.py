import pytest
from rest_framework.test import APIClient

from contracts.models import Contract

from utils.date_util import DateUtils

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

@pytest.mark.django_db
class TestContractEndpoint:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.user_dict = dicts_test_utils.university_user_dict_1

        self.university = create_objects_test_utils.create_test_university(self.university_dict)
        self.user = create_objects_test_utils.create_test_university_user(self.user_dict, self.university)

        self.client = APIClient()
        self.client.login(
            email = self.user_dict['email'], 
            password = self.user_dict['password'])

        self.consumer_unit_test_dict = dicts_test_utils.consumer_unit_dict_1
        self.consumer_unit_test = create_objects_test_utils.create_test_consumer_unit(self.consumer_unit_test_dict, self.university)
        
        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

        self.contract_test_1_dict = dicts_test_utils.contract_dict_1
        self.contract_test_2_dict = dicts_test_utils.contract_dict_2
        self.contract_test_3_dict = dicts_test_utils.contract_dict_3
        self.contract_test_4_dict = dicts_test_utils.contract_dict_4

        self.contract_test_1 = create_objects_test_utils.create_test_contract(self.contract_test_1_dict, self.distributor, self.consumer_unit_test)
        self.contract_test_2 = create_objects_test_utils.create_test_contract(self.contract_test_2_dict, self.distributor, self.consumer_unit_test)
        self.contract_test_3 = create_objects_test_utils.create_test_contract(self.contract_test_3_dict, self.distributor, self.consumer_unit_test)
        self.contract_test_4 = create_objects_test_utils.create_test_contract(self.contract_test_4_dict, self.distributor, self.consumer_unit_test)


    def test_create_contract_and_set_last_contract_end_date_1(self):
        end_date = DateUtils.get_yesterday_date(self.contract_test_2.start_date)

        contract_test_1 = Contract.objects.get(id = self.contract_test_1.id)

        assert contract_test_1.end_date == end_date

    def test_create_contract_and_set_last_contract_end_date_2(self):
        end_date = DateUtils.get_yesterday_date(self.contract_test_3.start_date)

        contract_test_2 = Contract.objects.get(id = self.contract_test_2.id)

        assert contract_test_2.end_date == end_date

    def test_create_contract_and_set_last_contract_end_date_3(self):
        end_date = DateUtils.get_yesterday_date(self.contract_test_4.start_date)

        contract_test_3 = Contract.objects.get(id = self.contract_test_3.id)

        assert contract_test_3.end_date == end_date

    def test_throws_exception_create_contract_with_start_date_not_valid(self):
        with pytest.raises(Exception) as e:
            contract_test_6_dict = dicts_test_utils.contract_dict_6
            create_objects_test_utils.create_test_contract(contract_test_6_dict, self.distributor, self.consumer_unit_test)

        assert 'Already have the contract in this date' in str(e.value)