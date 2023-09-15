

from fastapi import FastAPI, APIRouter
import uvicorn
import redis
import json
import pymysql
from datetime import datetime

app=FastAPI()
router=APIRouter()

todo_list=["1"]
r=redis.Redis(host='localhost',port=6379,db=0)

  
class User:
    def insert(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "insert into user values(%s, %s, %s)"
        vals = (vo.id, vo.name, vo.createTime)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()
    def update(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "insert into user values(%s, %s, %s)"
        vals = (vo.id, vo.name, vo.createTime)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()
    def delete(self, vo):
        self.conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')
        cur = self.conn.cursor()
        sql = "insert into user values(%s, %s, %s)"
        vals = (vo.id, vo.name, vo.createTime)
        cur.execute(sql, vals)
        self.conn.commit()
        self.conn.close()

class MyObject:
    def __init__(self, data):
        self.__dict__ = data

@app.get("/")
async def welcome() -> dict:
    json = {
            "message" : "Hello World"
            }
    return json

@router.post("/addUser")
async def add_user(user: dict) -> dict:
    # 사용자 검증
    userList = r.lrange("user",0,-1)
    if len(userList) > 0:
        for u in userList:
            print(user["id"],json.loads(u)["id"])
            if user["id"] == json.loads(u)["id"]:
                return {"message" : "same id conflict!!"}

    # redis insert
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user["createTime"] = current_time
    user["index"] = len(userList)+1
    jsonobj=json.dumps(user)
    r.rpush("user",jsonobj)

    #insert into db
    # obj = MyObject(user)
    # user=User()
    # user.insert(obj)
    return {"message" : "add User successfully!"}

@router.post("/deleteUser")
async def delete_userInfo(user: dict) -> dict:
    # 사용자 검증
    length = r.llen("user")
    if length > 0:
        nomatch=False
        for i in range(length):
            element = json.loads(r.lindex("user", i))
            #print(user["id"],element["id"])
            if user["id"] == element["id"]:
                print("index",r.lindex("user", i).decode('utf-8'))
                r.lrem("user",1,r.lindex("user", i))
                return {"message" : f"delete user name :{element['name']}(id={element['id']}) !!"}
            else:
                nomatch=True
        if nomatch==True:
            return {"message" : "ther is no user match id"}
    else:
        return {"message" : "there is no user"}

    # redis queue stack 에 삭제 내용 적기 

    # redis insert
    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # user["createTime"] = current_time
    # jsonobj=json.dumps(user)
    # r.lpush("user",jsonobj)

    # #insert into db
    # obj = MyObject(user)
    # user=User()
    # user.insert(obj)
    # return {"message" : "add User successfully!"}


    #r.delete("id::"+user["name"])
    
    #delete from db

    return {"message" : 'delete user '+user["name"]}

@router.post("/updateUser")
async def update_userInfo(user: dict) -> dict:
    # 사용자 검증
    length = r.llen("user")
    if length > 0:
        nomatch=False
        for i in range(length):
            element = json.loads(r.lindex("user", i))
            #print(user["id"],element["id"])
            if user["id"] == element["id"]:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                user["createTime"] = current_time
                r.lset("user",i,json.dumps(user))
                return {"message" : f"update user name(id={element['id']}):{element['name']} -> {user['name']}!!"}
            else:
                nomatch=True
        if nomatch==True:
            return {"message" : f"ther is no match user(id={user['id']})"}
    else:
        return {"message" : "there is no user"}


@router.get("/getAllUser")
async def get_allUser()->dict:
    return r.lrange("user",0,-1)

@router.post("/getUser")
async def get_userInfo(user: dict) -> dict:
    return r.hgetall("id::"+user["name"])

@router.post("/todo")
async def add_todo(todo: dict) -> dict:
    #todo_list.append(todo)
    value = todo["item"]
    r.lpush("todo",value)
    return {"message":"Todo added successfully"}

@router.get("/todo")
async def retrieve_todo() -> dict:
    todo_list=r.get("todo")
    return {"todos":todo_list}


# router를 app에 연결
app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
