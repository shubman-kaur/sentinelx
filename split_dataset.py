import os
import shutil
import random


SOURCE = "dataset/archive/data/data"
DEST = "dataset/split"
SPLIT_RATIO = 0.8 

random.seed(42)

classes = ["real", "fake"]

for cls in classes:
    src_class_path = os.path.join(SOURCE, cls)
    denominations = os.listdir(src_class_path)

    for denom in denominations:
        denom_path = os.path.join(src_class_path, denom)
        if not os.path.isdir(denom_path):
            continue

        images = [f for f in os.listdir(denom_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        random.shuffle(images)

        split_index = int(len(images) * SPLIT_RATIO)
        train_images = images[:split_index]
        val_images = images[split_index:]

        train_dest = os.path.join(DEST, "train", cls)
        val_dest = os.path.join(DEST, "val", cls)
        os.makedirs(train_dest, exist_ok=True)
        os.makedirs(val_dest, exist_ok=True)

        
        for img in train_images:
            shutil.copy(os.path.join(denom_path, img), os.path.join(train_dest, f"{denom}_{img}"))

        for img in val_images:
            shutil.copy(os.path.join(denom_path, img), os.path.join(val_dest, f"{denom}_{img}"))

        print(f"{cls}/{denom}: {len(train_images)} train, {len(val_images)} val")

print("\n✅ Dataset split complete!")