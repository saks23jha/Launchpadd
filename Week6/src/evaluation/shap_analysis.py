import joblib
import numpy as np
import shap
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
FEATURE_DIR = BASE_DIR / "features"
MODEL_DIR = BASE_DIR / "models"
EVAL_DIR = BASE_DIR / "evaluation"

EVAL_DIR.mkdir(exist_ok=True)


X_train = np.load(FEATURE_DIR / "X_train.npy")
model = joblib.load(MODEL_DIR / "best_model.pkl")


explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_train)


plt.figure()
shap.summary_plot(
    shap_values,
    X_train,
    show=False
)
plt.tight_layout()
plt.savefig(EVAL_DIR / "shap_summary.png", dpi=300)
plt.close()

# shap bar plot
plt.figure()
shap.summary_plot(
    shap_values,
    X_train,
    plot_type="bar",
    show=False
)
plt.tight_layout()
plt.savefig(EVAL_DIR / "shap_feature_importance.png", dpi=300)
plt.close()

print("SHAP analysis completed successfully.")
print("Saved:")
print("- evaluation/shap_summary.png")
print("- evaluation/shap_feature_importance.png")
