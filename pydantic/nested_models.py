from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin: str

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address 
    
address_dict = {'city': 'gurgoan', 'state': 'haryana', 'pin': '122001'}
address1 = Address(**address_dict)

patient_dict = {'name': 'Divyanshu', 'age': 22, 'gender': 'Male', 'address': address1} 

patient1 = Patient(**patient_dict)

print(patient1.name)
print(patient1.address.city)
print(patient1.address.state)
print(patient1.address.pin)
    