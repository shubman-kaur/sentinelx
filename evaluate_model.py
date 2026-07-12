from ultralytics import YOLO


model = YOLO("runs/classify/currency_classifier/weights/best.pt")

metrics = model.val(data="dataset/split", split="val")

print("\n" + "="*50)
print("FULL VALIDATION RESULTS")
print("="*50)
print(f"Top-1 Accuracy: {metrics.top1:.4f}")
print(f"Top-5 Accuracy: {metrics.top5:.4f}")