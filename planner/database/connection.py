from sqlmodel import SQLModel, Session, create_engine 
from models.events import Event, EventUpdate 

# database_file = "planner.db"

# database_connection_string = f"sqlite:///{database_file}"
# connect_args = {"check_same_thread": False}
# engine_url = create_engine(database_connection_string, echo=False, connect_args = connect_args)

db_name='fastapi'
db_id = 'dhhan'
db_ip = 'localhost' # 자신의 로컬컴퓨터
db_password = 'gksengus1'
db_port = '3306'
 
engine = create_engine("mysql+pymysql://" + db_id + ":" + db_password + "@"
                                        + db_ip + ":" + db_port + "/" + db_name, encoding='utf-8')

def conn():
    #SQLModel.metadata.create_all(engine_url)
    SQLModel.metadata.create_all(engine)
    
def get_session():
    print("get_session")
    #with Session(engine_url) as session:
    with Session(engine) as session:
        yield session