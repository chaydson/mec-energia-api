import pytest

from tests.test_utils import dicts_test_utils
from tests.test_utils import create_objects_test_utils

@pytest.mark.django_db
class TestContractCreation:
    def setup_method(self):
        self.university_dict = dicts_test_utils.university_dict_1
        self.university = create_objects_test_utils.create_test_university(self.university_dict)

        self.distributor_dict = dicts_test_utils.distributor_dict_1
        self.distributor = create_objects_test_utils.create_test_distributor(self.distributor_dict, self.university)

        self.consumer_unit_test_dict = dicts_test_utils.consumer_unit_dict_1
        self.consumer_unit_test = create_objects_test_utils.create_test_consumer_unit(self.consumer_unit_test_dict, self.university)