from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Customer,ServiceRequest,Staff,PhoneNumber,Bill
from schemas import LoginRequest,StaffLoginRequest,CustomerCreate,CustomerResponse,ServiceRequestCreate,TicketCreate,TicketResponse,ServiceResponse,StaffCreate,StaffResponse,PhoneNumberResponse,BillResponseModel,PhoneNumberCreate,BillCreate
from sqlalchemy.orm import joinedload,subqueryload
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.templating import Jinja2Templates
# templates = Jinja2Templates(directory="templates")
app = FastAPI()

# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_customer(identifier):
    db = SessionLocal()
    customer = db.query(Customer).filter((Customer.customerid == identifier) | (Customer.email == identifier)).first()
    db.close()

    if not customer:
        return None  # Customer not found
    return customer.customerid

def verify_staff(identifier):
    db = SessionLocal()
    customer = db.query(Customer).filter((Customer.customerid == identifier) | (Customer.email == identifier)).first()
    db.close()

    if not customer:
        return None  # Customer not found
    return customer.customerid

@app.post("/login", tags=["Authentication"])
def login(request: LoginRequest):
    customer = verify_customer(request.random_string)
    if not customer:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return {"customer_id":customer}
    #return templates.TemplateResponse("index.html", {"request": request, "first_name": "Your return value here"})

@app.post("/staff_login", tags=["Authentication"])
def login(request: StaffLoginRequest,db:Session=Depends(get_db)):
    staff=db.query(Staff).filter(Staff.staffid == request.id).first()

    if not staff:
        raise HTTPException(status_code=401, detail="Authentication failed")

    return {"staff_id":staff.staffid}




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
# @app.get('/service_requests/',tags=["ServiceRequests"])
# async def get_service_requests(db:Session=Depends(get_db)):
#     res=db.query(ServiceRequest).all()
#     return res 

@app.get('/service_requests/',tags=["ServiceRequests"])
async def get_service_requests(db:Session=Depends(get_db)):
    service_requests = db.query(ServiceRequest).options(subqueryload(ServiceRequest.customer))
    service_requests = service_requests.all()
    if not service_requests:
        raise HTTPException(status_code=404, detail="No service requests found.")
    response = {
        "service_requests": []
    }
    for request in service_requests:
        customer_details = request.customer
        response["service_requests"].append({
            "ticketid": request.ticketid,
            "customer_details": {
                "customerid": customer_details.customerid,
                "firstname": customer_details.firstname,
                "lastname": customer_details.lastname,
                # Add more customer details as needed
            },
            "description":request.description,
            "ticketstatus":request.ticketstatus
        })

    return response
    #res=db.query(ServiceRequest).all()
    #return res 

#Get Customer By id
# @app.get("/service_requests/{customer_id}", tags=["ServiceRequests"])
# def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
#     customer = db.query(ServiceRequest).join(Customer,ServiceRequest.ticketid == customer_id).filter(Customer.customerid == customer_id).all()
#     if customer is None:
#         raise HTTPException(status_code=404, detail="Ticket Not Found")
#     return customer

######################################################################################
# @app.get("/service_requests/{customer_id}", tags=["ServiceRequests"])
# def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
#     customer_subquery = db.query(Customer).filter(Customer.customerid == customer_id).subquery()
#     service_requests = db.query(ServiceRequest).join(customer_subquery, ServiceRequest.customerid == customer_subquery.c.customerid)
#     service_requests = service_requests.all()
#     if not service_requests:
#         raise HTTPException(status_code=404, detail="No service requests found for the provided customer.")
#     customer_details = db.query(Customer).filter(Customer.customerid == customer_id).first()
#     service_requests = [request for request in service_requests]
#     response = {
#         "customer_details": {
#             "customerid": customer_details.customerid,
#             "firstname": customer_details.firstname,
#             "lastname": customer_details.lastname,
#             # Add more customer details as needed
#         },
#         "service_requests": service_requests,
#     }
#     return response
###########################################################################################


@app.get("/service_requests/{customer_id}", tags=["ServiceRequests"])
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    service_requests = db.query(ServiceRequest).filter(ServiceRequest.customerid == customer_id).options(subqueryload(ServiceRequest.customer))
    service_requests = service_requests.all()
    if not service_requests:
        raise HTTPException(status_code=404, detail="No service requests found for the provided customer.")
    response = {
        "service_requests": []
    }
    for request in service_requests:
        customer_details = request.customer
        response["service_requests"].append({
            "ticketid": request.ticketid,
            "customer_details": {
                "customerid": customer_details.customerid,
                "firstname": customer_details.firstname,
                "lastname": customer_details.lastname,
                # Add more customer details as needed
            },
            "description":request.description,
            "ticketstatus":request.ticketstatus
        })
    return response
@app.get('/service_requests_by_staff/{staff_id}', tags=["ServiceRequests"])
async def get_service_requests_by_staff(staff_id: int, db: Session = Depends(get_db)):
    service_requests = db.query(ServiceRequest).filter(ServiceRequest.staffid == staff_id).options(subqueryload(ServiceRequest.customer))
    service_requests = service_requests.all()
    if not service_requests:
        raise HTTPException(status_code=404, detail=f"No service requests found for the staff with staff_id: {staff_id}")
    response = {
        "service_requests": []
    }
    for request in service_requests:
        customer_details = request.customer
        response["service_requests"].append({
            "ticketid": request.ticketid,
            "customer_details": {
                "customerid": customer_details.customerid,
                "firstname": customer_details.firstname,
                "lastname": customer_details.lastname,
                # Add more customer details as needed
            }
        })

    return response

    # customer_subquery = db.query(Customer).filter(Customer.customerid == customer_id).subquery()
    # service_requests = db.query(ServiceRequest).join(customer_subquery, ServiceRequest.customerid == customer_subquery.c.customerid)
    # service_requests = service_requests.all()
    # if not service_requests:
    #     raise HTTPException(status_code=404, detail="No service requests found for the provided customer.")
    # customer_details = db.query(Customer).filter(Customer.customerid == customer_id).first()
    # service_requests = [request for request in service_requests]
    # response = {
    #     "customer_details": {
    #         "customerid": customer_details.customerid,
    #         "firstname": customer_details.firstname,
    #         "lastname": customer_details.lastname,
    #         # Add more customer details as needed
    #     },
    #     "service_requests": service_requests,
    # }
    # return response



    # customer = db.query(ServiceRequest,Customer).join(Customer,ServiceRequest.customerid == Customer.customerid).filter(Customer.customerid == customer_id).options(joinedload(ServiceRequest.customer))
    # service_requests=customer.all()
    # if service_requests is None:
    #     raise HTTPException(status_code=404, detail="Ticket Not Found")
    # cust_details=service_requests[0].customer
    # service_requests = [request for request in service_requests]
    # print(service_requests)
    # response = {
    #     "customer_details": {
    #         "customerid": cust_details.customerid,
    #         "firstname": cust_details.firstname,
    #         "lastname": cust_details.lastname,
    #         # Add more customer details as needed
    #     },
    #     "service_requests": service_requests,
    # }
    # return response


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


# @app.get("/staff/{staff_id}", tags=["Staff"])
# def get_customer_by_id(staff_id: int, db: Session = Depends(get_db)):
#     staff_requests = db.query(Staff).filter(Staff.staffid == staff_id).options(subqueryload(Staff.service_requests))
#     staff = staff_requests.first()
#     if not staff:
#         raise HTTPException(status_code=404, detail="No service requests found for the provided customer.")
#     service_request=[]
#     for request in staff.service_requests:
#         customer_details = request.customer
#         service_request.append({
#             "ticketid": request.ticketid,
#             "customer_details": {
#                 "customerid": customer_details.customerid,
#                 "firstname": customer_details.firstname,
#                 "lastname": customer_details.lastname,
#                 # Add more customer details as needed
#             }
#         })
#     response = {
#         "staff_name": f"{staff.firstname} {staff.lastname}",
#         "service_requests": service_request
#     }
#     return response


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
# @app.get("/phone_numbers/{customer_id}",tags=["Staff"])
# def get_staff_by_id(customerid: int, db: Session = Depends(get_db)):
#     staff = db.query(PhoneNumber).filter(PhoneNumber.customer == customerid).first()
#     if staff is None:
#         raise HTTPException(status_code=404, detail="PhoneNumber not found")
#     return staff

@app.get("/phone_numbers/{customer_id}", tags=["PhoneNumber"])
async def get_customer_bills(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.customerid == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found.")
    customer_bills = []
    for phone_number in customer.phone_numbers:
        customer_bills.append({
                "phone_number_id": phone_number.phone_number,
                "type": phone_number.type,
                "plan": phone_number.plan
            })

    return {"phone_numbers": customer_bills}


@app.post("/bills/", response_model=BillResponseModel,tags=["Bill"])
def create_bill(bill: BillResponseModel, db: Session = Depends(get_db)):
    db_bill = Bill(**bill.dict())
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill
#get all staffs
# @app.get('/bills/',tags=["Bill"])
# async def get_all_bills(db:Session=Depends(get_db)):
#     res=db.query(Bill).all()
#     return res

@app.get('/bills/',tags=["Bill"])
async def get_all_bills(db:Session=Depends(get_db)):
    bills = db.query(Bill).options(
        subqueryload(Bill.phone_number).subqueryload(PhoneNumber.customer)
    ).all()
    response = []
    for bill in bills:
        phone_number = bill.phone_number
        customer = phone_number.customer if phone_number else None

        bill_data = {
            "bill_id": bill.billid,
            "amount": bill.amount,
            "phone_number": {
                "phone_number_id": phone_number.phone_number if phone_number else None,
                "type": phone_number.type if phone_number else None,
                "plan": phone_number.plan if phone_number else None,
                "customer_details": {
                    "customer_id": customer.customerid if customer else None,
                    "firstname": customer.firstname if customer else None,
                    "lastname": customer.lastname if customer else None,
                    # Add more customer details as needed
                } if customer else None
            }
        }

        response.append(bill_data)
        return response


# @app.get("/bills/{bill_id}",tags=["Bill"])
# def get_bill_by_id(billid: int, db: Session = Depends(get_db)):
#     staff = db.query(Bill).filter(Bill.billid == billid).first()
#     if staff is None:
#         raise HTTPException(status_code=404, detail="Bill not found")
#     return staff


@app.get("/bills/{bill_id}",tags=["Bill"])
def get_bill_by_id(bill_id: int, db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(Bill.billid == bill_id).first()
    if bill is None:
        raise HTTPException(status_code=404, detail="Bill not found")
    phone_number = bill.phone_number
    customer = phone_number.customer if phone_number else None
    response = {
        "bill_id": bill.billid,
        "amount": bill.amount,
        "phone_number": {
            "phone_number_id": phone_number.phone_number if phone_number else None,
            "type": phone_number.type if phone_number else None,
            "plan": phone_number.plan if phone_number else None,
            "customer_details": {
                "customer_id": customer.customerid if customer else None,
                "firstname": customer.firstname if customer else None,
                "lastname": customer.lastname if customer else None,
                # Add more customer details as needed
            } if customer else None
        }
    }
    return response 

@app.get('/bill/{customer_id}', tags=["Bill"])
async def get_bills_by_customer(customer_id: int, db: Session = Depends(get_db)):
    bills = db.query(Bill).join(PhoneNumber).filter(PhoneNumber.customerid == customer_id).options(subqueryload(Bill.phone_number))
    bills = bills.all()

    customer_bills = []
    for bill in bills:
        phone_number = bill.phone_number 
        customer_bills.append({
            "bill_id": bill.billid,
            "amount": bill.amount,
            "phone_number": {
                "phone_number_id": phone_number.phone_number,
                "type": phone_number.type,
                "plan": phone_number.plan,
            }
        })

    return {"customer_bills": customer_bills}
    # bill = db.query(Bill).filter(Bill.billid == bill_id).options(
    #     subqueryload(Bill.phone_number).subqueryload(PhoneNumber.customer)
    # ).first()
    # if bill is None:
    #     raise HTTPException(status_code=404, detail="Bill not found")
    # phone_number = bill.phone_number
    # customer = phone_number.customer
    # response = {
    #     "bill_id": bill.billid,
    #     "amount": bill.amount,
    #     "phone_number": {
    #         "phone_number_id": phone_number.phone_number,
    #         "type": phone_number.type,
    #         "plan": phone_number.plan,
    #         "customer_details": {
    #             "customer_id": customer.customerid,
    #             "firstname": customer.firstname,
    #             "lastname": customer.lastname,
    #             # Add more customer details as needed
    #         }
    #     }
    # }
    # return response



@app.delete("/bills/{bill_id}",tags=["Bill"])
def delete_customer(bill_id: int, db: Session = Depends(get_db)):
    customer = db.query(Bill).filter(Bill.billid== bill_id).delete()
    db.commit()
    if not customer:
        raise HTTPException(status_code=404, detail="Staffid not found")
    return {f"Bill id {bill_id} is deleted successfully"}