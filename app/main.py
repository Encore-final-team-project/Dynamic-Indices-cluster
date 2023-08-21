from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://admin:qwer1234@outsider-mysql.czxgnu6kme38.ap-northeast-2.rds.amazonaws.com/test"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Table1(Base):
    __tablename__ = "table1"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    db = SessionLocal()  # Create a new session instance
    analysis_result = db.query(Table1).first().name  # Fetch the name value from the first row
    db.close()  # Close the session after executing the query
    return templates.TemplateResponse("index.html", {"request": request, "analysis_result": analysis_result})
