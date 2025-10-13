from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, computed_field, Field
import json
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the Patient', example='P001')]
    name: Annotated[str, Field(..., description='Name of the Patient')]
    city: Annotated[str, Field(..., description='City of the Patient')]
    age: Annotated[int, Field(..., get=0, description='Age of the Patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the patient in kgs')]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'obese'
  

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get('/')
def hello():
    return {'message': 'Patient Management System API'}

@app.post('/create')
def create(patient: Patient):
    # load data
    data = load_data()
    
    #check if patient already exists in the database
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f'Patient with ID: {patient.id} already exists') 
    
    # if patient doesn't exists in the database
    data[patient.id] = patient.model_dump(exclude=['id']) 
    
    # save the patient into database
    save_data(data)
    
    #return the json response of sucessfull creation
    return JSONResponse(status_code=201, content={'message': 'patient created successfully'})

    