from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from config.city_tier import tier1, tier2

# pydantic model to validate  incoming data
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, description='Age of the user')]
    sex: Annotated[str, Field(..., description='Gender of the user')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the user')]
    bmi: Annotated[float, Field(..., gt=0, description='BMI of the user')]
    hereditary_diseases: Annotated[Literal['NoDisease', 'Epilepsy', 'EyeDisease', 'Alzheimer', 'Arthritis',
       'HeartDisease', 'Diabetes', 'Cancer', 'High BP', 'Obesity'], bool, Field(...,description='any disease user has?')]
    no_of_dependents: Annotated[int, Field(..., description='no. of people who depend on the user for livelihood')]
    smoker: Annotated[int, Field(..., description='user smokes or not')]
    city: Annotated[Literal['NewYork', 'Boston', 'Phildelphia', 'Pittsburg', 'Buffalo',
       'AtlanticCity', 'Portland', 'Cambridge', 'Hartford', 'Springfield',
       'Syracuse', 'Baltimore', 'York', 'Trenton', 'Warwick',
       'WashingtonDC', 'Providence', 'Harrisburg', 'Newport', 'Stamford',
       'Worcester', 'Atlanta', 'Brimingham', 'Charleston', 'Charlotte',
       'Louisville', 'Memphis', 'Nashville', 'NewOrleans', 'Raleigh',
       'Houston', 'Georgia', 'Oklahoma', 'Orlando', 'Macon', 'Huntsville',
       'Knoxville', 'Florence', 'Miami', 'Tampa', 'PanamaCity',
       'Kingsport', 'Marshall', 'Mandan', 'Waterloo', 'IowaCity',
       'Columbia', 'Indianapolis', 'Cincinnati', 'Bloomington', 'Salina',
       'KanasCity', 'Brookings', 'Minot', 'Chicago', 'Lincoln',
       'FallsCity', 'GrandForks', 'Fargo', 'Cleveland', 'Canton',
       'Columbus', 'Rochester', 'Minneapolis', 'JeffersonCity',
       'Escabana', 'Youngstown', 'SantaRosa', 'Eureka', 'SanFrancisco',
       'SanJose', 'LosAngeles', 'Oxnard', 'SanDeigo', 'Oceanside',
       'Carlsbad', 'Montrose', 'Prescott', 'Fresno', 'Reno', 'LasVegas',
       'Tucson', 'SanLuis', 'Denver', 'Kingman', 'Bakersfield',
       'Mexicali', 'SilverCity', 'Pheonix', 'SantaFe', 'Lovelock'],str, Field(..., description='city of user')]
    bloodpressure: Annotated[int, Field(..., gt=0, description='blood pressure of user')]
    diabetes: Annotated[int, Field(..., description='user has diabetes or not')]
    regular_ex: Annotated[int, Field(..., description='user do regular excercise or not')]
    job_title: Annotated[Literal['Actor', 'Engineer', 'Academician', 'Chef', 'HomeMakers', 'Dancer',
       'Singer', 'DataScientist', 'Police', 'Student', 'Doctor',
       'Manager', 'Photographer', 'Beautician', 'CA', 'Blogger', 'CEO',
       'Labourer', 'Accountant', 'FilmDirector', 'Technician',
       'FashionDesigner', 'Architect', 'HouseKeeper', 'FilmMaker',
       'Buisnessman', 'Politician', 'DefencePersonnels', 'Analyst',
       'Clerks', 'ITProfessional', 'Farmer', 'Journalist', 'Lawyer',
       'GovEmployee'],str, Field(...,description='job title of user')]
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v
    
    
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
        elif self.city in tier2:
            return 2
        else:
            return 3