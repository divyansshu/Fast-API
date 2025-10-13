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

temp = patient1.model_dump() # store model as dictionary 
temp2 = patient1.model_dump_json() # store model as json

temp3 = patient1.model_dump(include=['name', 'age'])
temp4 = patient1.model_dump(exclude=['name', 'age'])

print(temp)
print(temp2)
print(type(temp))
print(type(temp2))

print(temp3)
print(temp4)
    