import pickle
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "model.pkl"
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0'
class_labels = model.classes_.tolist()

def predict_output(user_input: dict) -> dict:
    df = pd.DataFrame([user_input])
    predicted = model.predict(df)[0]
    probs = model.predict_proba(df)[0]
    return {
        'predicted_risk': str(predicted),
        'confidence': round(float(max(probs)), 4),
        'class_probabilities': {label: round(float(p), 4) for label, p in zip(class_labels, probs)}
    }