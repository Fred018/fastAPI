
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


_db_path = os.path.join(os.path.dirname(__file__), "todoapp.db")
SQLALCHEMY_DB_URL = "postgresql://postgres:wlcTtEoYqfomIQvJezDEAMeEmbrnAlQb@centerbeam.proxy.rlwy.net:10085/railway"


engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()