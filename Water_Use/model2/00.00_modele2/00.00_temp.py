import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
import pickle

warnings.filterwarnings("ignore")
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\00.00_temp.csv")
data = data.dropna()

encoder = LabelEncoder()
# data["Wind Speed (mph)"] = encoder.fit_transform(data["Weather Condition"]) 

y = data["Weather Condition"].values 
X = data.drop(columns=["Weather Condition"]).values.astype(float)  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

dt_model = DecisionTreeRegressor(criterion="squared_error", max_depth=5, random_state=0)
dt_model.fit(X_train, y_train)

model_path = r"C:\project2\Water_Use\model2\00.00_modele2\00.00_temp.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(dt_model, file)

with open(model_path, 'rb') as file:
    model = pickle.load(file)

y_pred = model.predict(X_test)

print("Predicted Wind Speed (mph):", y_pred)
print("X_train shape:", X_train.shape)  
print("X_test shape:", X_test.shape)    
