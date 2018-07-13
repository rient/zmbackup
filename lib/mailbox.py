#!/usr/bin/python3

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Importing the Config Files
from config import config

# Loading the database
engine = create_engine(config['DATABASE'])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Creating the tables - all of them should start with zm in their names

# Create the SESSION table
# For status field the following options are valid:
# Running -> The backup is in execution right now
# Concluded -> The backup is concluded
# Scheduled -> Somewhere in the future the backup will be done
class Sessions(Base):

    # Inform a name for the table
    __tablename__ = 'zm_session'

    # Session Table info
    _id = Column(String(15), primary_key=True)
    initial_date = Column(DateTime, default=datetime.now())
    conclusion_date = Column(DateTime)
    size = Column(Integer,nullable=False,default=0)
    bkp_type = Column(String(20),nullable=False)
    status = Column(String(10),nullable=False,default="Scheduled")

# Create the USER table
# For status field the following options are valid:
# Running -> The backup is in execution right now
# Concluded -> The backup is concluded
# Scheduled -> Somewhere in the future the backup will be done
class Users(Base):

    # Inform a name for the tables
    __tablename__ = 'zm_user'

    # User table info
    _id = Column(Integer,primary_key=True, autoincrement=True)
    zm_session_id = Column(String(15),ForeignKey("zm_session._id"))
    email = Column(String(200),nullable=False)
    size = Column(Integer,default=0)
    initial_date = Column(DateTime, default=datetime.now())
    conclusion_date = Column(DateTime)
    status = Column(String(10),default="Scheduled")

    # Relationship to easy return the Session info from user if needed
    zm_session = relationship("Sessions")

    @staticmethod
    def create(**kwargs):
        user = Users(zm_session_id=kwargs['sessionID'],email=kwargs['email'])
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def find(**kwargs):
        user = session.query(Users).filter(User.zm_session_id == kwargs['sessionID'],
                                           User.email == kwargs['email'])
        return user
