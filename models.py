# -*- coding: utf-8 -*-

# others
from datetime import datetime, timedelta
# SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float, desc, and_
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Car(Base):
    __tablename__ = 'car'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    registration_num = Column(String)
    full_name = Column(String) # opis
    vin = Column(String)

    # Relationships
    refueling = relationship('Fuel', back_populates="car")
    reparations = relationship('Reparation', back_populates="car")
    technicalReviews = relationship('TechnicalReview', back_populates="car")
    replecements = relationship('Replecement', back_populates="car")
    insurances = relationship('Insurance', back_populates="car")

    def __init__(self, name, full_name, registration_num, vin):
        self.name = name
        self.registration_num = registration_num
        self.full_name = full_name
        self.vin = vin

class Fuel(Base):
    __tablename__ = 'fuel'
    id = Column(Integer, primary_key=True)
    auto_id = Column(Integer, ForeignKey('car.id'))
    refuel_date = Column(Date, default=datetime.now())
    quantity = Column(Float)
    price = Column(Float) # cena za litr
    mileage = Column(Float, nullable=True)
    value = Column(Float) # cena litr * ilosc

    # reverse
    car = relationship("Car", back_populates="refueling")

    def __init__(self, auto_id, refuel_date, quantity, price, mileage, value):
        self.auto_id = auto_id
        self.refuel_date = refuel_date
        self.quantity = quantity
        self.price = price
        self.mileage = mileage
        self.value = value

class Reparation(Base):
    __tablename__ = 'reparation'
    id = Column(Integer, primary_key=True)
    auto_id = Column(Integer, ForeignKey('car.id'))
    description = Column(String)
    repair_date = Column(Date, default=datetime.now())
    price = Column(Float)

    #reverse
    car = relationship("Car", back_populates="reparations")

    def  __init__(self, auto_id, description, repair_date, price):
        self.auto_id = auto_id
        self.description = description
        self.repair_date = repair_date
        self.price = price


class Replecement(Base):
    __tablename__ = 'replecement'
    id = Column(Integer, primary_key=True)
    auto_id = Column(Integer, ForeignKey('car.id'))
    replace_date = Column(Date)
    replace_date_next = Column(Date)
    description = Column(String)
    price = Column(Float)
    mileage = Column(Float, nullable=True)

    # reverse
    car = relationship("Car", back_populates="replecements")

    def __init__(self, auto_id, description, price, replace_date, mileage, replace_date_next):
        self.auto_id = auto_id
        self.description = description
        self.price = price
        self.replace_date = replace_date
        self.mileage = mileage
        self.replace_date_next = replace_date_next

class TechnicalReview(Base):
    __tablename__ = 'technicalreview'
    id = Column(Integer, primary_key=True)
    auto_id = Column(Integer, ForeignKey('car.id'))
    techrev_date = Column(Date, default=datetime.now())
    techrev_next_date = Column(Date)
    price = Column(Float)
    comments = Column(String)

    # reverse
    car = relationship("Car", back_populates="technicalReviews")

    def __init__(self, auto_id, techrev_date, techrev_next_date, price, comments):
        self.auto_id = auto_id
        self.techrev_date = techrev_date
        self.techrev_next_date = techrev_next_date
        self.price = price
        self.comments = comments

class Insurance(Base):
    __tablename__ = 'insurance'
    id = Column(Integer, primary_key=True)
    auto_id = Column(Integer, ForeignKey('car.id'))
    firm = Column(String)
    price = Column(Float)
    date_from = Column(Date, default=datetime.now())
    date_to = Column(Date)
    type_of = Column(String) # OC or OC+AC
    comments = Column(String)

    # reverse
    car = relationship("Car", back_populates="insurances")

    def __init__(self, auto_id, firm, price, date_from, date_to, type_of, comments):
        self.auto_id = auto_id
        self.firm = firm
        self.price = price
        self.date_from = date_from
        self.date_to = date_to
        self.type_of = type_of
        self.comments = comments


# -----------------  DATABASE CONNECTION  ---------------------

def database_connect():
    engine = create_engine('sqlite:///BazaDanych/samochodzik.db')
    # engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
    connection = engine.connect()
    '''
    if engine.has_table("Car"):
        Car.__table__.drop(engine)
        Fuel.__table__.drop(engine)
        Reparation.__table__.drop(engine)
        Replecement.__table__.drop(engine)
        TechnicalReview.__table__.drop(engine)
        Insurance.__table__.drop(engine)
    '''
    # create tables
    Base.metadata.create_all(engine)
    # create session
    Session = sessionmaker(bind=engine)
    session = Session()
    #test_data_for_database(session)
    return session

# ---------------------  TESTY --------------------------------

def test_data_for_database(session):
    c1 = Car("Mercedes")
    c2 = Car("Audi")
    session.add_all([
                        c1,
                        c2
        ])
    session.commit()

    session.add_all([
                        Fuel(c1.id, datetime.now(), 100, 5, 1000),
                        Fuel(c1.id, datetime.now()+timedelta(days=10), 120, 4.90, 1500),
                        Fuel(c2.id, datetime.now(), 200, 4.85, 500),
                        Fuel(c2.id, datetime.now()-timedelta(days=20), 100, 4.83, 100)
        ])
    session.commit()

    
