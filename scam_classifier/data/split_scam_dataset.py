"""
Step: Train/Test Split for Scam Classifier
- Stratified split to preserve scam:normal ratio in both sets
- Saves train.csv and test.csv for next step (TF-IDF + LightGBM)
"""

import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load the combined dataset
df = pd.read_csv("combined_scam_dataset.csv")

print("Total rows:", len(df))
print("\nLabel distribution (full dataset):")
print(df["label"].value_counts())

# 2. Stratified split — 80% train, 20% test
#    stratify=df["label"] ensures scam:normal ratio stays same in both splits
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42,       # fixed seed -> reproducible split (important for interviews too!)
    stratify=df["label"]
)

print("\nTrain size:", len(train_df))
print("Train label distribution:")
print(train_df["label"].value_counts(normalize=True))

print("\nTest size:", len(test_df))
print("Test label distribution:")
print(test_df["label"].value_counts(normalize=True))

# 3. Save splits
train_df.to_csv("train.csv", index=False)
test_df.to_csv("test.csv", index=False)
print("\nSaved: data/train.csv and data/test.csv")