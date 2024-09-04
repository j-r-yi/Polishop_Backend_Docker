from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import pymysql
pymysql.install_as_MySQLdb()

# DATABASE_URL = "mysql://root:joshua123@localhost/polishop"
DATABASE_URL = "mysql://root:Joshua123!@localhost:3306/polishop"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)
