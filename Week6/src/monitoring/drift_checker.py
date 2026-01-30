from pathlib import Path
import re
import numpy as np

# ---------------- PATHS ----------------
BASE_DIR = Path(__file__).resolve().parents[1]
LOG_FILE = BASE_DIR / "logs" / "predictions.log"

# ---------------- READ LOGS ----------------
predictions = []
probabilities = []

pattern = re.compile(r"prediction=(\d).*probability=([\d.]+)")

with open(LOG_FILE, "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            predictions.append(int(match.group(1)))
            probabilities.append(float(match.group(2)))

# ---------------- MONITORING ----------------
predictions = np.array(predictions)
probabilities = np.array(probabilities)

print("\n=== MONITORING REPORT ===")

print(f"Total predictions logged: {len(predictions)}")

print("\nPrediction distribution:")
print(f"  Predicted Not Survived (0): {(predictions == 0).sum()}")
print(f"  Predicted Survived (1): {(predictions == 1).sum()}")

print("\nProbability statistics:")
print(f"  Mean probability: {probabilities.mean():.4f}")
print(f"  Std deviation:   {probabilities.std():.4f}")
print(f"  Min probability: {probabilities.min():.4f}")
print(f"  Max probability: {probabilities.max():.4f}")

# ---------------- SIMPLE DRIFT CHECK ----------------
if probabilities.mean() < 0.3 or probabilities.mean() > 0.7:
    print("\n Warning: Potential prediction drift detected")
else:
    print("\n Prediction distribution looks stable")
