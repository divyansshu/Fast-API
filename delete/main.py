from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, computed_field, Field
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional, Annotated, Literal
import json

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

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    
    data = load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient_not_found')
    
    del data[patient_id]
    save_data(data) 
    
    return JSONResponse(status_code=200, content={'message': 'patient deleted'})
    