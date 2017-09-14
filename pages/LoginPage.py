
class LoginPage(object):

    def __init__(self, driver):
        self.driver = driver

    def UserName(self, user_name):
        self.driver.find_element_by_name("userName").clear()
        self.driver.find_element_by_name("userName").send_keys(user_name)

    def Password(self, password):
        self.driver.find_element_by_name("password").clear()
        self.driver.find_element_by_name("password").send_keys(password)

    def SignIn(self):
        self.driver.find_element_by_name("login").click()