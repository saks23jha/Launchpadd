import json
import optuna
import numpy as np
from pathlib import Path

from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).resolve().parents[1]
FEATURE_DIR = BASE_DIR / "features"
TUNING_DIR = BASE_DIR / "tuning"

TUNING_DIR.mkdir(exist_ok=True)

# ---------------- LOAD DATA ----------------
X_train = np.load(FEATURE_DIR / "X_train.npy")
y_train = np.load(FEATURE_DIR / "y_train.npy")

# ---------------- OPTUNA OBJECTIVE ----------------
def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 300, 800),
        "max_depth": trial.suggest_int("max_depth", 3, 8),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
        "subsample": trial.suggest_float("subsample", 0.7, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.7, 1.0),
        "gamma": trial.suggest_float("gamma", 0.0, 5.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        "eval_metric": "auc",
        "random_state": 42,
        "use_label_encoder": False
    }

    model = XGBClassifier(**params)

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    roc_auc = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="roc_auc",
        n_jobs=-1
    ).mean()

    return roc_auc

# ---------------- RUN STUDY ----------------
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=50)

# ---------------- SAVE RESULTS ----------------
results = {
    "best_cv_roc_auc": study.best_value,
    "best_params": study.best_params
}

with open(TUNING_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=4)

print("=" * 50)
print("HYPERPARAMETER TUNING COMPLETED")
print(f"Best CV ROC-AUC: {study.best_value:.4f}")
print("Best Parameters:")
for k, v in study.best_params.items():
    print(f"  {k}: {v}")
print("Results saved to tuning/results.json")
print("=" * 50)
