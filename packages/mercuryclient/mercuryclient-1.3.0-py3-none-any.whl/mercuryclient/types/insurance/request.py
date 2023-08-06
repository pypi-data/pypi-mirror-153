from dataclasses import field
from typing import List, Optional
from pydantic import BaseModel
from pydantic import Field


class Premium(BaseModel):

    amount: int


class Customer(BaseModel):

    id: Optional[str] = Field(max_length=50)
    name: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    email: Optional[str] = Field(max_length=50)
    state: str = Field(max_length=50)


class AccountData(BaseModel):

    number: str = Field(max_length=50)
    ifsc: str = Field(max_length=50)
    category: Optional[str] = Field(max_length=50)


class Insured(BaseModel):

    name: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    email: str = Field(max_length=50)
    pincode: Optional[str] = Field(max_length=50)
    city: Optional[str] = Field(max_length=50)
    address: Optional[str] = Field(max_length=50)
    gender: Optional[str] = Field(max_length=50)
    occupation: Optional[str] = Field(max_length=50)
    age: int = Field(min=18, max=50)
    dob: str = Field(max_length=50)
    account: AccountData


class Nominee(BaseModel):

    name: str = Field(max_length=50)
    relationship: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    dob: Optional[str] = Field(max_length=50)


class PersonData(BaseModel):
    insured: Insured
    nominee: Nominee


class LoanData(BaseModel):

    amount: int
    provider_id: int
    provider_name: str = Field(max_length=50)
    start_date: str = Field(max_length=50)
    end_date: str = Field(max_length=50)
    emi_amount: Optional[int]
    hospicash_amount: Optional[int]
    disbursement_date: str = Field(max_length=50)
    account_number: str = Field(max_length=50)
    tenure_in_months: int
    type: Optional[str] = Field(max_length=50)
    family_type: str = Field(max_length=50)
    application_number: str = Field(max_length=50)
    person: List[PersonData]


class AdditionalInfo(BaseModel):

    declaration_health: str = Field(max_length=4)
    assignment_clause: str = Field(max_length=4)
    collection_status: str = Field(max_length=4)


class InsuranceRequest(BaseModel):

    plan: str = Field(max_length=50)
    partner_id: str = Field(max_length=50)
    plan_type: int
    reference_id: str = Field(max_length=50)
    category: str = Field(max_length=50)
    premium: Premium
    customer: Customer
    loan: LoanData
    additional_info: AdditionalInfo
