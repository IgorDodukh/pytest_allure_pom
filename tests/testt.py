import allure
import pytest


@allure.testcase('TestCase functions')
def test_minor():
    assert True


class TestBar:

    def test_bar(self):
        pass


@pytest.fixture(scope="function")
def resource_setup(request):
    print("\nconnect to db")
    db = {"Red": 1, "Blue": 2, "Green": 3}

    def resource_teardown():
        print("\ndisconnect")

    request.addfinalizer(resource_teardown)
    return db


@allure.step('My step 1')
def test_db(resource_setup):
    for k in resource_setup.keys():
        print("color {0} has id {1}".format(k, resource_setup[k]))


@allure.step('My step 2')
def test_red(resource_setup):
    assert resource_setup["Red"] == 1


@allure.step('My step 3')
def test_blue(resource_setup):
    assert resource_setup["Blue"] != 1