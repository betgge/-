import requests
from bs4 import BeautifulSoup

def get_html():
  URL = 'https://www.mk.co.kr/news/business/'
  MK = requests.get(URL)
  return BeautifulSoup(MK.content.decode('euc-kr','replace'),'html.parser')

def MK_get_today_article():
  NEWS = []
  html = get_html()
  article_list = html.find_all('dl',{'class':"article_list"})
  i=1
  for block in article_list:
    print(f'MK keep going{i}')
    i=i+1
    title = block.find('dt',{'class':'tit'}).find('a').get_text(strip=True)
    desc = block.find('span',{'class':'desctxt'}).get_text(strip=True)
    date = block.find('span',{'class':'date'}).get_text(strip=True)
    url = block.find('a')['href']
    try:
      URL = f'{url}'
      img_url = requests.get(URL)
      html = BeautifulSoup(img_url.content.decode('euc-kr','replace'),'html.parser')
      img_url = html.find('div',{'class':'art_txt'}).find_all('img')
      if html.find('div',{'class':'art_txt'}).find('div').find('div',{'class','zoom_icon'}):
        img_url = img_url[1]['src']
      else:
        img_url = img_url[0]['src']
    except:
      img_url = "{{ url_for('static', filename='5.jpg') }}"
    NEWS.append({'title':title,'desc':desc,'date':date, 'url':url, 'img_url':img_url})
  return NEWS


def date_today():
  URL = 'https://www.mk.co.kr/news/all/'
  MK = requests.get(URL)
  html = BeautifulSoup(MK.content.decode('euc-kr','replace'),'html.parser')
  date_today = html.find('ul',{'class':'sub_tab_list'}).find('li',{'class':'on'}).find('a').get_text(strip=True)
  return date_today

