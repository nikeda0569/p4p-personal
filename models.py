# coding: utf-8
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from database import Base
from datetime import datetime as dt

#Table情報
class Data_D(Base):
    #TableNameの設定
    __tablename__ = "data_detection"
    #Column情報を設定する
    id = Column(Integer, primary_key=True)
    date_detection = Column(DateTime, unique=False)
    detection = Column(Integer, unique=False)

    def __init__(self, date_detection=None, detection=None, timestamp=None):
        self.date_detection = date_detection
        self.detection = detection
        self.timestamp = timestamp

class Data_L(Base):
    #TableNameの設定
    __tablename__ = "data_luminance"
    #Column情報を設定する
    id = Column(Integer, primary_key=True)
    date_luminance = Column(DateTime, unique=False)
    luminance = Column(Integer, unique=False)

    def __init__(self, date_luminance=None, luminance=None, timestamp=None):
        self.date_luminance = date_luminance
        self.luminance = luminance
        self.timestamp = timestamp