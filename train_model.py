from ultralytics import YOLO


model = YOLO("yolov8n-cls.pt")


results = model.train(
    data="dataset/split",   
    epochs=25,             
    imgsz=224,               
    batch=16,                 # how many images processed at once
    name="currency_classifier" 
)

print("\n✅ Training complete!")