import json
import joblib
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).resolve().parents[1]
FEATURE_DIR = BASE_DIR / "features"
MODEL_DIR = BASE_DIR / "models"
EVAL_DIR = BASE_DIR / "evaluation"

MODEL_DIR.mkdir(exist_ok=True)
EVAL_DIR.mkdir(exist_ok=True)

# ---------------- LOAD DATA ----------------
X_train = np.load(FEATURE_DIR / "X_train.npy")
X_test = np.load(FEATURE_DIR / "X_test.npy")
y_train = np.load(FEATURE_DIR / "y_train.npy")
y_test = np.load(FEATURE_DIR / "y_test.npy")

# ---------------- MODELS ----------------
models = {
    "LogisticRegression": LogisticRegression(max_iter=1000),
    "RandomForest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        n_estimators=600,
        learning_rate=0.03,
        max_depth=6,
        min_child_weight=1,
        gamma=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        eval_metric="auc",
        random_state=42
    ),
    "NeuralNetwork": MLPClassifier(
        hidden_layer_sizes=(64, 32),
        max_iter=500,
        random_state=42
    )
}

metrics = {}
best_model = None
best_model_name = None
best_cv_roc = -1

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# ---------------- TRAIN & EVALUATE ----------------
for name, model in models.items():
    print("\n" + "=" * 45)
    print(f"Training Model: {name}")
    print("=" * 45)

    # ---- Cross-validated ROC-AUC (USED FOR SELECTION) ----
    cv_roc = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="roc_auc"
    ).mean()

    # ---- Train on full training set ----
    model.fit(X_train, y_train)

    # ---- Test predictions ----
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc = roc_auc_score(y_test, y_prob)

    print(f"Accuracy   : {acc:.4f}")
    print(f"Precision  : {prec:.4f}")
    print(f"Recall     : {rec:.4f}")
    print(f"F1 Score   : {f1:.4f}")
    print(f"ROC-AUC    : {roc:.4f}")
    print(f"CV ROC-AUC : {cv_roc:.4f}")

    metrics[name] = {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "roc_auc": roc,
        "cv_roc_auc": cv_roc
    }

    # ---- Select best model based on CV ROC-AUC ----
    if cv_roc > best_cv_roc:
        best_cv_roc = cv_roc
        best_model = model
        best_model_name = name

# ---------------- SAVE BEST MODEL ----------------
joblib.dump(best_model, MODEL_DIR / "best_model.pkl")

# ---------------- SAVE METRICS ----------------
with open(EVAL_DIR / "metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# ---------------- CONFUSION MATRIX ----------------
cm = confusion_matrix(y_test, best_model.predict(X_test))

plt.figure(figsize=(5, 4))
plt.imshow(cm)
plt.title(f"Confusion Matrix ({best_model_name})")
plt.colorbar()
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig(EVAL_DIR / "confusion_matrix.png")
plt.close()

print("\n" + "=" * 45)
print(f"BEST MODEL SELECTED (CV ROC-AUC): {best_model_name}")
print(f"Best CV ROC-AUC: {best_cv_roc:.4f}")
print("Model saved to models/best_model.pkl")
print("Metrics saved to evaluation/metrics.json")
print("Confusion matrix saved to evaluation/confusion_matrix.png")
