from pydantic import BaseModel, EmailStr, computed_field
from typing import List , Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    height: float
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi(self)-> float:
        BMI = (self.weight/(self.height**2))
        return round(BMI, 2)



def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.height)
    print(patient.weight)
    print(patient.bmi)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    

patient_info = {'name': 'Divyanshu', 'email': 'abc@icic.com','age': '65','height':1.65, 'weight': 62.00, 'married': False, 'allergies': ['None'], 'contact_details': {'phone_no': '12345678', 'emergency': '23456789'}}
patient1 = Patient(**patient_info)

insert_patient_data(patient1)

