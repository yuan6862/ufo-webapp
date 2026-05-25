import pickle
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

print("=" * 50)
print("UFO Model Training")
print("=" * 50)

# Load data
ufos = pd.read_csv("./data/ufos.csv")
print(f"\nRaw data rows: {len(ufos)}")

# Feature selection and cleaning
ufos = pd.DataFrame({
    "Seconds": ufos["duration (seconds)"],
    "Country": ufos["country"],
    "Latitude": ufos["latitude"],
    "Longitude": ufos["longitude"],
})
ufos.dropna(inplace=True)
ufos = ufos[(ufos["Seconds"] >= 1) & (ufos["Seconds"] <= 60)]
print(f"After cleaning: {len(ufos)} rows")

# Encode labels
le = LabelEncoder()
ufos["Country"] = le.fit_transform(ufos["Country"])
print(f"Countries: {list(enumerate(le.classes_))}")

# Train / test split
X = ufos[["Seconds", "Latitude", "Longitude"]]
y = ufos["Country"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
print(f"\nTrain: {len(X_train)} samples  |  Test: {len(X_test)} samples")

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print("\n" + "=" * 50)
print(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
print("=" * 50)
print("\nClassification Report:")
print(classification_report(
    y_test, predictions,
    target_names=["Australia", "Canada", "Germany", "UK", "US"]
))

# Save model
with open("ufo-model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to ufo-model.pkl")

# Sanity check
test_pred = model.predict([[50, 44, -12]])[0]
countries = ["Australia", "Canada", "Germany", "UK", "US"]
print(f"Sanity check: input [50s, lat=44, lon=-12] → {countries[test_pred]}")
