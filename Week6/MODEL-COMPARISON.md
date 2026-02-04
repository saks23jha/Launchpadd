# DAY 3 — MODEL COMPARISON & SELECTION

## Objective
The objective of Day 3 was to build a unified training pipeline, train multiple machine learning models, compare their performance using cross-validated evaluation metrics, and select the best model in a robust and unbiased manner.

---

## Models Trained
The following models were trained and evaluated using the same feature set:

- Logistic Regression  
- Random Forest  
- XGBoost  
- Neural Network (MLP)

All models were trained on the training split and evaluated using cross-validation as well as a final hold-out test set.

---

## Evaluation Strategy
To avoid overfitting and ensure reliable model comparison, **cross-validated ROC-AUC (CV ROC-AUC)** was used as the **primary model selection metric**.

### Why CV ROC-AUC?
- ROC-AUC measures class separability across all thresholds
- Cross-validation reduces variance caused by a single train-test split
- More reliable for imbalanced datasets like Titanic
- Prevents choosing a model that performs well only by chance on the test set

---

## Model Performance Summary

- **Logistic Regression**
  - Strong baseline with stable performance
  - High interpretability
  - Slightly lower CV ROC-AUC compared to XGBoost

- **Random Forest**
  - Captured non-linear relationships
  - Performance was competitive but less stable across folds

- **XGBoost**
  - Achieved the **highest cross-validated ROC-AUC**
  - Consistently strong performance across folds
  - Effectively captured feature interactions and non-linear patterns
  - Selected as the final model

- **Neural Network**
  - Required more tuning and data
  - Did not outperform tree-based models on CV ROC-AUC

---

## Best Model Selection
The final model was selected **solely on the basis of cross-validated ROC-AUC**, not on single-split test metrics.

**Final Selected Model:**  
XGBoost

The selected model was saved as:
models/best_model.pkl



## Conclusion
By using **cross-validated ROC-AUC** as the selection criterion, the Day 3 pipeline ensures robust and unbiased model selection. XGBoost emerged as the best-performing model due to its superior and consistent CV ROC-AUC, making it the most reliable choice for further tuning, interpretation, and deployment.
