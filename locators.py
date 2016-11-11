from selenium.webdriver.common.by import By


class LoginPageLocators(object):

	USERNAME = (By.CSS_SELECTOR, '#user_login')
	PASSWORD = (By.CSS_SELECTOR, '#user_pass')
	SUBMIT = (By.CSS_SELECTOR, '#wp-submit')

class AdminPageLocators(object):

	H1 = (By.CSS_SELECTOR, ".wrap>h1")

class MainPageLocators(object):

	ENTRY_TITLE = (By.CSS_SELECTOR, ".entry-title")