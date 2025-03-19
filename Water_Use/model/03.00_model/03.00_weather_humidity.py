import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression  # ใช้ GLM (Logistic Regression)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\WeterCSV\water-03.00-dawn.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
data["Humidity(%)"] = encoder.fit_transform(data["Humidity(%)"])  # แปลงเป็นตัวเลข

# แยก features (X) และ labels (y)
y = data["Humidity(%)"].values  # ใช้ Weather Condition เป็น target
X = data.drop(columns=["Humidity(%)"]).values.astype(float)  # ลบ Weather Condition ออกจาก X

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Logistic Regression (GLM)
glm_model = LogisticRegression(max_iter=1000, random_state=0)

# เทรนโมเดล
glm_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model\03.00_model\03.00_humidity.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(glm_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทดสอบทำนาย Weather Condition
y_pred = model.predict(X_test)

# แปลงค่าตัวเลขกลับเป็น Weather Condition เดิม
y_pred_labels = encoder.inverse_transform(y_pred)

# แสดงผลลัพธ์
print("Predicted Weather Conditions:", y_pred_labels)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test
