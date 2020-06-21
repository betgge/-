from flask import Flask, render_template, request
from MK_scrapper import MK_get_today_article, date_today
from HK_scrapper import HK_get_today_article
# import random
from apscheduler.schedulers.background import BackgroundScheduler
import json

# 과제 언론사 여러개 더하고 실시간 인기 기사 스크래핑 + 프론트엔드 손보기(UX/UI)
# 직접 모든 기사들 각각의 url로 들어가 기사 직접 스크래핑하기. 기사요약본이위에 클릭하면 기사 본문이 나오도록 할 수 있음 => 모달창 형식으로 뜨게 만들기.
# 실시간 인기 기사 리스트, 각 언론사들의 상위 기사들 순위 등등 여러가지가 가능.
# 로그인 기능 구현, 개인별 저장기능 구현
# 예를들어 실시간 인기 1위기사의 사진을 대문으로 걸기.
# 데이터베이스에 저장한 놈들을 파일로 저장하는 방법과 파일에서 db로 꺼내오는 방법
# CRUD 시스템.
# POPULAR POP 기사들 
# 원하는 기사 저장하기(SEXY)

db = {}
date = {}

app = Flask('Today_Ecomony_News_Scrapper')
nameTag = [
  {'key':'MK','name':'매일경제'},
  {'key':'HK','name':'한국경제'}
]

def save_file():
  try:
    with open('db_file','w') as db_file:
      json.dump(db, db_file)
    with open('date_file','w') as date_file:
      json.dump(date, date_file)
  except:
    pass

def load_file(): 
  try:
    with open('db_file','r') as db_file:
      return json.load(db_file)
  except:
    return {}

def load_date():
  try:
    with open('date_file','r') as date_file:
      return json.load(date_file)
  except:
    return {}

def run_saving():
  MK_NEWS = MK_get_today_article()
  today = date_today()
  HK_NEWS = HK_get_today_article()
  db['MK_NEWS'] = MK_NEWS
  db['HK_NEWS'] = HK_NEWS
  date['today'] = today
  save_file()

run_saving()
scheduler = BackgroundScheduler()
scheduler.add_job(func=run_saving, trigger="interval", minutes=10)
scheduler.start()
# 30분 마다 db에 데이터 갱신 


@app.route('/')
def main():
  full_db = db
  today = date['today']
  return render_template('crazy.html', nameTag=nameTag,db=full_db,today=today)


# def main():
#   random.shuffle(press)
#   return render_template('main.html', press=press)

@app.route('/select/')
def select():
  today = date['today']
  press = request.args.get('press')
  name = request.args.get('name')
  if press == 'MK':
    NEWS = db.get('MK_NEWS')
  elif press == 'HK':
    NEWS = db.get('HK_NEWS')
  return render_template('one.html',today=today,NEWS=NEWS,name=name,press=press,nameTag=nameTag)
  
  # 입력하는 언론사 이름에 맞는 언론사 정보 받아오기.

db = load_file()
date = load_date()
print(db)
app.run(host='0.0.0.0')