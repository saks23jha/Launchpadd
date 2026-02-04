# DAY 4 — MODEL INTERPRETATION & ERROR ANALYSIS

## Objective
The objective of Day 4 was to improve the baseline model using hyperparameter tuning and to add explainability and error analysis to understand model behavior and performance.

---

## Step 1: Hyperparameter Tuning
The baseline XGBoost model selected in Day 3 was optimized using cross-validated ROC-AUC as the evaluation metric. Multiple combinations of hyperparameters were tested to improve generalization and reduce overfitting.

The tuned model achieved a higher ROC-AUC compared to the baseline, confirming improvement in model performance.

Tuning results were saved in:
tuning/results.json

---

## Step 2: Model Explainability (SHAP)
SHAP (SHapley Additive exPlanations) was used to interpret the predictions of the tuned XGBoost model.

The SHAP summary plot ranks features by their overall impact on model predictions. Each point represents a passenger, where positive SHAP values push predictions toward survival and negative values push toward non-survival. Feature values are represented using color gradients.

The SHAP feature importance chart provides a global view of the most influential features, showing that a limited set of features drives most predictions.

Generated files:
evaluation/shap_summary.png  
evaluation/shap_feature_importance.png

---

## Step 3: Error Analysis
Error analysis was performed using a confusion matrix heatmap to identify misclassification patterns.

The model correctly classifies most non-survivors, while a smaller number of survivors are misclassified as non-survivors. This indicates a conservative prediction behavior, which is expected due to class imbalance in the Titanic dataset.

The error analysis heatmap was saved as:
evaluation/error_heatmap.png

---

## Final Conclusion
Hyperparameter tuning significantly improved the XGBoost model over the baseline. SHAP analysis provided clear insights into feature influence and model decision-making. Error analysis revealed understandable and consistent misclassification patterns. The final model is both accurate and interpretable.

---

## Deliverables Completed
- training/tuning.py  
- tuning/results.json  
- evaluation/shap_summary.png  
- evaluation/shap_feature_importance.png  
- evaluation/error_heatmap.png  
- MODEL-INTERPRETATION.md
