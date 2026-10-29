import pickle
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "loan_applicants.json"
MODEL_PATH = BASE_DIR / "model" / "model.pkl"

# 1. Data load
df = pd.read_json(DATA_PATH)

# 2. Feature engineering
df['monthly_installment'] = df['loan_amount'] / df['loan_term_months']
df['debt_to_income'] = df['monthly_installment'] / df['monthly_income']

# 3. Target banana (rules se)
def assign_risk(row):
    if row['debt_to_income'] > 0.5 or row['existing_loans'] >= 3:
        return "High"
    elif row['debt_to_income'] < 0.3 and row['credit_history'] == "good":
        return "Low"
    else:
        return "Medium"

df['loan_risk'] = df.apply(assign_risk, axis=1)
print(df['loan_risk'].value_counts())

# 4. Features aur target
categorical = ['credit_history', 'employment_type']
numeric = ['age', 'monthly_income', 'loan_amount', 'loan_term_months',
           'existing_loans', 'debt_to_income']
X = df[numeric + categorical]
y = df['loan_risk']

# 5. Pipeline
preprocessor = ColumnTransformer([
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
    ('num', 'passthrough', numeric)
])
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# 6. Train (sirf 20 rows hain, isliye poore data par)
pipeline.fit(X, y)
print("Training accuracy:", pipeline.score(X, y))

# 7. Save
with open(MODEL_PATH, 'wb') as f:
    pickle.dump(pipeline, f)
print("Model saved:", MODEL_PATH)