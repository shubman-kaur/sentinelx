"""
Step: TF-IDF Vectorization + Combine with Red Flag Features
- Fit TF-IDF only on train data (avoid data leakage)
- Transform both train and test using that same fitted vectorizer
- Combine TF-IDF features with the 6 red flag columns
- Save everything needed for LightGBM training (next step)
"""

import pandas as pd
import scipy.sparse as sp
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. Load train and test data (already split earlier)
train_df = pd.read_csv("train.csv")
test_df = pd.read_csv("test.csv")

print("Train rows:", len(train_df))
print("Test rows:", len(test_df))

# 2. Convert label to numeric: scam -> 1, normal -> 0
train_df["label_num"] = (train_df["label"] == "scam").astype(int)
test_df["label_num"] = (test_df["label"] == "scam").astype(int)

# 3. TF-IDF Vectorization
#    max_features: limit vocabulary size to avoid too many sparse columns
#    stop_words='english': ignore common words like "the", "is", "a"
vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")

# IMPORTANT: fit only on train text, then transform both train and test
X_train_tfidf = vectorizer.fit_transform(train_df["text"].fillna(""))
X_test_tfidf = vectorizer.transform(test_df["text"].fillna(""))

print("\nTF-IDF train shape:", X_train_tfidf.shape)
print("TF-IDF test shape:", X_test_tfidf.shape)

# 4. Red flag columns (already numeric 0/1 in the CSV)
red_flag_cols = [
    "Fake Authority Claim",
    "Threat Language",
    "Payment Pressure",
    "Remote Access Request",
    "OTP Request",
    "Isolation Tactics"
]

X_train_flags = sp.csr_matrix(train_df[red_flag_cols].values)
X_test_flags = sp.csr_matrix(test_df[red_flag_cols].values)

# 5. Combine TF-IDF features + red flag features (horizontal stack)
X_train_final = sp.hstack([X_train_tfidf, X_train_flags])
X_test_final = sp.hstack([X_test_tfidf, X_test_flags])

print("\nFinal train feature shape (TF-IDF + red flags):", X_train_final.shape)
print("Final test feature shape (TF-IDF + red flags):", X_test_final.shape)

# 6. Save everything needed for the next step (LightGBM training)
sp.save_npz("X_train_final.npz", X_train_final)
sp.save_npz("X_test_final.npz", X_test_final)

train_df["label_num"].to_csv("y_train.csv", index=False)
test_df["label_num"].to_csv("y_test.csv", index=False)

# Save the fitted vectorizer too -> needed later for FastAPI endpoint
# (so new incoming text can be transformed the same way)
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("\nSaved: X_train_final.npz, X_test_final.npz, y_train.csv, y_test.csv, tfidf_vectorizer.pkl")