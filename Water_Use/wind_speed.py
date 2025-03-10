import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor  # ใช้ Decision Tree Regressor
from sklearn.model_selection import train_test_split
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\test9.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แยก features (X) และ labels (y)
X = data.drop(columns=["Wind Speed(mph)"]).values.astype(float)  # ลบคอลัมน์ Wind Speed(mph) ออกจาก features
y = data["Wind Speed(mph)"].values  # ใช้ Wind Speed(mph) เป็น target

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ตรวจสอบจำนวนคอลัมน์
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# ใช้ Decision Tree Regressor
# ใช้ Decision Tree Regressor
dt_model = DecisionTreeRegressor(criterion='squared_error', max_depth=5, random_state=0)


# เทรนโมเดล
dt_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\wind_speed.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(dt_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทำนายใน test set
y_pred = model.predict(X_test)

# แสดงผลลัพธ์
print("Predicted Wind Speed(mph) for the test set:", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test
