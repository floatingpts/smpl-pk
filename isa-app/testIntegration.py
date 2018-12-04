from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Integration(unittest.TestCase):
    # Test fixtures loaded here.
    fixtures = ['test_fixture.json']
    
    def setUp(self):
        self.driver = webDriver.Chrome()
    
    def test_search(self):
        driver = test.driver
        # Pull up home page
        driver.get('https://')
        # Submit search
        search_form = driver.find_element_by_id('search_form')
        search_form.clear()
        search_form.send_keys('Piano')
        search_form.submit()
        
    def tearDown(self):
        self.driver.close()
