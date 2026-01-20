# DATA REPORT – Week 6 Day 1

## Objective
Build a data cleaning pipeline to convert raw Titanic data into a clean dataset and perform Exploratory Data Analysis (EDA) to understand patterns 
and relationships in the data.

## Dataset
- **Raw Data:** `src/data/raw/titanic.csv`
- **Processed Data:** `src/data/processed/final.csv`

## Data Pipeline
The pipeline reads raw data, cleans it, and saves a processed dataset.

### Cleaning Steps
- **Missing Values**
  - Age → filled with median
  - Embarked → filled with mode
- **Duplicates**
  - Removed duplicate records
- **Outliers**
  - Removed extreme Fare values using the IQR method (1.5 × IQR)

The cleaned data is saved as `final.csv`. Raw data remains unchanged.

## Exploratory Data Analysis (EDA)
EDA was performed on the cleaned dataset using Pandas, Matplotlib, and Seaborn.

### EDA Tasks
- Verified cleaned data using `df.head()`
- Analyzed target variable (Survived) distribution
- Visualized feature distributions (Age, Fare)
- Generated correlation matrix
- Verified missing values using a heatmap

## Key Insights
- Data cleaning improved analysis clarity

## Conclusion
A complete data cleaning pipeline and EDA process was implemented, resulting in a reliable, analysis-ready dataset suitable for further modeling.
