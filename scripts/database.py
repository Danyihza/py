from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

dbhost = os.environ['DB_HOST']
dbport = os.environ['DB_PORT']
dbuser = os.environ['DB_USER']
dbpassword = os.environ['DB_PASSWORD']
db = os.environ['DB_NAME']
dbtype = os.environ['DB_TYPE']

SQLALCHEMY_DATABASE_URI = f"{dbtype}://{dbuser}:{dbpassword }@{dbhost}:{dbport}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()