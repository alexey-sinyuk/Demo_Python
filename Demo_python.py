import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import page
import argparse

argparser = argparse.ArgumentParser(description='Use a profile if set')
argparser.add_argument('-p', choices=['chrome_local','chrome_remote','firefox_local', 'firefox_remote'])
args = argparser.parse_args()
profile = args.p

local_grid = 'http://127.0.0.1:4444/wd/hub'
remote_grid = 'http://qa-u1604.vlab.lohika.com:4444/wd/hub'
base_url = 'http://qa-u1604.vlab.lohika.com:8080/wp-login.php'

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

class BaseTest(unittest.TestCase):

	def setUp(self):
		print ("setup ran")
		for case in switch(profile):
		    if case('chrome_local'):
		        self.driver = webdriver.Remote(
		        	command_executor=local_grid,
		        	desired_capabilities=DesiredCapabilities.CHROME)
		        break
		    if case('firefox_local'):
		        self.driver = webdriver.Remote(
		        	command_executor=local_grid,
		        	desired_capabilities=DesiredCapabilities.FIREFOX)
		        break
		    if case('chrome_remote'):
		        self.driver = webdriver.Remote(
		        	command_executor=remote_grid,
		        	desired_capabilities=DesiredCapabilities.CHROME)
		        break		        
		    if case('firefox_remote'):
		        self.driver = webdriver.Remote(
		        	command_executor=remote_grid,
		        	desired_capabilities=DesiredCapabilities.FIREFOX)
		        break
		    if case():
		        self.driver = webdriver.Remote(
		        	command_executor='http://127.0.0.1:4444/wd/hub',
		        	desired_capabilities=DesiredCapabilities.CHROME)
		
		self.driver.implicitly_wait(10)

	def tearDown(self):
		print ("tearDown ran")
		self.driver.close()

	@staticmethod
	def setUpClass():
		print ("setUpClass")

	@staticmethod
	def tearDownClass():
		print ("tearDownClass")

	def setUpModule(self):
		print ("setUpModule")

class LoginFlowTests(BaseTest):

	def test_admin_login(self):
		driver = self.driver
		login_page = page.LoginPage(driver)
		admin_page = page.AdminPage(driver)
		login_page.to(base_url)
		login_page.login_as("admin_as", "P@ssw0rd")
		assert admin_page.at(), "Not logged into Dashboard"

	def test_viewer_login(self):
		driver = self.driver
		login_page = page.LoginPage(driver)
		main_page = page.MainPage(driver)
		login_page.to(base_url)
		login_page.login_as("viewer_as", "P@ssw0rd")
		assert main_page.at(), "Not logged into shop"

	def test_cookie(self):
		driver = self.driver
		driver.get("http://www.google.com");
		# Now set the cookie. This one's valid for the entire domain
		#cookie = {"key": "value"}
		#driver.add_cookie(cookie)
		driver.add_cookie({'name' : 'foo', 'value' : 'bar', 'secure' : False})

		# And now output all the available cookies for the current URL
		all_cookies = driver.get_cookies()
		for cookie_name, cookie_value in all_cookies[0].items():
			print ("%s -> %s", cookie_name, cookie_value)


if __name__ == "__main__":	
	suite = unittest.TestLoader().loadTestsFromTestCase(LoginFlowTests)
	runner = unittest.TextTestRunner()
	runner.run(suite)
