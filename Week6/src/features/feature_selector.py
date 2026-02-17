import json
import numpy as np
import joblib
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from sklearn.feature_selection import mutual_info_classif

BASE_DIR = Path(__file__).resolve().parents[1]
FEATURE_DIR = BASE_DIR / "features"

# Load data
X_train = np.load(FEATURE_DIR / "X_train.npy", allow_pickle=True)
y_train = np.load(FEATURE_DIR / "y_train.npy", allow_pickle=True)

preprocessor = joblib.load(FEATURE_DIR / "preprocessing_pipeline.pkl")

# Extract feature names
num_features = preprocessor.named_transformers_["num"].get_feature_names_out()
cat_features = (
    preprocessor.named_transformers_["cat"]
    .named_steps["encoder"]
    .get_feature_names_out()
)

feature_names = list(num_features) + list(cat_features)

X_df = pd.DataFrame(X_train, columns=feature_names)

# 1️ Correlation Threshold

corr_matrix = X_df.corr().abs()

upper = corr_matrix.where(
    np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
)

CORR_THRESHOLD = 0.85

to_drop = [
    column for column in upper.columns
    if any(upper[column] > CORR_THRESHOLD)
]

X_corr_filtered = X_df.drop(columns=to_drop)

print(f"Correlation filter: dropped {len(to_drop)} features")


# 2️ Mutual Information

mi_scores = mutual_info_classif(
    X_corr_filtered.values,
    y_train,
    random_state=42
)

mi_df = pd.DataFrame({
    "feature": X_corr_filtered.columns,
    "mi_score": mi_scores
}).sort_values(by="mi_score", ascending=False)

TOP_K = 20
selected_features = mi_df.head(TOP_K)["feature"].tolist()

# Save selected features
with open(FEATURE_DIR / "feature_list.json", "w") as f:
    json.dump(selected_features, f, indent=4)

# Plot MI scores

names = mi_df.head(TOP_K)["feature"]
scores = mi_df.head(TOP_K)["mi_score"]

plt.figure(figsize=(8, 6))
plt.barh(names[::-1], scores[::-1])
plt.title("Top Features by Mutual Information")
plt.tight_layout()
plt.savefig(FEATURE_DIR / "feature_importance.png")
plt.close()

print("Day 2: Feature selection completed successfully")
print(f"Top {TOP_K} features saved to feature_list.json")
print("Feature importance plot saved as feature_importance.png")
