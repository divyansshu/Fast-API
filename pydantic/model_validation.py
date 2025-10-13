from pydantic import BaseModel, EmailStr, model_validator, field_validator
from typing import List , Dict

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]
    
    
    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, value):
        print(type(value))
        return value
            
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model
    

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.email)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    
def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    

patient_info = {'name': 'Divyanshu', 'email': 'abc@icic.com','age': '65', 'weight': 62.00, 'married': False, 'allergies': ['None'], 'contact_details': {'phone_no': '12345678', 'emergency': '23456789'}}
patient1 = Patient(**patient_info)

insert_patient_data(patient1)


# update_patient_data(patient1)