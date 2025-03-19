import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor  # ใช้ Decision Tree Regressor แทน
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\19.00_weather.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
# data["Wind Speed (mph)"] = encoder.fit_transform(data["Weather Condition"])  # แปลงเป็นตัวเลข ถ้าต้องการแปลงค่าที่เป็นข้อความเป็นตัวเลข

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values  # ใช้ Wind Speed (mph) เป็น target
X = data.drop(columns=["Weather Condition"]).values.astype(float)  # ลบ Wind Speed ออกจาก X

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Decision Tree Regressor แทน
dt_model = DecisionTreeRegressor(criterion="squared_error", max_depth=5, random_state=0)

# เทรนโมเดล
dt_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model2\19.00_modele2\19.00_weather.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(dt_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทดสอบทำนาย Wind Speed (mph)
y_pred = model.predict(X_test)

# แสดงผลลัพธ์
print("Predicted Wind Speed (mph):", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test
