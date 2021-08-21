# coding: utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
import pandas as pd

# databese_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data.db')
engine = create_engine('postgres://zwnoabnidggxci:189655b81c38533dedf1f1576d0af6a0689e184ceaf8d36b26e944747521e4d0@ec2-34-193-101-0.compute-1.amazonaws.com:5432/d3guu425ahc2or', convert_unicode=True , echo=True)
# engine = create_engine(os.environ.get('DATABASE_URL') or 'sqlite:///' + databese_file, convert_unicode=True , echo=True)
db_session = scoped_session(
                sessionmaker(
                    autocommit = False,
                    autoflush = False,
                    bind = engine
                )
             )
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from models import Data_D
    from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
    from database import Base
    Base.metadata.create_all(bind=engine)

    from models import Data_L
    from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
    from database import Base
    Base.metadata.create_all(bind=engine)

def read_data_D():
    from models import Data_D
    import datetime
    dfD = pd.read_csv('data_D.csv')
    for index,_df in dfD.iterrows():
        date = datetime.datetime.strptime(_df['date'],'%Y-%m-%d %H:%M:%S')
        row = Data_D(date_detection=date,detection=_df['detection'])
        db_session.add(row)
    db_session.commit()

def read_data_L():
    from models import Data_L
    import datetime
    dfL = pd.read_csv('data_L.csv')
    for index,_df in dfL.iterrows():
        date = datetime.datetime.strptime(_df['date'],'%Y-%m-%d %H:%M:%S')
        row = Data_L(date_luminance=date,luminance=_df['luminance'])
        db_session.add(row)
    db_session.commit()