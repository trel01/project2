import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import warnings
import pickle

warnings.filterwarnings("ignore")
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\00.00_humidity.csv")
data = data.dropna()
encoder = LabelEncoder()
data["Weather Condition"] = encoder.fit_transform(data["Weather Condition"])

y = data["Weather Condition"].values 
X = data.drop(columns=["Weather Condition"]).values.astype(float) 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)

rf_model.fit(X_train, y_train)

model_path = r"C:\project2\Water_Use\model2\00.00_modele2\00.00_humidity.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(rf_model, file)

with open(model_path, 'rb') as file:
    model = pickle.load(file)

y_pred = model.predict(X_test)

y_pred_labels = encoder.inverse_transform(y_pred)

print("Predicted Weather Conditions:", y_pred_labels)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

valid_classes = np.unique(np.concatenate((y_test, y_pred))) 
valid_class_labels = encoder.inverse_transform(valid_classes).astype(str).tolist()  

print("Classification Report:")
print(classification_report(y_test, y_pred, labels=valid_classes, target_names=valid_class_labels))
