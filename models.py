from database import Base,engine
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
class Customer(Base):
    __tablename__ = "Customer"

    custid = Column(Integer, primary_key=True, index=True)
    lastname = Column(String)
    firstname = Column(String)
    idf_proof = Column(String)
    idnumber = Column(String)
    phone_number_id = Column(Integer, ForeignKey('PHONENUMBER.phone_number'))
    address = Column(String)
    dob = Column(String)
    phone_number = relationship("PhoneNumber", back_populates="customer")

class Tickets(Base):
    __tablename__ = "Tickets"

    Ticketid = Column(Integer, primary_key=True, index=True)
    phone_number_id = Column(Integer, ForeignKey('PHONENUMBER.phone_number'))
    custid = Column(Integer, ForeignKey('Customer.custid'))
    staffid = Column(Integer, ForeignKey('Staff.staffid'))
    TicketStatus = Column(String)
    Description = Column(String)

class Staff(Base):
    __tablename__ = "Staff"

    staffid = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    idproof = Column(String)
    idnumber = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    
class PhoneNumber(Base):
    __tablename__ = "PHONENUMBER"

    phone_number = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    plan = Column(String)
    customer = relationship("Customer", back_populates="phone_number")

class Bill(Base):
    __tablename__ = "Bill"

    Billid = Column(Integer, primary_key=True, index=True)
    phone_number_id = Column(Integer, ForeignKey('PHONENUMBER.phone_number'))
    Amount = Column(Integer)
    
Base.metadata.create_all(bind=engine)