
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base



SQLALCHEMY_DB_URL = "postgresql://postgres:wlcTtEoYqfomIQvJezDEAMeEmbrnAlQb@centerbeam.proxy.rlwy.net:10085/railway"


engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()