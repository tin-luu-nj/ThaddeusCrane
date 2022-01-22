import datetime, json, re, yaml
from os.path import exists
from os import remove
from requests import Session
from bs4 import BeautifulSoup

from pyExtern import extern

class clsMangaFeed(Session):
  def __init__(self) -> None:
    super().__init__()
    if exists('./notification/manga-feed.yml'):
      with open('./notification/manga-feed.yml', 'r') as stream:
        extern.gMangaFeed = yaml.load(stream, Loader=yaml.CLoader)
      remove('./notification/manga-feed.yml')
    else:
      pass
    self.logged = False
    self.__login()

  def __login(self) -> bool:
    _url    = 'https://manga4life.com/auth/login.php'
    payload = extern.gConfig['webscraper']['manga-feed']
    request = self.post(_url, json=payload)
    result  = json.loads(request.text)
    if result['success'] and result['val'] == 'ok':
      self.logged = True
    else:
      self.logged = False

  async def checkFeed(self):
    if self.logged:
      _url = 'https://manga4life.com/feed.php'
      soup = BeautifulSoup(self.get(_url).content, "html.parser")
      content = soup.find_all("script")[-1].string

      vmFeedJSON = re.search('vm.FeedJSON = (.*?);', content)
      data = json.loads(vmFeedJSON.group(1))

      _url  = 'https://manga4life.com/read-online/'
      today = str(datetime.datetime.today().date())

      if not str(today) in extern.gMangaFeed:
        extern.gMangaFeed = {}
        extern.gMangaFeed[str(today)] = {}
        extern.gMangaFeed[str(today)]['new'] = []
        extern.gMangaFeed[str(today)]['notified'] = []
      else:
        pass

      for entry in data:
        date = re.search('^(.*?)T', entry['Date']).group(1)
        if date == today:

          chapter = int(entry['Chapter'])%100000
          if 0 == chapter%10:
            chapter = int(chapter/10)
          else:
            chapter = float(chapter/10.0)

          indexName   = entry['IndexName']
          chapter_url = '{}{}-chapter-{}.html'.format(_url, indexName, chapter)

          if not chapter_url in extern.gMangaFeed[str(today)]['notified']:
            extern.gMangaFeed[str(today)]['new'].append(chapter_url)
          else:
            pass

        else:
          break
    else:
      print('[ERR] manga-feed not logged in')