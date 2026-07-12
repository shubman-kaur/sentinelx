from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI(title="SentinelX Central Intelligence Engine")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for hackathon/demo purposes; restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


SCAM_API_URL = "http://127.0.0.1:8000/predict-scam"
INVESTIGATION_API_URL = "http://127.0.0.1:8001/investigate"
CURRENCY_API_URL = "http://127.0.0.1:8002/predict-currency"  


SCAM_WEIGHT = 0.40
INVESTIGATION_WEIGHT = 0.35
CURRENCY_WEIGHT = 0.25


def get_threat_level(score):
    """Maps a 0-100 risk score to a threat level and recommended action"""
    if score >= 80:
        return "Critical", "Immediate action required. Do not engage further. Report to cybercrime.gov.in or call 1930 immediately."
    elif score >= 60:
        return "High", "Strong signs of fraud. Avoid sharing any information and report to authorities."
    elif score >= 35:
        return "Medium", "Exercise caution. Verify the identity/source independently before taking any action."
    else:
        return "Low", "No strong signs of fraud detected. Stay generally alert."


@app.post("/analyze")
def analyze(text: str = Form(...), currency_image: Optional[UploadFile] = File(None)):
    """
    Combines Scam Classifier, Investigation Copilot, and (optionally) Currency
    Detector outputs into a single weighted risk score and threat level.
    """

    
    scam_response = requests.post(SCAM_API_URL, json={"text": text})
    scam_response.raise_for_status()
    scam_data = scam_response.json()
    scam_score = scam_data["scam_probability"] * 100  # convert to 0-100 scale

   
    investigation_response = requests.post(INVESTIGATION_API_URL, json={"text": text})
    investigation_response.raise_for_status()
    investigation_data = investigation_response.json()
    investigation_score = investigation_data["scam_probability"] * 100  # same underlying score, but validated via RAG context

    currency_score = None
    if currency_image is not None:
        files = {"file": (currency_image.filename, currency_image.file, currency_image.content_type)}
        currency_response = requests.post(CURRENCY_API_URL, files=files)
        currency_response.raise_for_status()
        currency_data = currency_response.json()
        
        if currency_data["verdict"] == "Fake":
            currency_score = currency_data["confidence"] * 100
        else:
            currency_score = (1 - currency_data["confidence"]) * 100

   
    if currency_score is not None:
       
        weighted_score = (
            scam_score * SCAM_WEIGHT +
            investigation_score * INVESTIGATION_WEIGHT +
            currency_score * CURRENCY_WEIGHT
        )
    else:
       
        total_remaining_weight = SCAM_WEIGHT + INVESTIGATION_WEIGHT
        adjusted_scam_weight = SCAM_WEIGHT / total_remaining_weight
        adjusted_investigation_weight = INVESTIGATION_WEIGHT / total_remaining_weight

        weighted_score = (
            scam_score * adjusted_scam_weight +
            investigation_score * adjusted_investigation_weight
        )

    weighted_score = round(weighted_score, 2)
    threat_level, recommended_action = get_threat_level(weighted_score)

    return {
        "unified_risk_score": weighted_score,
        "threat_level": threat_level,
        "recommended_action": recommended_action,
        "component_scores": {
            "scam_classifier": round(scam_score, 2),
            "investigation_copilot": round(investigation_score, 2),
            "currency_detector": round(currency_score, 2) if currency_score is not None else "Not provided"
        },
        "investigation_report": investigation_data["report"],
        "red_flags_detected": scam_data["red_flags_detected"]
    }