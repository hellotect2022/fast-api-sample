from fastapi import FastAPI 
from fastapi.responses import RedirectResponse
from routes.users import user_router 
from routes.events import event_router 
import uvicorn 
from database.connection import conn 


app=FastAPI()

@app.on_event("startup")
def on_startup():
    conn()

@app.get("/")
async def home()->dict:
    return RedirectResponse(url="/event/")
    # return {
    #     "message":"hello world!"
    # }

#라우터 등록 
app.include_router(user_router,prefix="/user")
app.include_router(event_router,prefix="/event")

if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=80,reload=True)