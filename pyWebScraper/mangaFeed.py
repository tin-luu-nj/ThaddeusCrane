"""! @brief Defines the Manga Feed class """

################################################################################
# @file bot.py
#
# @brief This file defines class(es) and function(s) for pyWebScraper.
#
# @section Description
# Defines class for MangaFeed
# - clsMangaFeed
#
# @section Libraries/Modules
# - datetime standard library
#    + Access today and date method in datetime class
# - re standard library
#    + Access search method
# - os standard library
#    + Access to exists method in path module
#    + Access to remove method
# - json standard library
#    + Access to loads method
# - yaml open-source library
#    + Access to loads method
#    + Access to YAML Loader "yaml.CLoader"
# - requests open-source library
#    + Access to Session class
# - extern local library
#    + [RO] gConfig
#    + [RW] gMangaFeed
#
# @section NOTE
# - None
#
# @section TODO
# - None
#
# @section Change History
# Example description:
# Version Y-M-D       Author      Change description
# 1.0.0   2022-01-22  Tin Luu     Initial Version
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Get shared variable across modules
from pyExtern import extern

# Import standard library
import datetime, re, json
from os.path import exists
from os import remove

# Import open-source library
import yaml
from requests import Session
from bs4 import BeautifulSoup

class clsMangaFeed(Session):
  """! The Discord Bot base class.
  Defines the base class utilized the Discord Bot.
  """
  def __init__(self) -> None:
    """! The Manga Feed class initializer.

    @param  None.
    @return  None.
    """
    # Initialization with base class
    super().__init__()
    # When manga-feed.yml is existed
    if exists('./notification/manga-feed.yml'):
      # Open manga-feed.yml as standard input stream
      with open('./notification/manga-feed.yml', 'r') as stream:
        # Load manga-feed.yml to MangaFeed
        extern.gMangaFeed = yaml.load(stream, Loader=yaml.CLoader)
      # Remove manga-feed.yml
      remove('./notification/manga-feed.yml')
    # When manga-feed.yml is not existed
    else:
      pass
    # Set logged to False
    self.logged = False
    # Invoke login
    self.__login()

  def __login(self) -> None:
    """! Login method.

    @param  None.
    @return  None.
    """
    # Get login URL
    _url    = 'https://manga4life.com/auth/login.php'
    # Get payload JSON
    payload = extern.gConfig['webscraper']['manga-feed']
    # Invoke POST request with payload JSON
    request = self.post(_url, json=payload)
    # Load response of POST request
    result  = json.loads(request.text)
    # Check result of response
    if result['success'] and result['val'] == 'ok':
      self.logged = True
    else:
      self.logged = False

  async def checkFeed(self):
    """! Checking Manga Feed method.

    @param  None.
    @return  None.
    """
    # When Request is logged in
    if self.logged:
      # Get feed URL
      _url = 'https://manga4life.com/feed.php'
      # Parse feed response using Beautiful Soup
      soup = BeautifulSoup(self.get(_url).content, "html.parser")
      # Get content of feed response
      content = soup.find_all("script")[-1].string
      # Get vmFeedJSON from script
      vmFeedJSON = re.search('vm.FeedJSON = (.*?);', content)
      # Load vmFeedJSON to data local variables
      data = json.loads(vmFeedJSON.group(1))
      # Get template of chapter URL
      _url  = 'https://manga4life.com/read-online/'
      # Get today date
      today = str(datetime.datetime.today().date())
      # When Manga Feed contains today information
      if not today in extern.gMangaFeed:
        # Reset Manga Feed
        extern.gMangaFeed = {}
        extern.gMangaFeed[today] = {}
        extern.gMangaFeed[today]['new'] = []
        extern.gMangaFeed[today]['notified'] = []
      # When Manga Feed does not contain today information
      else:
        pass

      # Loop through each entry in data
      for entry in data:
        # Regex search and split date information
        date = re.search('^(.*?)T', entry['Date']).group(1)
        # If entry date is today
        if date == today:
          # Get chapter information
          # Chapter information is equal to chapter*10 + 100000
          chapter = int(entry['Chapter'])%100000
          if 0 == chapter%10:
            chapter = int(chapter/10)
          else:
            chapter = float(chapter/10.0)
          # Get IndexName of Series
          indexName   = entry['IndexName']
          # Get chapter URL
          chapter_url = '{}{}-chapter-{}.html'.format(_url, indexName, chapter)
          # When entry is not notified
          if not chapter_url in extern.gMangaFeed[today]['notified']:
            # Append chapter URL to Manga Feed
            extern.gMangaFeed[today]['new'].append(chapter_url)
          # When entry is notified
          else:
            pass
        # If entry date is not today
        else:
          break
    # When request is not logged
    else:
      print('[ERR] manga-feed not logged in')

################################################################################
# END OF FILE
################################################################################
