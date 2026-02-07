from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic_settings import BaseSettings,  SettingsConfigDict

class Settings(BaseSettings):
    api_key: str
    
    model_config = SettingsConfigDict(env_file='.env')
        
settings = Settings()
app = FastAPI()

def get_api_key(api_key: str = Header(...)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=403, detail='Unauthorized')
    return api_key

@app.get('/get-data')
def get_data(api_key: str = Depends(get_api_key)):
    return {'output': 'Access Granted'}