import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor  # ใช้ GBT สำหรับ Regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder  # ใช้สำหรับแปลงข้อมูลข้อความเป็นตัวเลข
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\test9.csv")

# ตรวจสอบคอลัมน์ทั้งหมด
print(data.columns)  # ตรวจสอบว่ามี "Temperature(℃)" หรือไม่

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงคอลัมน์ข้อความให้เป็นตัวเลข
categorical_columns = data.select_dtypes(include=["object"]).columns  # ค้นหาคอลัมน์ข้อความ
encoder = LabelEncoder()

for col in categorical_columns:
    data[col] = encoder.fit_transform(data[col])  # แปลงข้อความเป็นตัวเลข

# แยก features (X) และ labels (y)
y = data["Temperature(℃)"].values.astype(float)  # ใช้คอลัมน์ Temperature(℃) เป็นค่าที่ต้องพยากรณ์
X = data.drop(columns=["Temperature(℃)"]).values.astype(float)  # ลบคอลัมน์ Temperature(℃) ออกจาก features

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Gradient Boosting Regressor
gbt_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0)

# เทรนโมเดล
gbt_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\temp.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(gbt_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทำนายค่า Temperature(℃) บนชุดทดสอบ
y_pred = model.predict(X_test)

# แสดงผลลัพธ์
print("Predicted Temperatures:", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test

