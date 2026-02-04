# FEATURE ENGINEERING – WEEK 6 DAY 2

## Objective
Convert cleaned Titanic data into **model-ready data** by engineering features, selecting the most important ones, and preparing train/test datasets.

## Target Variable
- Survived (1 = survived, 0 = not survived)

## Feature Engineering
- Generated **10 new features**: FamilySize, IsAlone, FarePerPerson, FareLog, AgeFilled, IsChild, AgeBucket, HighFare, LargeFamily, PclassFare
- Handled missing values using **median (numerical)** and **most frequent (categorical)**
- Encoded categorical features using **One-Hot Encoding**
- Normalized numerical features using **StandardScaler**
- Built a reusable preprocessing pipeline and saved it

## Feature Selection
- Applied **Mutual Information** to select important features
- Used **Random Forest feature importance** for visualization
- Saved selected features to `feature_list.json`
- Saved feature importance plot as `feature_importance.png`

## Outputs
- `feature_list.json`
- `feature_importance.png`

## Conclusion
This step prepares a clean, efficient, and scalable feature set for **model training and evaluation**.
