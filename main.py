from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
from PIL import Image
import io


app = FastAPI(title="SentinelX - Currency Detector API")


model = YOLO("runs/classify/currency_classifier/weights/best.pt")

@app.get("/")
def read_root():
    return {"message": "SentinelX Currency Detector API is running"}

@app.post("/predict-currency")
async def predict_currency(file: UploadFile = File(...)):
    
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Run prediction
    results = model(image, verbose=False)
    
   
    pred_class = results[0].names[results[0].probs.top1]
    confidence = results[0].probs.top1conf.item()
    
    
    verdict = "Real" if pred_class == "real" else "Fake"
    
    return {
        "filename": file.filename,
        "verdict": verdict,
        "confidence": round(confidence, 4)
    }