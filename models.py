#! coding:utf-8
__author__ = 'haocheng'

from sqlalchemy import Column, create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:@localhost:3306/zero?charset=utf8')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
session = DBSession()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Job(BaseModel):

    __tablename__ = 'Job'

    id = Column(Integer, primary_key=True)
    positionname = Column(String(30))
    positionid = Column(Integer)
    companyid = Column(Integer)
    s_salary = Column(Integer)
    e_salary = Column(Integer)
    company = Column(String(20))
    status = Column(Integer)
    area = Column(String(10))
    experience = Column(String(20))
    education = Column(String(10))
    tag = Column(String(40))


init_db()