from fastapi import FastAPI, HTTPException, Header, Depends

app = FastAPI()

API_KEY = 'my_secret_key'

def get_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail='Unauthorized')
    return api_key

@app.get('/get-data')
def get_data(api_key: str = Depends(get_api_key)):
    return {'output': 'Access Granted'}