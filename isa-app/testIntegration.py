from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest
import time

# Helpful resource: https://selenium-python.readthedocs.io/getting-started.html#using-selenium-with-remote-webdriver


class Integration(unittest.TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']
    
    def setUp(self):
        self.driver = webdriver.Remote('http://selenium-chrome:4444/wd/hub', desired_capabilities=DesiredCapabilities.CHROME)
    
    def test_search(self):
        driver = self.driver
        # Pull up home page
        driver.get('http://web:8000/')
        # Check that we are on home page
        self.assertEqual('Homepage', driver.title)
        # Submit search
        search_form = driver.find_element_by_id('search_box')
        search_form.clear()
        search_form.send_keys('Piano')
        search_form.submit()
        # Check that 'Piano sound effects' in results
        assert "Piano sound effects" in driver.page_source

    def test_signup(self):
        driver = self.driver
        # get homepage and assert success
        driver.get('http://web:8000')
        self.assertEqual('Homepage', driver.title)
        # navigate to login page and assert success
        driver.get('http://web:8000/login/')
        self.assertEqual('Login', driver.title)
        # navigate to create account page and assert success
        driver.get('http://web:8000/create_account/')
        self.assertEqual('Sign up', driver.title)
        
        # test call to create_account service with sample form data

        # locate username box
        signup_form = driver.find_element_by_name('username')
        signup_form.send_keys('tom')
        # locate password box
        signup_form = driver.find_element_by_name('password')
        signup_form.send_keys('password')
        # locate email box
        signup_form = driver.find_element_by_name('email')
        signup_form.send_keys('tom@gmail.com')       
        # submit the form
        signup_form.submit()

        # check that we successfully returned to the homepage
        self.assertEqual('Homepage', driver.title)

    def tearDown(self):
        self.driver.close()
        
if __name__ == "__main__":
    time.sleep(15)
    unittest.main()


