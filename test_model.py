from ultralytics import YOLO
import random
import os


model = YOLO("runs/classify/currency_classifier/weights/best.pt")


val_dir = "dataset/split/val"


classes = ["real", "fake"]

for cls in classes:
    folder_path = os.path.join(val_dir, cls)
    images = os.listdir(folder_path)
    
    
    sample_images = random.sample(images, min(3, len(images)))
    
    print(f"\n{'='*50}")
    print(f"Testing {cls.upper()} images (actual label: {cls})")
    print(f"{'='*50}")
    
    for img_name in sample_images:
        img_path = os.path.join(folder_path, img_name)
        results = model(img_path, verbose=False)
        
       
        pred_class = results[0].names[results[0].probs.top1]
        confidence = results[0].probs.top1conf.item()
        
        print(f"Image: {img_name}")
        print(f"  Actual: {cls} | Predicted: {pred_class} | Confidence: {confidence:.4f}")