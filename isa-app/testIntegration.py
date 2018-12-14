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

    def test_create_account(self):
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

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    time.sleep(15)
    unittest.main()
