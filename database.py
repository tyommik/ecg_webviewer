import json
import os
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta
from itertools import groupby

import pandas as pd
import sqlalchemy
from sqlalchemy import Integer, ForeignKey, String, Column, DateTime, Boolean, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


def count_per_day(ecg_list) -> dict:
    ecg_dates = [i.done_time.strftime('%d-%m-%Y') for i in ecg_list]
    days = {(datetime.now() - timedelta(days=d)).strftime('%d-%m-%Y'): 0 for d in range(31)}
    for ecg in ecg_dates:
        days[ecg] += 1
    return days


class Main(Base):
    __tablename__ = 'main'
    id = Column(Integer, primary_key=True)
    patient_id = Column(String(128))
    test_id = Column(String(128))
    date_of_test = Column(DateTime)
    report = Column(String)
    path = Column(String)
    url = Column(String)
    hold_by = Column(DateTime)
    done_time = Column(DateTime)
    block_by_user_id = Column(Integer)
    done = Column(Boolean)
    done_by_user_id = Column(String)
    age = Column(Integer)
    sex = Column(Integer)
    anno = relationship("Annotations", backref="annotation")


class Annotations(Base):
    __tablename__ = 'annotations'
    id = Column(Integer, ForeignKey(Main.id), primary_key=True, autoincrement=True)
    anno = Column(String)

    def __repr__(self):
        return f"<Annotations()>"


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    userpassword = Column(String)


class Database:
    def __init__(self, csvdb, root_url, sqldb, create_new=False):
        self.df = pd.read_csv(csvdb, index_col=None)
        self.root_url = root_url
        self.db = sqldb
        self.session = self.connect()
        if create_new:
            self.init_db()

    def connect(self):
        # TODO safety multithreading
        self.engine = create_engine(self.db, connect_args={'check_same_thread': False})
        self.connection = self.engine.connect()
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def init_db(self):
        metadata = MetaData()
        main_table = Main()

        annotations = Annotations()

        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

        for row_idx, _ in enumerate(self.df.iterrows()):
            source = self.df.iloc[row_idx]
            main_row = Main(patient_id=source['patient_id'],
                            test_id=source['test_id'],
                            date_of_test=datetime.strptime(source['date_of_test'], '%Y-%m-%d'),
                            report=source['report'],
                            url=os.path.join(self.root_url, source['patient_id'], source['test_id']),
                            hold_by=datetime.strptime("01-01-2000", '%d-%m-%Y'),
                            path=source["path"],
                            age=source["age"],
                            sex=int(source["sex"]),
                            done=False
                            )
            anno_row = Annotations(anno=json.dumps({}))
            self.session.add(main_row)
            self.session.add(anno_row)
        self.session.commit()

    def query_new_list(self, length: int = 50, skip_holded=False):
        """ Return rows of size [size] and not holded """
        result = self.session.query(Main).filter(sqlalchemy.and_(Main.hold_by < datetime.now(), Main.done == False)).first()

        query = sqlalchemy.select([Main])
        query = query.where(sqlalchemy.and_(Main.hold_by < datetime.now(), Main.done == False, Main.patient_id == result.patient_id)).order_by(Main.date_of_test)
        query = query.limit(length)
        ResultProxy = self.connection.execute(query)
        all_data = ResultProxy.fetchall()
        result = [(i[0], i[3].strftime("%d-%m-%Y")) for i in all_data]
        return result

    def query_holded_list(self, length: int, user: str, skip_holded=False):
        """ Return rows of size [size] and not holded """
        query = sqlalchemy.select([Main])
        query = query.where(
            sqlalchemy.and_(Main.hold_by > datetime.now(), Main.block_by_user_id == user, Main.done == False)).order_by(Main.date_of_test)
        query = query.limit(length)
        ResultProxy = self.connection.execute(query)
        all_data = ResultProxy.fetchall()
        result = [(i[0], i[3].strftime("%d-%m-%Y")) for i in all_data]
        return result

    def hold_list(self, idx_list: list, user: str, holdtime=timedelta(days=1)):
        """ Hold list of ids by holdtime """
        for i, _ in idx_list:
            result = self.session.query(Main).filter(Main.id == i)
            result.update({"hold_by": datetime.now() + holdtime, "block_by_user_id": user})
        self.session.commit()

    def unhold_list(self, idx_list: list, user: str, holdtime=timedelta(days=1)):
        """ Hold list of ids by holdtime """
        for i, _ in idx_list:
            result = self.session.query(Main).filter(Main.id == i)
            result.update({"hold_by": datetime.strptime("01-01-2000", '%d-%m-%Y')})
        self.session.commit()

    def query(self, idx: int):
        """ Query data of specific id"""
        query = sqlalchemy.select([Main])
        query = query.where(Main.id == idx)
        ResultProxy = self.connection.execute(query)
        query_result = ResultProxy.fetchall()[0]
        query_result = dict(query_result)
        return query_result

    def query_anno(self, idx: int):
        anno = sqlalchemy.select([Annotations])
        anno = anno.where(Annotations.id == idx)
        ResultProxy = self.connection.execute(anno)
        anno_result = ResultProxy.fetchall()[0]
        anno_result = dict(anno_result)
        return anno_result

    def update_anno(self, idx: int, user: str, anno: dict):
        """ Update specific anno by id """
        anno = json.dumps(anno)
        result = self.session.query(Annotations).filter(Annotations.id == idx)
        result.update({"anno": anno})
        self.mask_as_done(idx, user)
        self.session.commit()

    def mask_as_done(self, idx, user):
        """ mark record done """
        result = self.session.query(Main).filter(Main.id == idx)
        result.update({"done_by_user_id": user, "done": True, "done_time": datetime.now()})
        self.session.commit()

    def __len__(self):
        query = self.session.query(Main).count()
        return query

    def count_done(self):
        query = self.session.query(Main).filter(Main.done == True).count()
        return query

    def count_done_by_user(self, user):
        total = self.session.query(Main).filter(Main.done_by_user_id == user).count()
        count_by_days = self.session.query(Main).filter(Main.done_by_user_id == user).filter(Main.done_time > datetime.now() - timedelta(days=30))
        days_stat = count_per_day(count_by_days.order_by(Main.done_time).all())
        return total, days_stat

    def get_users_list(self):
        raise NotImplementedError

    def query_done_list(self, length: int, user: str, skip_holded=False):
        """ Return rows of size [size] and not holded """
        query = sqlalchemy.select([Main])
        query = query.where(Main.done == True)
        query = query.limit(length)
        ResultProxy = self.connection.execute(query)
        all_data = ResultProxy.fetchall()
        result = [(i[0], i[1], i[9], i[11], i[3].strftime("%d-%m-%Y")) for i in all_data]
        return result