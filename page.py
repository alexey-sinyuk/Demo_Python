from locators import *

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver

class LoginPage(BasePage):    

    def to(self, base_url):
        self.driver.get(base_url)

    def at(self):
        return "Log In" in self.driver.title

    def login_as(self, username, password):
        username_field = self.driver.find_element(*LoginPageLocators.USERNAME)
        password_field = self.driver.find_element(*LoginPageLocators.PASSWORD)
        submit_button = self.driver.find_element(*LoginPageLocators.SUBMIT)
        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()


class AdminPage(BasePage):

    def at(self):
        res = self.driver.find_element(*AdminPageLocators.H1).text
        return "Dashboard" in res

class MainPage(BasePage):

    def at(self):
        res = self.driver.find_element(*MainPageLocators.ENTRY_TITLE).text
        return "My account" in res