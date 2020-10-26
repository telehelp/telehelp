import os
import random

from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import func

from contextlib import contextmanager

from zipcode_utils import getDistanceApart
from zipcode_utils import getDistrict
from zipcode_utils import readZipCodeData

Base = declarative_base()

# Consider useing flask-migrate in the future
class User(Base):
    __abstract__ = True
    id = Column("id", Integer, primary_key=True)
    zipcode = Column("zipcode", String)
    phone = Column("phone", String, unique=True)
    talking_to = Column("talking_to", String, nullable=True)  # Actively talking to each other
    signup_time = Column(DateTime(timezone=True), server_default=func.now())
    connected_with = Column("connected_with", String, nullable=True)  # have previously connected
    district = Column("district", String)  # TODO, pre-calculate this in the add functions

    # talking_to should probably be something else or be done in redis, but ok,
    # also it should handle multiple users in the future so we can move it to one of the child classes


class Helper(User):
    __tablename__ = "helper"
    name = Column("name", String)


class Customer(User):
    __tablename__ = "customer"


class Analytic(Base):
    __abstract__ = True
    id = Column("id", Integer, primary_key=True)
    callid = Column("callid", String)
    elkid = Column("elkid", String)
    userid = Column("userid", String)
    call_start = Column("call_start", DateTime)
    call_end = Column("call_end", DateTime)
    unregistered = Column("unregistered", Boolean)


class HelperAnalytic(Analytic):
    __tablename__ = "helper_analytic"
    contacted_prev_customer = Column("contacted_prev_customer", Boolean)


class CustomerAnalytic(Analytic):
    __tablename__ = "customer_analytic"
    n_helpers_contacted = Column("n_helpers_contacted", Integer)
    relistened_info = Column("relistened_info", String)
    new_customer = Column("new_customer", Boolean)
    used_prev_helper = Column("used_prev_helper", Boolean)
    match_found = Column("match_found", Boolean)


class CallVariable(Base):
    __tablename__ = "call_variable"
    id = Column("id", Integer, primary_key=True)
    callid = Column("callid", String)
    closest_helpers = Column("closest_helpers", String, nullable=True)
    hangup = Column("hangup", Boolean)


DB_HOST = os.getenv("DB_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Connect
engine = create_engine(
    f"postgresql+pg8000://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}/telehelp", echo=True, encoding="utf8"
)
Session = scoped_session(sessionmaker(bind=engine))

Base.metadata.create_all(bind=engine)


@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


# TODO, figure out something smart to do so these get deduplicated
class DatabaseConnection:
    """Database interface"""

    def add_helper(self, name, zipcode, phone):
        with db_session() as session:
            user = Helper(name=name, zipcode=zipcode, phone=phone)
            session.add(user)

    def add_customer(self, zipcode, phone, district):
        with db_session() as session:
            user = Customer(zipcode=zipcode, phone=phone, district=district)
            session.add(user)

    def helper_exists(self, phone):
        with db_session() as session:
            return session.query(Helper.id).filter_by(phone=phone).scalar() is not None

    def customer_exists(self, phone):
        with db_session() as session:
            return session.query(Customer.id).filter_by(phone=phone).scalar() is not None

    def helper_zipcodes(self):
        with db_session() as session:
            return session.query(Helper.zipcode).all()

    def connect_users(self, helper_phone, customer_phone):
        with db_session() as session:
            session.query(Helper).filter_by(phone=helper_phone).update({Helper.talking_to: customer_phone})
            session.query(Customer).filter_by(phone=customer_phone).update({Customer.talking_to: helper_phone})

    def reset_helper_contact(self, phone):
        with db_session() as session:
            session.query(Helper).filter_by(phone=phone).update({Helper.talking_to: None})

    def get_helper_customer(self, helper_phone):
        with db_session() as session:
            return session.query(Helper.talking_to).filter_by(phone=helper_phone).scalar()

    def get_customer_helper(self, customer_phone):
        with db_session() as session:
            return session.query(Customer.talking_to).filter_by(phone=customer_phone).scalar()

    def get_connected_helper(self, customer_phone):
        with db_session() as session:
            return session.query(Helper.phone).filter_by(connected_with=customer_phone).scalar()

    def reset_pairing(self, helper_phone):
        with db_session() as session:
            session(Helper).filter_by(phone=helper_phone).update({Helper.connected_with: None})
            session(Customer).filter_by(connected_with=helper_phone).update({Customer.connected_with: None})

    def get_helper_name(self, phone):
        with db_session() as session:
            return session.query(Helper.name).filter_by(phone=phone).scalar()

    def delete_helper(self, phone):
        with db_session() as session:
            session.query(Helper).filter_by(phone=phone).delete()
            session.query(Customer).filter_by(talking_to=phone).update({Customer.talking_to: None})

    def delete_customer(self, phone):
        with db_session() as session:
            session.query(Customer).filter_by(phone=phone).delete()
            session.query(Helper).filter_by(talking_to=phone).update({Helper.talking_to: None})

    def get_helper_zipcode(self, phone):
        with db_session() as session:
            return session.query(Helper.zipcode).filter_by(phone=phone).scalar()

    def get_customer_zipcode(self, phone):
        with db_session() as session:
            return session.query(Customer.zipcode).filter_by(phone=phone).scalar()

    def set_call_history_helpers(self, callid, closest_helpers):
        with db_session() as session:
            session.query(CallVariable).filter_by(callid=callid).update(
                {CallVariable.closest_helpers: closest_helpers}
            )

    def set_call_history_hangup(self, callid, hangup):
        with db_session() as session:
            session.query(CallVariable).filter_by(callid=callid).update({CallVariable.hangup: hangup})

    def create_call_history(self, callid):
        with db_session() as session:
            if session(CallVariable.id).filter_by(callid=callid).scalar() is not None:
                call = CallVariable(callid=callid)
                session.add(call)

    def get_call_history_hangup(self, callid):
        with db_session() as session:
            return session.query(CallVariable.hangup).filter_by(callid=callid).scalar()

    def get_call_history_helpers(self, callid):
        with db_session() as session:
            return session.query(CallVariable.closest_helpers).filter_by(callid=callid).scalar()

    def get_new_connection_details(self, helper_phone):
        with db_session() as session:
            return session.query(Helper.name, Helper.district).filter_by(phone=helper_phone).scalar()

    def fetch_closest_helpers(self, district, zipcode, location_dict):
        with db_session() as session:
            helpers_in_district = session.query(Helper).filter_by(district=district).all()

        if not helpers_in_district:
            return None

        zipped = []
        maxDist = 20
        maxQueue = 10

        for helper in helpers_in_district:
            noisy_distance = getDistanceApart(zipcode, helper.zipcode, location_dict) + random.random()

            if noisy_distance <= maxDist:
                zipped.append((helper.phone, noisy_distance))

        if not zipped:
            return None

        zipped.sort(key=lambda x: x[1])
        results = zipped[:maxQueue]
        numbers, _ = zip(*results)
        return numbers

    def write_customer_analytics(self, **kwargs):
        with db_session() as session:
            analytic = CustomerAnalytic(**kwargs)
            res = session.query(CustomerAnalytic).filter_by(callid=kwargs["callid"])
            if res.scalar() is None:
                session.add(analytic)
            else:
                res.update(analytic)

    def write_helper_analytics(self, **kwargs):
        with db_session() as session:
            analytic = CustomerAnalytic(**kwargs)
            res = session.query(HelperAnalytic).filter_by(callid=kwargs["callid"])
            if res.scalar() is None:
                session.add(analytic)
            else:
                res.update(analytic)
