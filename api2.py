

from fastapi import FastAPI, APIRouter
import uvicorn
import redis
from redis.exceptions import ConnectionError
import json
import pymysql
import time
from datetime import datetime
from database.myDB import Database

app=FastAPI()
router=APIRouter()

r=redis.Redis(host='localhost',port=6379,db=0)
conn = pymysql.connect(host='localhost', user='dhhan', password='0000', db='fastapi', charset='utf8')

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
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    user["createTime"] = current_time
    user["index"] = len(userList)+1
    r.rpush("user",json.dumps(user))
     #삽입을 적재시키기 위한 queue
    user["type"]="insert"
    r.rpush("user-call",json.dumps(user))
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
                
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                user["createTime"] = current_time
                user["type"] = "delete" 
                #삭제를 적재시키기 위한 queue
                r.rpush("user-call",json.dumps(user))
                return {"message" : f"delete user name :{element['name']}(id={element['id']}) !!"}
            else:
                nomatch=True
        if nomatch==True:
            return {"message" : "ther is no user match id"}
    else:
        return {"message" : "there is no user"}

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
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                user["createTime"] = current_time
                r.lset("user",i,json.dumps(user))

                #업데이트를 적재시키기 위한 queue
                user["type"]="update"
                r.rpush("user-call",json.dumps(user))
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

def redis_state_check() -> bool:
    redisCheck = True
    while redisCheck:
        time.sleep(3)
        try:
            r.ping()
            print("Redis 서버 연결 성공")
            redisCheck = False
        except ConnectionError as e:
            print("Redis 서버 연결 실패:", e)
            redisCheck = True
        except Exception as e:
            print("다른 예외 발생:", e) 
            redisCheck = True      

def redis_check() -> dict:

    # redis 민 후 db 연결
    r.flushall()
    cur = conn.cursor()
    sql = "select * from user where useYn='Y' "
    cur.execute(sql)
    dbList = cur.fetchall()
    conn.commit()
    conn.close()
   
    if len(dbList) > 0:
        for row in dbList:
            data = {}
            data["id"] = row[0]
            data["name"] = row[1]
            data["createTime"] = row[2].strftime("%Y-%m-%d %H:%M:%S.%f")
            r.lpush("user",json.dumps(data))
    
    return {"meesage":"redis sync"}

# router를 app에 연결
app.include_router(router, prefix="")

if __name__ == "__main__":
    redis_state_check()
    my_db = Database()

    # db 에서 최신 날짜 비교 
    db_date = my_db.selectLastCreateTime()

    #backupfromDB = False
    if db_date is not None:
        userList = r.lrange("user",0,-1)
        if len(userList) > 0:
            redis_time = datetime(1970, 1, 1)
            for value in userList:
                redis_time_str = json.loads(value)["createTime"]
                if redis_time < datetime.strptime(redis_time_str, "%Y-%m-%d %H:%M:%S.%f"):
                    redis_time = datetime.strptime(redis_time_str, "%Y-%m-%d %H:%M:%S.%f")
            if db_date > redis_time :
                print("db 값이 가장최신입니다.")
                redis_check()
            else :
                print("redis 값이 가장최신입니다.")
        else :
            print("redis 에 값이 없어서 db에서 백업합니다.")
            redis_check()            
    uvicorn.run(app, host="0.0.0.0", port=8000)
