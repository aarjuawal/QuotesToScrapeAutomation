from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from unittest import TestCase
from selenium.webdriver.chrome.options import Options
def setup():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://quotes.toscrape.com/")
    return driver
def teardown(driver):
    driver.quit()

def element_locator():
      return {
        "quotes": '//div[@class="quote"]/span[@itemprop="text"]',
        "title": '//h1',
        "first_quote": '//div[@class="quote"][1]',
        "authors": '//div[@class="quote"]/span/small[@itemprop="author"]',
        "tags": '//div[@class="tags"]/a',""
        "top_tags": "//span[@class='tag-item']/a[@class='tag']",
        "next_button": "//li[@class='next']/a",
        "love_button": "//span[@class='tag-item']/a[@class='tag' and text()='love']",
        "about_link": "(//small[@class='author']/following-sibling::a)[1]",
        "about_description": '(//div[@class="author-details"]//child::strong)[2]',
        "login_button": "//p/a[text()='Login']",
        "username_field": "//input[@id='username']",
        "password_field": "//input[@id='password']",
        "submit_button": "//input[@type='submit']",
        "logout_button": "//p/a[@href='/logout']",
        "author_birth_name": "//h3[@class='author-title']",
        "author_birth_date": "//span[@class='author-born-date']",
        "author_birth_location": "//span[@class='author-born-location']"
      }
class TestQuotesToScrape(TestCase):

    def test_AssertTitle(self):
        driver = setup()
        try:
            self.assertEqual(driver.title, "Quotes to Scrape")
            print('pass-title found')
        except AssertionError as e:
            print('fail-title not found')
            print(e)
        finally:
            teardown(driver)
    
TestQuotesToScrape().test_AssertTitle()
class TestQuotesContent(TestCase):
    def quotes_contents(self):
        driver = setup()
        locator = element_locator()
        try:
            quotes = driver.find_elements(By.XPATH, locator['quotes'])
            for quote in quotes:
                author = driver.find_elements(By.XPATH, locator['authors'])
                tags = driver.find_elements(By.XPATH, locator['tags'])
                self.assertTrue(author, "Author is missing in quote block")
                print('testpass-author found')
                self.assertTrue(tags, "Tags are missing in quote block")
                print('testpass-tag found')

        except AssertionError as e:
            print(e)    
        teardown(driver)
TestQuotesContent().quotes_contents()        
class TestAuthor(TestCase):
    def check_for_quote(self):
        driver = setup()
        quotes = driver.find_elements(By.CLASS_NAME, 'text')
        authors = driver.find_elements(By.CLASS_NAME, 'author')
        tags_list = driver.find_elements(By.CLASS_NAME, 'tags')

        for i in range(len(quotes)):
            print(f"'{quotes[i].text}'")
            print(f"-by{authors[i].text}")
            tags = tags_list[i].find_elements(By.TAG_NAME,'a')
            tag_texts = [tag.text for tag in tags]
            if tag_texts:
                print("Tags:", ", ".join(tag_texts))
            else:
                print("Tags: None")
            expected_result= authors[i].text
            try:
                self.assertGreater(len(authors),0,"Test Result: fail - author is not present.")
                print("Test Result: pass - Author is present")
            except AssertionError as e:
                print(e)
            

        teardown(driver)
TestAuthor().check_for_quote() 
class TestTagPresence(TestCase):    
    def get_tags(self):
        driver = setup()
        locator=element_locator()
        pTag = driver.find_elements(By.XPATH, locator["tags"])
        p_text=[p.text for p in pTag]
        for val in pTag:
            print(val.text)

        try:
            self.assertIn("world",p_text,"TestFailed-world not found")
            print("Testpass-found world")
        except AssertionError as e:
            print(e)
        

        teardown(driver)
TestTagPresence().get_tags()
class Lovebtn(TestCase):
  def love_btn(self):
    driver=setup()
    locator = element_locator()
    loveBtn =driver.find_element(By.XPATH, locator["love_button"] )
    loveBtn.click()
    try:
      actres=driver.find_element(By.XPATH, "//div[@class='container']/h3")
      actualResult = actres.text
      expectedResult= "Viewing tag: love"
      self.assertEqual(actualResult,expectedResult,'failed-title not found')

      print("Success!-found title")
    except AssertionError as e:
      print(e)
    teardown(driver) 
Lovebtn().love_btn()

class TestLogin(TestCase):
    def valid_credentials(self):
        driver = setup()
        wait = WebDriverWait(driver, 10)
        locator = element_locator()
        LoginBtn = driver.find_element(By.XPATH, locator["login_button"])
        LoginBtn.click()
        username = wait.until(EC.presence_of_element_located((By.XPATH, locator["username_field"])))
        username.send_keys("aa@gmail.com")
        password= driver.find_element(By.XPATH, locator["password_field"])
        password.send_keys("akkaka")
        submit = driver.find_element(By.XPATH, locator["submit_button"])
        submit.click()
        logout= wait.until(EC.presence_of_element_located((By.XPATH, "//p/a[@href='/logout']")))
        actualResult=logout.text
        expectedResult="Logout"
        try:
            self.assertEqual(actualResult,expectedResult,"Login unsuccessful")
            print("Login Successful")
        except Exception as e:
            print(e)
        finally:
            teardown(driver)
TestLogin().valid_credentials()
class TestLogin2(TestCase):    
    def login_with_invalid_username(self):
        driver = setup()
        wait=WebDriverWait(driver,10)
        LoginBtn = driver.find_element(By.XPATH, '//a[@href="/login"]')
        LoginBtn.click()
        username= wait.until(EC.presence_of_element_located((By.ID, "username")))
        username.send_keys("as@gmail.com")
        password= wait.until(EC.presence_of_element_located((By.ID, "password")))
        password.send_keys("11")
        submit = driver.find_element(By.XPATH, "//input[@type='submit']")
        submit.click()
        time.sleep(2)
        expected_result="https://quotes.toscrape.com"
        try:
            actual_result = driver.current_url
            self.assertEqual(actual_result,expected_result,"test fail-User is logged in even with invalid username")

            print("Test Result: Pass - User is not logged in with invalid username.")
        except AssertionError as e:
            print(e)
            
        
        teardown(driver)
TestLogin2().login_with_invalid_username()
class TestLoginWithEmptyField(TestCase):    
    def login_with_empty_field(self):
        driver = setup()
        locator=element_locator()
        wait=WebDriverWait(driver,10)
        LoginBtn = driver.find_element(By.XPATH, locator['login_button'])
        LoginBtn.click()
        username= wait.until(EC.presence_of_element_located((By.XPATH, locator['username_field'])))
        username.send_keys("")
        password= wait.until(EC.presence_of_element_located((By.XPATH, locator['password_field'])))
        password.send_keys("")
        submit = driver.find_element(By.XPATH, locator['submit_button'])
        submit.click()
        time.sleep(2)
        expected_result="https://quotes.toscrape.com"
        try:
            self.assertTrue(expected_result,"test fail-User is logged in even with empty credentials")
            print("Test Result: Pass - User is not logged in with empty credentials.")
        except AssertionError as e:
            print(e)   
        teardown(driver)
TestLoginWithEmptyField().login_with_empty_field()
class TestTagCount(TestCase):    
    def check_lessthan(self):
        driver = setup()
        locator=element_locator()
        Top_tag = driver.find_elements(By.XPATH, locator["top_tags"])        
        try:
            self.assertLess(len(Top_tag),11,"TestFail-top tags are not less than 11")
            print("Testpass-top tags are less than 11")
        except AssertionError as e:
            print(e)
        
        teardown(driver)
TestTagCount().check_lessthan()
class TestQuotesCount(TestCase):    
    def check_greaterthan(self):
        driver = setup()
        locator=element_locator()
        totalQuotes=0
        quotes = driver.find_elements(By.XPATH, locator["quotes"])  
        while True:
              noOfQuotesPerPage = len(driver.find_elements(By.XPATH, locator['quotes']))
              totalQuotes += noOfQuotesPerPage
              next_buttons = driver.find_elements(By.XPATH, locator['next_button'])
              if next_buttons:
                  next_buttons[0].click()
              else:
                  break
        self.assertGreater(totalQuotes,50, "Failed: All quotes are not there")
        print("Pass: Total no. of quotes: ", totalQuotes)

        
        teardown(driver)
TestQuotesCount().check_greaterthan()
class TestAuthorDescription(TestCase):
    def check_description(self):
        driver = setup()
        locator=element_locator()
        try:
            about_author= driver.find_element(By.XPATH, locator["about_link"])
            about_author.click()
            expected_result= "Description"
            actual_result = driver.find_element(By.XPATH, "//div[@class='author-details']")
            self.assertIn(expected_result,actual_result.text,"failed-description not found")
            print("pass-description is present")
        except AssertionError as e:
              print(e)

        teardown(driver)
TestAuthorDescription().check_description()


class TestAuthorDetails(TestCase):
    def author_details_page(self):
        driver = setup()
        locator = element_locator()
        about_author= driver.find_element(By.XPATH, locator["about_link"])
        about_author.click()
        author_name = driver.find_element(By.XPATH, locator['author_birth_name'])
        author_dob = driver.find_element(By.XPATH, locator['author_birth_date'])
        author_location = driver.find_element(By.XPATH, locator['author_birth_location'])
        author_description = driver.find_element(By.XPATH, locator['about_description'])
        expected_result = all([author_name, author_dob, author_location, author_description]) 
        try:
            # self.assertTrue(author_name,"TestFail- Doesnot contains author name")
            # print("Test Pass - The author details page contains author name.")
            # self.assertTrue(author_dob,"TestFail-Doesnot contains author dob")
            # print("Test Pass - The author details page contains author date of birth.")
            # self.assertTrue(author_location,"fail")
            # print("Test Pass - The author details page contains author location.")
            # self.assertTrue(author_description,"fail")
            # print("Test Pass - The author details page contains author description.")
             self.assertTrue(expected_result,"TestFail- The author details paeg doesnot contains all the author details")
             print("Test Pass - The author details page contains all the author details.")
        except AssertionError as e:
            print(e)
        
        teardown(driver)
TestAuthorDetails().author_details_page()
class TestQuotesPerPage(TestCase):
    def get_quote_perpage(self):
        driver = setup()
        locator=element_locator()
        try:
            noOfQuotesPerPage = len(driver.find_elements(By.XPATH, locator['quotes']))
            self.assertLessEqual(noOfQuotesPerPage,10,'TestFailed-the number of quotes is not 10 or less')
            print("Testpass-the number of qoutes:", noOfQuotesPerPage)
        except AssertionError as e:
            print(e)

        teardown(driver)
TestQuotesPerPage().get_quote_perpage() 
class TestWholePageContent(TestCase):
    def get_whole_page(self):
        driver =setup()
        locator = element_locator()
        wait = WebDriverWait(driver, 10)
        title= wait.until(EC.presence_of_element_located((By.XPATH, locator['title']))).text.strip()
        logout= wait.until(EC.presence_of_element_located((By.XPATH, locator['login_button']))).text.strip()
        quotes=  wait.until(EC.presence_of_element_located((By.XPATH, locator['quotes']))).text.strip()
        tags=  wait.until(EC.presence_of_element_located((By.XPATH, locator['tags']))).text.strip()
        next= wait.until(EC.presence_of_element_located((By.XPATH, locator['next_button']))).text.strip()
        expected_result = all([title, logout, quotes, tags, next]) 
        try:
            self.assertTrue(expected_result, 'TestFail-some elements are missing')
            print('pass-found all items')
        except AssertionError as e:
            print(e)


        teardown(driver)
TestWholePageContent().get_whole_page()
