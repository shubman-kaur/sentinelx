"""
FastAPI endpoint for Scam Classifier
- Takes raw text (SMS/call transcript) as input
- Detects red flags using red_flags.py
- Transforms text using the saved TF-IDF vectorizer
- Combines TF-IDF + red flags -> feeds to trained LightGBM model
- Returns scam/normal verdict + confidence + which red flags fired
"""

from fastapi import FastAPI
from pydantic import BaseModel
import scipy.sparse as sp
import joblib

from red_flags import detect_red_flags

app = FastAPI()


model = joblib.load("data/scam_classifier_model.pkl")
vectorizer = joblib.load("data/tfidf_vectorizer.pkl")


RED_FLAG_ORDER = [
    "Fake Authority Claim",
    "Threat Language",
    "Payment Pressure",
    "Remote Access Request",
    "OTP Request",
    "Isolation Tactics"
]


class ScamCheckRequest(BaseModel):
    text: str

@app.post("/predict-scam")
def predict_scam(request: ScamCheckRequest):
    text = request.text

    
    flags_dict = detect_red_flags(text)
    flags_list = [flags_dict[flag] for flag in RED_FLAG_ORDER]

    
    text_tfidf = vectorizer.transform([text])

    
    flags_sparse = sp.csr_matrix([flags_list])
    final_features = sp.hstack([text_tfidf, flags_sparse])

    prediction = model.predict(final_features)[0]          # 0 = normal, 1 = scam
    probability = model.predict_proba(final_features)[0][1]  # probability of being scam

    verdict = "scam" if prediction == 1 else "normal"

    return {
        "verdict": verdict,
        "scam_probability": round(float(probability), 4),
        "red_flags_detected": flags_dict
    }