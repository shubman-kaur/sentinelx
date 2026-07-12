"""
Step: Train LightGBM Classifier
- Uses TF-IDF + red flag features saved in previous step
- Handles class imbalance using class_weight='balanced'
- Saves trained model for evaluation + FastAPI use
"""

import pandas as pd
import scipy.sparse as sp
import joblib
import lightgbm as lgb

# 1. Load features and labels saved from previous step
X_train = sp.load_npz("X_train_final.npz")
X_test = sp.load_npz("X_test_final.npz")

y_train = pd.read_csv("y_train.csv")["label_num"]
y_test = pd.read_csv("y_test.csv")["label_num"]

print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# 2. Define LightGBM model
#    class_weight='balanced' -> automatically gives more weight to the
#    minority class (scam) so the model doesn't just predict "normal" always
model = lgb.LGBMClassifier(
    n_estimators=200,
    learning_rate=0.05,
    class_weight="balanced",
    random_state=42
)

# 3. Train the model
model.fit(X_train, y_train)

# 4. Quick check on training accuracy (just a sanity check, real eval is next step)
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)

print("\nTrain accuracy:", train_accuracy)
print("Test accuracy:", test_accuracy)

# 5. Save the trained model
joblib.dump(model, "scam_classifier_model.pkl")

print("\nSaved: scam_classifier_model.pkl")