import allure


@allure.severity(allure.severity_level.MINOR)
def test_minor():
    assert False


@allure.severity(allure.severity_level.CRITICAL)
class TestBar:

    # will have CRITICAL priority
    def test_bar(self):
        pass

    # will have BLOCKER priority via a short-cut decorator
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bar(self):
        pass