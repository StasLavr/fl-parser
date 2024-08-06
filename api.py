import requests
from datetime import datetime
from bs4 import BeautifulSoup
import fake_useragent
user = fake_useragent.UserAgent().random
session = requests.Session()

class flparcer():
    def __init__(self, src):
        self.src = src
    
    def getfllist(self):
      
      header = {'user-agent': user}

      data = {
         'username':	"staslav12@gmail.com",
         'password':  "l3107945%L"

      }
      login = session.post("https://www.fl.ru/account/login/", data=data, headers=header).text
      res = session.get(self.src, headers=header )
      soup = BeautifulSoup(res.text, "lxml")
      name = soup.findAll("div", class_="search-lenta-item c")
      list = []
      for el in name:
          name = el.find("h3").text
          name = name.replace("\n", '')
          url = el.find("h3")
          url = "https://www.fl.ru" + el.find('a').get('href') 
          res = session.get(url, headers=header)
          soup = BeautifulSoup(res.text, "lxml")
          price = soup.find('div', class_="py-32 text-right unmobile flex-shrink-0 ml-auto mobile") 
          try: 
            price = price.find('span').text.strip()
          except AttributeError:
            price = soup.find('div', class_="d-flex b-layout__table_bordbot_df b-layout__table_2bordtop_df mb-20 text-dark py-32")
          try:
            price = price.find('span', class_="text-8 text-md-4").text.strip()
          except TypeError:
             pass
          overview = soup.find('div', class_="text-5 b-layout__txt_padbot_20")
          try:
            overview = overview.text
          except AttributeError:
            overview = soup.find('div', class_="text-5 b-layout__txt_padbot_20 wizard__editor")
            overview = overview.text
          overview = overview.replace("<br/>", "\n \n")
          overview = overview.strip()
          if overview.lower().find("<") != -1: 
             overview = overview.replace('<', '').replace('>', '')
          else:
             pass
          lenov = len(overview)
          if lenov > 3000:
             overview = overview[0:3001] + "\n Сообщение слишком большое"
          else:
              pass
          date = soup.find('div', class_="b-layout__txt b-layout__txt_padbot_30 mt-32")
          date = date.find('div', class_="text-5")
          date = date.text
          date = date.replace("                                ", " ")
          date = date.replace("                 ", ' ')
          date = date.replace('                ', " ")
          date = date.strip()
          dateall = date.replace(".", '').replace(":", '')
          # dateall = dateall[0:8] + dateall [11:15]
          dateall = dateall[2:4] + dateall[0:2] + dateall[4:8] + dateall [11:15]
          data = {
              'name': name,
              'url': url,
              'price': price,
              'overview': overview,
              'date': date,
              'dateall': dateall,
          }
          list.append(data)
      return list