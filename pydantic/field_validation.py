from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List , Dict, Optional, Annotated

class Patient(BaseModel):
    # name: str = Field(max_length=50)
    name: Annotated[str, Field(max_length=10, title='Name of the patient', description='Name must be within 50 characters', examples=['Divyanshu', 'Nitish'])]
    email: EmailStr
    website: Optional[AnyUrl] = None
    age: int = Field(gt=0, le=100)
    weight: float = Annotated[float, Field(gt=0, strict=True)]
    # married: Optional[bool] = False
    married: Annotated[bool, Field(defulat=None, description='Is the Patient Married?')]
    allergies: Optional[List[str]] = Annotated[None, Field(max_length=5)]
    contact_details: Dict[str, str]
    
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
    

patient_info = {'name': 'Divyanshu', 'email': 'abc@gmail.com','age': 22, 'weight': 62.00, 'contact_details': {'phone_no': '12345678'}}
patient1 = Patient(**patient_info)

insert_patient_data(patient1)


# update_patient_data(patient1)