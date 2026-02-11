import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import confusion_matrix


BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"
FEATURE_DIR = BASE_DIR / "features"
EVAL_DIR = BASE_DIR / "evaluation"

EVAL_DIR.mkdir(exist_ok=True)


X_test = np.load(FEATURE_DIR / "X_test.npy")
y_test = np.load(FEATURE_DIR / "y_test.npy")


model = joblib.load(MODEL_DIR / "best_model.pkl")

# predictions
y_pred = model.predict(X_test)

# confusion matrix
cm = confusion_matrix(y_test, y_pred)

# heatmap
plt.figure(figsize=(6, 5))
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Not Survived", "Survived"],
    yticklabels=["Not Survived", "Survived"]
)

plt.xlabel("Predicted Label")
plt.ylabel("Actual Label")
plt.title("Error Analysis Heatmap (Confusion Matrix)")
plt.tight_layout()

plt.savefig(EVAL_DIR / "error_heatmap.png")
plt.close()

print("Error analysis completed.")
print("Saved: evaluation/error_heatmap.png")
