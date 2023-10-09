from typing import List
from fastapi import FastAPI, Depends
from database import SessionLocal
from sqlalchemy.orm import Session
from models import *
from schemas import *
app=FastAPI()
def get_db():
   db = SessionLocal()
   try:
      yield db
   finally:
    db.close()

@app.post("/customers/", response_model=CustomerResponse,tags=["Customers"])
def create_customer(customer: CustomerCreate,db:Session=Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    db.close()
    return db_customer

 
@app.get("/customers/",tags=["Customers"])
async def get_staff(db:Session=Depends(get_db)):
    res=db.query(Customer).all()
    return res   
    
@app.post("/tickets/", response_model=TicketResponse,tags=["Tickets"])
def create_ticket(ticket: TicketCreate,db:Session=Depends(get_db)):
    db_ticket = Tickets(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    db.close()
    return db_ticket

@app.get("/tickets/",tags=["Tickets"])
async def get_staff(db:Session=Depends(get_db)):
    res=db.query(Tickets).all()
    return res


@app.post("/staff/", response_model=StaffResponse,tags=["Staff"])
def create_staff(staff: StaffCreate,db:Session=Depends(get_db)):
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    db.close()
    return db_staff
@app.get("/staff/",tags=["Staff"])
async def get_staff(db:Session=Depends(get_db)):
    res=db.query(Staff).all()
    return res

@app.post("/phone_numbers/", response_model=PhoneNumberResponse,tags=["PhoneNumber"])
def create_phone_number(phone_number: PhoneNumberCreate,db:Session=Depends(get_db)):
    db_phone_number = PhoneNumber(**phone_number.dict())
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    db.close()
    return db_phone_number

@app.get("/phone_numbers/",tags=["PhoneNumber"])
async def get_phone_numbers(db:Session=Depends(get_db)):
    res=db.query(PhoneNumber).all()
    return res

@app.post("/bills/", response_model=BillResponse,tags=["Bill"])
def create_bill(bill: BillCreate,db:Session=Depends(get_db)):
    db_bill = Bill(**bill.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    db.close()
    return db_bill

@app.get("/bills/",tags=["Bill"])
async def get_bills(db:Session=Depends(get_db)):
    res=db.query(Bill).all()
    return res

