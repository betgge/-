import requests
from bs4 import BeautifulSoup

def get_html():
  URL = 'https://www.hankyung.com/all-news/economy'
  HK = requests.get(URL)
  return BeautifulSoup(HK.text,'html.parser')

def HK_get_today_article():
  NEWS = []
  html = get_html()
  article_list = html.find('ul',{'class':'article_list'}).find_all('li')
  i=1
  for block in article_list:
    print(f'HK keep going{i}')
    i=i+1
    title = block.find('h3',{'class':'tit'}).find('a').get_text(strip=True)
    url = block.find('a')['href']
    URL = f'{url}'
    img_url = requests.get(URL)
    html = BeautifulSoup(img_url.text,'html.parser')
    try:
      img_url = html.find('div',{'class':'articleimage'}).find('img')['src']
    except:
      img_url = ''
    date = html.find('span',{'class':'date-published'}).find('span',{'class':'num'}).get_text(strip=True)
    desc = html.find('div',{'id':'articletxt'}).find('br').previous_sibling
    strong = html.find('div',{'id':'articletxt'}).find('strong')
    if strong:
      try:
        desc = strong.find('font').get_text(strip=True)
      except:
        desc = html.find('div',{'id':'articletxt'}).find('br').previous_sibling.string
    # find는 그 자체가 찾는 함수이기 때문에 if:에서 존재를 확인하는 작업에서도 해당 메소드를 작동해서 정의할 필요가 있기 때문에 find에서 찾지 못하면 오류가 일어나는 것이다.

    NEWS.append({'title':title, 'url':url, 'img_url':img_url, 'date':date , 'desc':desc})
        # try는 오류가 나면 그 이후는 실행이 되지 않는 것이다.
  return NEWS


# 종목별 기사 스크래핑, 전체기사 인기기사 모두 다 스크래핑 

