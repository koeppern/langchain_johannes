# 2023-06-03
# Test of serpapi which can be used as tool for a langchain agent

import configparser
from serpapi_test import GoogleSearch

config_filename = "C://config//cofig.ini"

config = configparser.ConfigParser()

config.read(config_filename)
 
google_api_key = config['DEFAULT']['GOOGLE_API']

os.environ["SERPAPI_API_KEY"] = google_api_key


search = GoogleSearch({
    "q": "coffee", 
    "location": "Austin,Texas",
    "api_key": google_api_key
  })
result = search.get_dict()