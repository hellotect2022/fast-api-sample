import redis
#from fastapi import FastAPI, BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time 
import pymysql
import json
import asyncio

class User:
    def insert(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        #sql = "insert into user values(%s, %s, %s, %s, 'Y')"
        sql = ''' INSERT INTO user (id, name, createtime, type, useYn) 
                    VALUES (%s, %s, %s, %s, 'Y') 
                    ON DUPLICATE KEY UPDATE 
                    name = VALUES(name),  -- 중복되는 경우 name 열을 업데이트
                    createtime = VALUES(createtime),
                    type = 'insert',
                    useYn = 'Y'
                '''
        vals = (vo.id, vo.name, vo.createTime, vo.type)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()
    def update(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "update user set name=%s, createTime=%s, type=%s where id=%s and createTime < %s and useYn ='Y'" 
        vals = (vo.name, vo.createTime, vo.type ,vo.id, vo.createTime)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()
    def update2(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "update user set name=%s, createTime=%s, type=%s, useYn ='N' where id=%s and createTime < %s and useYn='Y'"
        vals = (vo.name, vo.createTime, vo.type ,vo.id, vo.createTime)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()
    def delete(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "delete from user where id=%s"
        vals = (vo.id)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()

class MyObject:
    def __init__(self, data):
        self.__dict__ = data

async def insert_redis_to_db():
    try :

        if r.llen("user-call") > 0:

            for i in range(r.llen("user-call")):
                #element = r.lindex("user-call", i)
                element = r.lpop("user-call")
                print(i," : ",element)
                jsonobj = json.loads(element)
                print(i," 22: ",jsonobj)
                obj = MyObject(jsonobj)
                user=User()
                
                if obj.type == "insert":
                    user.insert(obj)
                elif obj.type == "delete":
                    user.update2(obj)
                elif obj.type == "update":
                    user.update(obj)
                print(f"{obj.type} to db {obj.id}, {obj.name}")
                
                #r.lrem("user-call",1,r.lindex("user-call", i))
        else:
            print("redis에 값이 없습니다.")
    except Exception as e:
        print("redis 에서 이상발생.",e)

r=redis.Redis(host='localhost',port=6379,db=0)


async def test():
    try:
        while True:
            await asyncio.sleep(10)
            await insert_redis_to_db()
    except (KeyboardInterrupt, SystemExit):
        print("종료합니다.ㅋㅋ")

async def printt(text):
    print(text)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()
