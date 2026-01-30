import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


# Load data
df = pd.read_csv("data/raw/titanic.csv")

# Target
y = df["Survived"]
X = df.drop(columns=["Survived"])


# -------- FEATURE GENERATION (10+) --------
X["FamilySize"] = X["SibSp"] + X["Parch"] + 1
X["IsAlone"] = (X["FamilySize"] == 1).astype(int)
X["FarePerPerson"] = X["Fare"] / X["FamilySize"]
X["FareLog"] = np.log1p(X["Fare"])
X["AgeFilled"] = X["Age"].fillna(X["Age"].median())
X["IsChild"] = (X["AgeFilled"] < 12).astype(int)
X["AgeBucket"] = pd.cut(
    X["AgeFilled"],
    bins=[0, 12, 20, 40, 60, 80],
    labels=["Child", "Teen", "Adult", "MiddleAge", "Senior"]
)
X["HighFare"] = (X["Fare"] > X["Fare"].median()).astype(int)
X["LargeFamily"] = (X["FamilySize"] >= 5).astype(int)
X["PclassFare"] = X["Pclass"] * X["Fare"]


# Feature groups
num_cols = [
    "Age", "Fare", "SibSp", "Parch", "FamilySize",
    "FarePerPerson", "FareLog", "AgeFilled",
    "IsAlone", "IsChild", "HighFare", "LargeFamily", "PclassFare"
]

cat_cols = ["Sex", "Embarked", "Pclass", "AgeBucket"]

X = X[num_cols + cat_cols]


# -------- PIPELINES --------
num_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

cat_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", num_pipeline, num_cols),
    ("cat", cat_pipeline, cat_cols)
])


# Transform
X_processed = preprocessor.fit_transform(X)

# Train–test split
X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# # Save outputs
joblib.dump(preprocessor, "features/preprocessing_pipeline.pkl")

np.save("features/X_train.npy", X_train)
np.save("features/X_test.npy", X_test)
np.save("features/y_train.npy", y_train)
np.save("features/y_test.npy", y_test)

print("build_features.py completed")
