from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Customer,ServiceRequest,Staff,PhoneNumber,Bill
from schemas import CustomerCreate,CustomerResponse,ServiceRequestCreate,TicketCreate,TicketResponse,ServiceResponse,StaffCreate,StaffResponse,PhoneNumberResponse,BillResponseModel,PhoneNumberCreate,BillCreate

app = FastAPI()

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Create Customer      
@app.post("/customers/", response_model=CustomerResponse,tags=["Customers"])
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer
#get all customers
@app.get('/customers/',tags=["Customers"])
async def get_customers(db:Session=Depends(get_db)):
    res=db.query(Customer).all()
    return res 
#Get Customer By id
@app.get("/customers/{customer_id}", tags=["Customers"])
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customerid == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
#Update Customer
@app.put("/customers/{customer_id}", response_model=CustomerResponse,tags=["Customers"])
def update_customer(customer_id: int, customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.customerid == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    for key, value in customer.dict().items():
        setattr(db_customer, key, value)
    db.commit()
    db.refresh(db_customer)
    return db_customer
#delete Customer by id.
@app.delete("/customers/{customer_id}",tags=["Customers"])
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customerid == customer_id).delete()
    db.commit()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {f"Customer id {customer_id} is deleted successfully"}

# Create
@app.post("/service_requests/", response_model=TicketResponse,tags=["ServiceRequests"])
def create_service_request(service_request: TicketCreate, db: Session = Depends(get_db)):
    db_service_request = ServiceRequest(**service_request.dict())
    db.add(db_service_request)
    db.commit()
    db.refresh(db_service_request)
    return db_service_request

#get all customers
@app.get('/service_requests/',tags=["ServiceRequests"])
async def get_service_requests(db:Session=Depends(get_db)):
    res=db.query(ServiceRequest).all()
    return res 
#Get Customer By id
@app.get("/service_requests/{service_request_id}", tags=["ServiceRequests"])
def get_customer_by_id(service_request_id: int, db: Session = Depends(get_db)):
    customer = db.query(ServiceRequest).filter(ServiceRequest.ticketid == service_request_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Ticket Not Found")
    return customer
# Update
@app.put("/service_requests/{ticket_id}", response_model=ServiceResponse,tags=["ServiceRequests"])
def update_service_request(ticket_id: int, service_request: ServiceRequestCreate, db: Session = Depends(get_db)):
    db_service_request = db.query(ServiceRequest).filter(ServiceRequest.ticketid == ticket_id).first()
    if db_service_request is None:
        raise HTTPException(status_code=404, detail="Service Request not found")
    for key, value in service_request.dict().items():
        setattr(db_service_request, key, value)
    db.commit()
    db.refresh(db_service_request)
    return db_service_request

#delete Customer by id.
@app.delete("/service_requests/{ticket_id}",tags=["ServiceRequests"])
def delete_customer(ticket_id: int, db: Session = Depends(get_db)):
    customer = db.query(ServiceRequest).filter(ServiceRequest.ticketid== ticket_id).delete()
    db.commit()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {f"Customer id {ticket_id} is deleted successfully"}


@app.post("/staff/", response_model=StaffCreate,tags=["Staff"])
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


#get all staffs
@app.get('/staff/',tags=["Staff"])
async def get_all_staff(db:Session=Depends(get_db)):
    res=db.query(Staff).all()
    return res 

@app.get("/staff/{staff_id}",tags=["Staff"])
def get_staff_by_id(staff_id: int, db: Session = Depends(get_db)):
    staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff

@app.put("/staff/{staff_id}", response_model=StaffCreate,tags=["Staff"])
def update_staff(staff_id: int, staff: StaffCreate, db: Session = Depends(get_db)):
    db_staff = db.query(Staff).filter(Staff.staffid == staff_id).first()
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    for key, value in staff.dict().items():
        setattr(db_staff, key, value)
    db.commit()
    db.refresh(db_staff)
    return db_staff

#delete Customer by id.
@app.delete("/staff/{staff_id}",tags=["Staff"])
def delete_customer(staff_id: int, db: Session = Depends(get_db)):
    customer = db.query(Staff).filter(Staff.staffid== staff_id).delete()
    db.commit()
    if not customer:
        raise HTTPException(status_code=404, detail="Staffid not found")
    return {f"Staff id {staff_id} is deleted successfully"}

@app.post("/phone_numbers/", response_model=PhoneNumberResponse,tags=["PhoneNumber"])
def create_phone_number(phone_number: PhoneNumberResponse, db: Session = Depends(get_db)):
    db_phone_number = PhoneNumber(**phone_number.dict())
    db.add(db_phone_number)
    db.commit()
    db.refresh(db_phone_number)
    return db_phone_number
#get all staffs
@app.get('/phone_numbers/',tags=["PhoneNumber"])
async def get_all_staff(db:Session=Depends(get_db)):
    res=db.query(PhoneNumber).all()
    return res
@app.get("/phone_numbers/{customer_id}",tags=["Staff"])
def get_staff_by_id(customerid: int, db: Session = Depends(get_db)):
    staff = db.query(PhoneNumber).filter(PhoneNumber.customer == customerid).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="PhoneNumber not found")
    return staff


@app.post("/bills/", response_model=BillResponseModel,tags=["Bill"])
def create_bill(bill: BillResponseModel, db: Session = Depends(get_db)):
    db_bill = Bill(**bill.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill
#get all staffs
@app.get('/bills/',tags=["Bill"])
async def get_all_bills(db:Session=Depends(get_db)):
    res=db.query(Bill).all()
    return res

@app.get("/bills/{bill_id}",tags=["Bill"])
def get_bill_by_id(billid: int, db: Session = Depends(get_db)):
    staff = db.query(Bill).filter(Bill.billid == billid).first()
    if staff is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    return staff
@app.delete("/bills/{bill_id}",tags=["Bill"])
def delete_customer(bill_id: int, db: Session = Depends(get_db)):
    customer = db.query(Bill).filter(Bill.billid== bill_id).delete()
    db.commit()
    if not customer:
        raise HTTPException(status_code=404, detail="Staffid not found")
    return {f"Bill id {bill_id} is deleted successfully"}