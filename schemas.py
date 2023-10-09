from pydantic import BaseModel

class CustomerCreate(BaseModel):
    custid:int
    lastname: str
    firstname: str
    idf_proof: str
    idnumber: str
    phone_number_id: int
    address: str
    dob: str
    
class CustomerResponse(BaseModel):
    custid: int
    lastname: str
    firstname: str
    idf_proof: str
    idnumber: str
    phone_number_id: int
    address: str
    dob: str


class TicketCreate(BaseModel):
    Ticketid:int
    phone_number_id: int
    custid: int
    staffid: int
    TicketStatus: str
    Description: str

class TicketResponse(BaseModel):
    Ticketid: int
    phone_number_id: int
    custid: int
    staffid: int
    TicketStatus: str
    Description: str
    
    
class StaffCreate(BaseModel):
    staffid:int
    address: str
    idproof: str
    idnumber: str
    firstname: str
    lastname: str

class StaffResponse(BaseModel):
    staffid: int
    address: str
    idproof: str
    idnumber: str
    firstname: str
    lastname: str

class PhoneNumberCreate(BaseModel):
    phone_number:int
    type: str
    plan: str

class PhoneNumberResponse(BaseModel):
    phone_number: int
    type: str
    plan: str

class BillCreate(BaseModel):
    Billid:int
    phone_number_id: int
    Amount: int

class BillResponse(BaseModel):
    Billid: int
    phone_number_id: int
    Amount: int