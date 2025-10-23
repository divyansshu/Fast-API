from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pickle
import pandas as pd

# import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
 
app = FastAPI()

tier1 = [
    'NewYork', 'Boston', 'Philadelphia', 'WashingtonDC', 'Baltimore',
    'Atlanta', 'Charlotte', 'Miami', 'Tampa', 'Houston', 'Dallas',
    'Chicago', 'Minneapolis', 'SanFrancisco', 'SanJose', 'LosAngeles',
    'SanDiego', 'Phoenix', 'LasVegas', 'Denver', 'Portland', 'Orlando',
    'Nashville', 'NewOrleans', 'Cleveland', 'Columbus', 'Raleigh',
    'Louisville', 'KansasCity'
]

tier2 = [
    'Pittsburg', 'Buffalo', 'AtlanticCity', 'Cambridge', 'Hartford',
    'Springfield', 'Syracuse', 'York', 'Trenton', 'Warwick', 'Providence',
    'Harrisburg', 'Newport', 'Stamford', 'Worcester', 'Brimingham',
    'Charleston', 'Memphis', 'Macon', 'Huntsville', 'Knoxville',
    'Florence', 'PanamaCity', 'Kingsport', 'Marshall', 'Mandan',
    'Waterloo', 'IowaCity', 'Columbia', 'Indianapolis', 'Cincinnati',
    'Bloomington', 'Salina', 'Brookings', 'Minot', 'Lincoln', 'FallsCity',
    'GrandForks', 'Fargo', 'Canton', 'Rochester', 'JeffersonCity',
    'Escabana', 'Youngstown', 'SantaRosa', 'Eureka', 'Oxnard',
    'Oceanside', 'Carlsbad', 'Montrose', 'Prescott', 'Fresno', 'Reno',
    'Tucson', 'SanLuis', 'Kingman', 'Bakersfield', 'Mexicali', 'SilverCity',
    'SantaFe', 'Lovelock', 'Georgia', 'Oklahoma'
]


# pydantic model to validate  incoming data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, description='Age of the user')]
    sex: Annotated[str, Field(..., description='Gender of the user')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the user')]
    bmi: Annotated[float, Field(..., gt=0, description='BMI of the user')]
    hereditary_diseases: Annotated[bool, Field(..., gt=0, description='any disease user has?')]
    no_of_dependents: Annotated[int, Field(..., description='no. of people who depend on the user for livelihood')]
    smoker: Annotated[int, Field(..., description='user smokes or not')]
    city: Annotated[str, Field(..., description='city of user')]
    bloodpressure: Annotated[int, Field(..., gt=0, description='blood pressure of user')]
    diabetes: Annotated[int, Field(..., description='user has diabetes or not')]
    regular_ex: Annotated[int, Field(..., description='user do regular excercise or not')]
    job_title: Annotated[str, Field(..., gt=0, description='job title of user')]
    
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'
    
    @computed_field
    @property
    def age_group(self) -> str:
          if self.age < 25:
              return "young"
          elif self.age < 45:
              return "adult"
          elif self.age < 60:
              return "middle_aged"
          else: return "senior"
    
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier1:
            return 1
        else:
            return 2

@app.post('/predict')
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        'sex': data.sex,
        'bmi': data.bmi,
        'hereditary_diseases': data.hereditary_diseases,
        'no_of_dependents' : data.no_of_dependents,
        'bloodpressure' : data.bloodpressure,
        'diabetes' : data.diabetes,
        'regular_ex' : data.regular_ex,
        'job_title' : data.job_title,
        'age_group': data.age_group,
        'lifestyle_risk' : data.lifestyle_risk,
        'city_tier' : data.city_tier
    }])
    
    prediction = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={'predicted_category': prediction})
    
    
    