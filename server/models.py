from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

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