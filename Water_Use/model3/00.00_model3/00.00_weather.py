import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor  # ใช้ Decision Tree Regressor แทน
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV3\00.00_weather.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
# หาก Weather Condition เป็นข้อความ ให้แปลงเป็นตัวเลข
data["Weather Condition"] = encoder.fit_transform(data["Weather Condition"])

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values  # ใช้ Weather Condition เป็น target
X = data.drop(columns=["Weather Condition"]).values.astype(float)  # ลบ Weather Condition ออกจาก X

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Decision Tree Regressor
dt_model = DecisionTreeRegressor(criterion="squared_error", max_depth=5, random_state=0)

# เทรนโมเดล
dt_model.fit(X_train, y_train)

# สร้าง directory ถ้ายังไม่มี
model_dir = r"C:\project2\Water_Use\model3\00.00_model3"  # แก้ไขให้ถูกต้อง
os.makedirs(model_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

# บันทึกโมเดลด้วย pickle
model_path = os.path.join(model_dir, "00.00_weather.pkl")  # แก้ไขชื่อไฟล์ให้ถูกต้อง
with open(model_path, 'wb') as file:
    pickle.dump(dt_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทำนายผล
y_pred = model.predict(X_test)

# แสดงผลลัพธ์
print("Predicted Weather Condition:", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test

# ถ้าต้องการแปลงค่าตัวเลขกลับเป็น Weather Condition เดิม
y_pred_labels = encoder.inverse_transform(np.round(y_pred).astype(int))

print("Predicted Weather Condition (Labels):", y_pred_labels)
