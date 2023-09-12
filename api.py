

from fastapi import FastAPI, APIRouter
import uvicorn
import redis
import json

app=FastAPI()
router=APIRouter()

todo_list=["1"]
r=redis.Redis(host='localhost',port=6379,db=0)

@app.get("/")
async def welcome() -> dict:
    json = {
            "message" : "Hello World"
            }
    return json

@router.post("/addUser")
async def add_user(user: dict) -> dict:
    #r.hset("id::"+user["name"] , mapping=user)
    print("user::::",user)
   #print("change:::",json.dump)
    r.lpush("user",json.dumps(user))
    return {"message" : "add User successfully!"}

@router.post("/getUser")
async def get_userInfo(user: dict) -> dict:
    return r.hgetall("id::"+user["name"])

@router.post("/deleteUser")
async def delete_userInfo(user: dict) -> dict:
    r.delete("id::"+user["name"])
    return {"message" : 'delete user '+user["name"]}


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
