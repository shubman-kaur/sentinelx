"""
Step: Detailed Evaluation of Scam Classifier
- Precision, Recall, F1-score (per class)
- Confusion Matrix
- Why these matter more than plain accuracy on imbalanced data
"""

import pandas as pd
import scipy.sparse as sp
import joblib
from sklearn.metrics import classification_report, confusion_matrix

# 1. Load test features, true labels, and the trained model
X_test = sp.load_npz("X_test_final.npz")
y_test = pd.read_csv("y_test.csv")["label_num"]

model = joblib.load("scam_classifier_model.pkl")

# 2. Get predictions on test set
y_pred = model.predict(X_test)

# 3. Classification report -> precision, recall, f1-score per class
#    target_names makes the output readable (0 = normal, 1 = scam)
print("=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=["normal", "scam"]))

# 4. Confusion Matrix
#    Rows = actual class, Columns = predicted class
#    [ [TN, FP],
#      [FN, TP] ]
cm = confusion_matrix(y_test, y_pred)
print("=== Confusion Matrix ===")
print("                Predicted Normal   Predicted Scam")
print(f"Actual Normal        {cm[0][0]:<15}   {cm[0][1]}")
print(f"Actual Scam          {cm[1][0]:<15}   {cm[1][1]}")

print("\nTN (correctly said normal):", cm[0][0])
print("FP (said scam, was actually normal):", cm[0][1])
print("FN (said normal, was actually SCAM - dangerous!):", cm[1][0])
print("TP (correctly caught scam):", cm[1][1])