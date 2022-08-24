from fastapi import FastAPI, HTTPException,Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String,DateTime
import sqlalchemy

my_database_connection = 'postgresql://waliyullah:incubation-whaleeu@borderless-crypto-db-instance.cyjsfpjxjrtj.us-east-1.rds.amazonaws.com/CryptoTransactDB'
#'postgresql://postgres:postgres@localhost/postgres'


engine = create_engine(my_database_connection)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



class testAPIModel(Base):
    __tablename__ = "transacttb"
    Symbol=  Column(String(10),primary_key=True)
    CoinName= Column(String(15),primary_key=True)
    Price= Column(String(30),primary_key=True)
    Change_24h = Column(String(10),primary_key=True)
    Volume_24h = Column(String(35),primary_key=True)
    Website = Column(String(250),primary_key=True)
    Time = Column(DateTime)


Base.metadata.create_all(bind=engine)
app = FastAPI(title= "CRYPTO_DATA_APP")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/testing_api/")
def read_users(db:Session = Depends(get_db)):
    users = db.query(testAPIModel).all()
    return users

@app.get("/testing_api/{Start_date},{End_date}")
def date_filter(Start_date:str,End_date:str,db:Session = Depends(get_db)):
    try:
        quer = db.query(testAPIModel).filter(testAPIModel.Time.between(Start_date,End_date)).all()
        return quer
    except:
        return HTTPException(status_code=404,detail="Not found")    

