from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()


# user readable
@app.get('/')
def home():
    return {'message': 'Insurance Premium Claim Prediction API'}

# machine readable
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model loaded': model is not None
        
    }

@app.post('/predict')
def predict_premium(data: UserInput):
    user_input = {
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
    }
    
    try:
        prediction = predict_output(user_input)
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    
    except Exception as e:
        return JSONResponse(status_code=500, content=str(e))
    
    