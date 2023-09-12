import redis
#from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time 
import pymysql
import json


class User:
    def insert(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "insert into users values(%s, %s)"
        vals = (vo.id, vo.name)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()

class MyObject:
    def __init__(self, data):
        self.__dict__ = data

def add_data_to_db():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value= r.lrange("user",0,-1)
    
    element = r.lpop("user")
    if element:
        #r.lpush("user",element)
        json_str = element.decode('utf-8')
        
        jsonobj = json.loads(json_str)
        obj = MyObject(jsonobj)
        user=User()
        user.insert(obj)
        print(f"insert to db {obj.id}, {obj.name}")
    else:
        print("redis에 값이 없습니다.")

#scheduler = BackgroundScheduler()
#scheduler.add_job(add_data_to_db,'interval',seconds=2)
#scheduler.start()
r=redis.Redis(host='localhost',port=6379,db=0)


#try:
    # 스케줄러가 계속 실행되도록 유지
#    while True:
#        pass
#except (KeyboardInterrupt, SystemExit):
    # Ctrl+C 또는 종료 시 스케줄러 정지
#    scheduler.shutdown()

def test():
    try:
        while True:
            add_data_to_db()
            time.sleep(2) 
    except (KeyboardInterrupt, SystemExit):
        print("종료합니다.ㅋㅋ")

    #scheduler = BackgroundScheduler()
    #scheduler.add_job(add_data_to_db,'interval',seconds=1)
    #scheduler.start()



if __name__ == "__main__":
    test()
