from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = 'sqlite:///./oyenlogin.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
LocalSession = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
