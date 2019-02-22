import typing, csv, contextlib, random
from selenium import webdriver
import string, random, time
from bs4 import BeautifulSoup as soup
import site_scraping_statuses, site_scraping_tests


#<a class="button button-primary" href="/register/plan/?type=FREE">GET STARTED</a>


class SignupTest:
    def __init__(self, _driver:webdriver.Chrome) -> None:
        self.driver = _driver
    
    @site_scraping_tests.task
    def gmail_login_check(self, _creds:dict) -> site_scraping_statuses.Status:
        self.driver.get('https://accounts.google.com/ServiceLogin/signinchooser?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&osid=1&service=mail&ss=1&ltmpl=default&rm=false&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
        _email = d.find_element_by_id('email')
        _email.send_keys(_creds['email'])
        second_d = d.find_element_by_id('identifierNext')
        second_d.send_keys('\n')
        time.sleep(4)
        new_d = d.find_elements_by_class_name('whsOnd')[0]
        new_d.send_keys(_creds['password'])
        final_d = d.find_element_by_id('passwordNext')
        final_d.send_keys('\n')
        time.sleep(20)
        return site_scraping_statuses.Status('gmail_login_check', any(i.text == 'Welcome to Datadocs!' for i in soup(self.driver.page_source, 'html.parser').find_all('span')))
        #third_d = d.find_elements_by_class_name('whsOnd')[0]

    @site_scraping_tests.task
    def site_signup(self, _creds:dict) -> site_scraping_statuses.Status:
        self.driver.get('https://staging1.datadocs.com/register/')
        self.driver.find_element_by_id('name').send_keys(_creds['name'])
        self.driver.find_element_by_id('email').send_keys(_creds['email'])
        self.driver.find_element_by_id('password').send_keys(_creds['password'])
        
        self.driver.find_element_by_id('loginButton').send_keys('\n')
        time.sleep(5)
        return site_scraping_statuses.Status('site_signup', soup(self.driver.page_source, 'html.parser').find('li', {'class':'error-message'}) is None)

    @site_scraping_tests.task
    def select_payment_tier(self, _creds:dict) -> site_scraping_statuses.Status:
        self.driver.get('https://staging1.datadocs.com/register/plan/')
        for i in self.driver.find_elements_by_tag_name('a'):
            if i.text.endswith("STARTED") and i.text.startswith('GET'):
                i.send_keys('\n')
                break

        time.sleep(2)
        return site_scraping_statuses.Status('select_payment_tier', bool(soup(self.driver.page_source, 'html.parser').find_all('div', {'class':'MinimalLoginForm'})))



    @site_scraping_tests.initialize
    def __call__(self, _payload:dict) -> None:
        for _val in _payload:
            _ = self.site_signup(_val)
            _ = self.select_payment_tier(_val)


if __name__ == "__main__":
    d = webdriver.Chrome('/Users/jamespetullo/Downloads/chromedriver')
    _credentials = [i.strip('\n') for i in open('site_creds.txt')]
    _vals = [{'email':_credentials[i], 'password':_credentials[i+1], 'name':''.join(random.choice(string.ascii_letters) for _ in range(10)), 'site_password':''.join(random.choice(string.printable) for _ in range(8))} for i in range(0, len(_credentials), 2)]
    _tasks = SignupTest(d)
    _tasks(_vals)
