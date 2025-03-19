import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV3\00.00_temp.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
# data["Wind Speed (mph)"] = encoder.fit_transform(data["Weather Condition"])  # หากต้องการแปลงข้อความเป็นตัวเลข

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values  # ใช้ Weather Condition เป็น target
X = data.drop(columns=["Weather Condition"]).values.astype(float)  # ลบ Weather Condition ออกจาก X

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ RandomForestRegressor
rf_model = RandomForestRegressor(random_state=0)

# การค้นหา Hyperparameters ด้วย GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# เทรนโมเดลด้วย GridSearchCV
grid_search.fit(X_train, y_train)

# แสดงผลลัพธ์ของ GridSearchCV
print("Best Parameters found: ", grid_search.best_params_)

# ใช้โมเดลที่ดีที่สุดจากการค้นหา
best_rf_model = grid_search.best_estimator_

# ทำนายผล
y_pred = best_rf_model.predict(X_test)

# สร้าง directory ถ้ายังไม่มี
model_dir = r"C:\project2\Water_Use\model3\00.00_model3"  # แก้ไขให้ถูกต้อง
os.makedirs(model_dir, exist_ok=True)  # สร้างโฟลเดอร์ถ้ายังไม่มี

# บันทึกโมเดลด้วย pickle
model_path = os.path.join(model_dir, "00.00_temp.pkl")  # แก้ไขชื่อไฟล์ให้ถูกต้อง
with open(model_path, 'wb') as file:
    pickle.dump(best_rf_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# แสดงผลลัพธ์
print("Predicted Weather Condition:", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test
