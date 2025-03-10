import numpy as np
import pandas as pd
from sklearn.svm import SVR  # เปลี่ยนจาก SVC เป็น SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\test9.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# จัดการกับคอลัมน์ข้อความ (ถ้ามี)
categorical_columns = data.select_dtypes(include=["object"]).columns
encoder_dict = {}

for col in categorical_columns:
    encoder = LabelEncoder()
    data[col] = encoder.fit_transform(data[col])  # แปลงข้อความเป็นตัวเลข
    encoder_dict[col] = encoder  # เก็บ encoder ไว้ใช้ตอน decode

# แยก features (X) และ labels (y)
y = data["Humidity(%)"].values  # ใช้ Humidity(%) เป็น target
X = data.drop(columns=["Humidity(%)"], errors="ignore").values.astype(float)  # ลบ Humidity ออกจาก X

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ตรวจสอบจำนวนคอลัมน์
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)

# ใช้ Support Vector Regression (SVR)
svm_model = SVR(kernel='rbf', C=1.0, epsilon=0.1)

# เทรนโมเดล
svm_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\humidity.pkl"
with open(model_path, 'wb') as file:
    pickle.dump((svm_model, encoder_dict), file)  # บันทึก encoder ด้วย

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model, encoder_dict = pickle.load(file)

# ทำนายใน test set
y_pred = model.predict(X_test)

# แสดงผลลัพธ์
print("Predicted Humidity(%) for the test set:", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)