from os.path import join, dirname, abspath
from sys import path as sys_path
sys_path.append(join(dirname(abspath(__file__)), 'bin'))

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import time

import yaml

with open('Alfred.yml', 'r') as stream:
  env = yaml.load(stream, Loader=yaml.CLoader)

URL = "https://manga4life.com/"

def init(url: str):
  opts = Options()
  opts.headless = True
  assert opts.headless # Operating in headless mode
  browser = Edge(options=opts)
  browser.get(url)
  return browser

def close(browser: Edge):
  browser.close()

def login(browser):
  timeout = 3
  page_ready = False
  try:
    element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.ID, 'Nav')))
    page_ready = True
  except TimeoutException:
    print("Loading took too much time!")

  if (True == page_ready):
    element = browser.find_element(By.XPATH, '//div[@class="container MainContainer"]//input[@type="email"]')
    element.send_keys('trongtin96@gmail.com')

    element = browser.find_element(By.XPATH, '//div[@class="container MainContainer"]//input[@type="password"]')
    element.send_keys('SHERlocked@manga4life.19')

    element = browser.find_element(By.XPATH, '//div[@class="container MainContainer"]//button')
    element.click()

    try:
      element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/user/subscription.php"]')))
      page_ready = True
    except TimeoutException:
      print("Loading took too much time!")

def getSubcription(browser: Edge):
  subURL = 'https://manga4life.com/user/subscription.php'
  browser.get(subURL)
  timeout = 3
  page_ready = False
  try:
    element = WebDriverWait(browser, timeout).until(EC.presence_of_element_located((By.XPATH, '//span[@ng-if="!vm.GettingSubscription"]')))
    page_ready = True
  except TimeoutException:
    print("Loading took too much time!")

  time.sleep(1)
  if (True == page_ready):
    element = browser.find_element(By.XPATH, '//div[@ng-if="vm.Subscription.length > 0"]')
    element_src = element.get_attribute("outerHTML")
    with open('./mangaFeedSubscription.html', 'w') as f:
      f.write(element_src)
    # elements = browser.find_elements(By.XPATH, '//span[@ng-if="Series.LatestChapter.Chapter != \'N/A\'"]')
    # for element in elements:
    #   print(element.find_element(By.TAG_NAME, 'span').text)
    #   print(element.find_element(By.TAG_NAME, 'a').text)
    #   print(element.find_element(By.TAG_NAME, 'a').get_attribute('href'))

# def mangaFeed():
#   browser = init(URL)
#   login(browser)
#   # time.sleep(6)
#   getSubcription(browser)

class WebScrapper(object):
  def __init__(self) -> None:
    super().__init__()
    opts = Options()
    # opts.headless = True
    # assert opts.headless # Operating in headless mode
    self.browser = Edge(options=opts)

  def login(self):
    TIMEOUT = env['bot']['webscraper']['manga-feed']['timeout']
    PAGE_READY = False
    self.browser.get(env['bot']['webscraper']['manga-feed']['url'])
    try:
      element = WebDriverWait(self.browser, TIMEOUT).until(EC.presence_of_element_located((By.ID, 'Nav')))
      PAGE_READY = True
    except TimeoutException:
      print("[INF] Loading Timeout")

    if PAGE_READY:
      for e in env['bot']['webscraper']['manga-feed']['login']['element']:
        BY = By.XPATH
        element = self.browser.find_element(BY, e['element'])
        if e['type'] == 'text-field':
          element.send_keys(e['value'])
        elif e['type'] == 'click':
          element.click()

if '__main__' == __name__:
  mangaFeed = WebScrapper()
  mangaFeed.login()
  # mangaFeed()