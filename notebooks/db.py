import os

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete


Model = declarative_base()
engine = create_engine(os.environ['DATABASE_URL'])
Model.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
