import allure
#
#
# @allure.severity(allure.severity_level.MINOR)
# def test_minor():
#     assert False
#
#
# @allure.severity(allure.severity_level.CRITICAL)
# class TestBar:
#
#     # will have CRITICAL priority
#     def test_bar(self):
#         pass
#
#     # will have BLOCKER priority via a short-cut decorator
#     @allure.severity(allure.severity_level.CRITICAL)
#     def test_bar(self):
#         pass

import pytest


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