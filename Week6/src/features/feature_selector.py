import json
import numpy as np
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier


BASE_DIR = Path(__file__).resolve().parents[1]
FEATURE_DIR = BASE_DIR / "features"


X_train = np.load(FEATURE_DIR / "X_train.npy", allow_pickle=True)
y_train = np.load(FEATURE_DIR / "y_train.npy", allow_pickle=True)

preprocessor = joblib.load(FEATURE_DIR / "preprocessing_pipeline.pkl")


# extract feature names from preprocessor
num_features = preprocessor.named_transformers_["num"].get_feature_names_out()
cat_features = (
    preprocessor.named_transformers_["cat"]
    .named_steps["encoder"]
    .get_feature_names_out()
)

feature_names = list(num_features) + list(cat_features)


# traing model for feature importance
rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf.fit(X_train, y_train)

importances = rf.feature_importances_

importance_df = sorted(
    zip(feature_names, importances),
    key=lambda x: x[1],
    reverse=True
)

TOP_K = 20
selected_features = [f[0] for f in importance_df[:TOP_K]]



with open(FEATURE_DIR / "feature_list.json", "w") as f:
    json.dump(selected_features, f, indent=4)


names = [f[0] for f in importance_df[:TOP_K]]
scores = [f[1] for f in importance_df[:TOP_K]]

plt.figure(figsize=(8, 6))
plt.barh(names[::-1], scores[::-1])
plt.title("Top Feature Importances")
plt.tight_layout()
plt.savefig(FEATURE_DIR / "feature_importance.png")
plt.close()


print("Day 2: Feature selection completed successfully")
print(f"Top {TOP_K} features saved to feature_list.json")
print("Feature importance plot saved as feature_importance.png")
