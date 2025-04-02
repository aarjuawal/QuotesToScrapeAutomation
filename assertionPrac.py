from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
from unittest import TestCase
def setup():
    driver = webdriver.Chrome()
    driver.get("https://quotes.toscrape.com/")
    return driver
def teardown(driver):
    driver.quit()

def element_locator():
      return {
        "quotes": '//div[@class="quote"]/span[@itemprop="text"]',
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
            print('pass')
        except AssertionError as e:
            print('fail')
            print(e)
        finally:
            teardown(driver)
    
TestQuotesToScrape().test_AssertTitle()



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
      # assert actualResult == expectedResult, 'Failed'
      self.assertEqual(actualResult,expectedResult,'failed')

      print("Success!")
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
    def login_with_invalid_credentials(self):
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
TestLogin2().login_with_invalid_credentials()
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
class TestTagCount(TestCase):    
    def check_lessthan(self):
        driver = setup()
        locator=element_locator()
        Top_tag = driver.find_elements(By.XPATH, locator["top_tags"])        
        try:
            self.assertLess(len(Top_tag),11,"TestFail-Is not less than 11")
            print("Testpass-Is less than 11")
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
            self.assertIn(expected_result,actual_result.text,"failed")
            print("pass")
        except AssertionError as e:
              print(e)

        teardown(driver)
TestAuthorDescription().check_description()


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
