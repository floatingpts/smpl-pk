from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import unittest

# Helpful resource: https://selenium-python.readthedocs.io/getting-started.html#using-selenium-with-remote-webdriver


class Integration(unittest.TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']
    
    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://selenium-chrome:4444/', desired_capabilities=DesiredCapabilities.CHROME)
    
    def test_search(self):
        driver = self.driver
        # Pull up home page
        driver.get('http://localhost:8000/')
        # Check that we are on home page
        self.assertEqual('Homepage', driver.title)
        # Submit search
        search_form = driver.find_element_by_id('search_form')
        search_form.clear()
        search_form.send_keys('Piano')
        search_form.submit()
        # Check that 'Piano sound effects' in results
        assert "Piano sound effects" in driver.page_source
        
    def tearDown(self):
        self.driver.close()
        
if __name__ == "__main__":
    unittest.main()


