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
        username = driver.find_element_by_name('username')
        username.send_keys('tom_1')
        # locate password box
        password = driver.find_element_by_name('password')
        password.send_keys('password_2')
        # locate email box
        email = driver.find_element_by_name('email')
        email.send_keys('tom3@gmail.com')       
        # submit the form
        submit_button = driver.find_element_by_id('submit_button')
        submit_button.click()

        # check that we successfully returned to the homepage
        self.assertEqual('Homepage', driver.title)

    def test_login_success(self):
        driver = self.driver
        # test login with correct info
        # get homepage and assert success
        driver.get('http://web:8000')
        self.assertEqual('Homepage', driver.title)

        driver.get('http://web:8000/login/')
        self.assertEqual('Login', driver.title)
        # navigate to create account page and assert success
        driver.get('http://web:8000/create_account/')
        self.assertEqual('Sign up', driver.title)
        
        # create a sample account

        # locate username box
        username = driver.find_element_by_name('username')
        username.send_keys('tomsobolik')
        # locate password box
        password = driver.find_element_by_name('password')
        password.send_keys('booty')
        # locate email box
        email = driver.find_element_by_name('email')
        email.send_keys('tomsobolikrocks@gmail.com')       
        # submit the form
        submit_button = driver.find_element_by_id('submit_button')
        submit_button.click()

        # log into the new acccount

        # navigate to login page and assert success
        driver.get('http://web:8000/login/')
        self.assertEqual('Login', driver.title)

        # locate username box
        username_box = driver.find_element_by_name('username')
        username_box.send_keys('tomsobolik')
        # locate password box
        password_box = driver.find_element_by_name('password')
        password_box.send_keys('booty')      
        # submit the form
        button = driver.find_element_by_id('loginButton')
        button.click()

        # check that we logged in by seeing if the login button changed
        assert "Log out" in driver.page_source

    def test_login_incorrectInput(self):
        driver = self.driver
        driver.get('http://web:8000/')
        # navigate to login page and assert success
        driver.get('http://web:8000/login/')
        # test login with incorrect info

        # locate username box
        username = driver.find_element_by_name('username')
        username.send_keys('faskdjfaskdjf')
        # locate password box
        password = driver.find_element_by_name('password')
        password.send_keys('faiesudiewafig4')      
        # submit the form
        submit_button = driver.find_element_by_id('loginButton')
        submit_button.click()

        # check that login request was denied
        self.assertEqual('Login', driver.title)

    def test_create_listing(self):
        driver = self.driver
        driver.get('http://web:8000/')
        driver.get('http://web:8000/login')
        driver.get('http://web:8000/create_account')

        # create an account
        username = driver.find_element_by_name('username')
        username.send_keys('tom')
        # locate password box
        password = driver.find_element_by_name('password')
        password.send_keys('password')
        # locate email box
        email = driver.find_element_by_name('email')
        email.send_keys('tom@gmail.com')       
        # submit the form
        submit_button = driver.find_element_by_id('submit_button')
        submit_button.click()

        # navigate to create listing page
        driver.get('http://web:8000/create_listing')
        # submit form data
        name = driver.find_element_by_name('sample_name')
        name.send_keys('newPack1')

        description = driver.find_element_by_name('sample_description')
        description.send_keys('sample pack description')

        price = driver.find_element_by_name('price')
        price.send_keys(1)

        submit_button = driver.find_element_by_id('submitNewListing')
        submit_button.click()

        assert "Your pack was successfully added!" in driver.page_source

    def tearDown(self):
        self.driver.close()
        
if __name__ == "__main__":
    time.sleep(15)
    unittest.main()
