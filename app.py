from fastapi import FastAPI, HTTPException
from schema.user_input import LoanApplicant
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Loan Risk Prediction API'}

@app.get('/health')
def health_check():
    return {'status': 'OK', 'version': MODEL_VERSION, 'model_loaded': model is not None}

@app.post('/predict', response_model=PredictionResponse)
def predict_risk(data: LoanApplicant):
    user_input = {
        'age': data.age,
        'monthly_income': data.monthly_income,
        'loan_amount': data.loan_amount,
        'loan_term_months': data.loan_term_months,
        'existing_loans': data.existing_loans,
        'credit_history': data.credit_history,
        'employment_type': data.employment_type,
        'debt_to_income': data.debt_to_income
    }
    try:
        return predict_output(user_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))