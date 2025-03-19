import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
import warnings

warnings.filterwarnings("ignore")

# 🔹 โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV3\08.00_wind_speed.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# 🔹 แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
data["Weather Condition"] = encoder.fit_transform(data["Weather Condition"])

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values
X = data.drop(columns=["Weather Condition"]).values.astype(float)

# 🔹 ปรับขนาดข้อมูล
scaler = StandardScaler()
X = scaler.fit_transform(X)

# แบ่งข้อมูล train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# 🔹 ใช้ Generalized Linear Model (Logistic Regression)
glm_model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=1000, random_state=0)

# เทรนโมเดล
glm_model.fit(X_train, y_train)

# 🔹 บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model3\08.00_model3\08.00_wind_speed.pkl"
with open(model_path, 'wb') as file:
    pickle.dump((glm_model, scaler), file)  # บันทึกทั้งโมเดลและ scaler

# 🔹 โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model, scaler = pickle.load(file)

# ทดสอบทำนาย Weather Condition
X_test_scaled = scaler.transform(X_test)
y_pred = model.predict(X_test_scaled)

# แปลงค่าตัวเลขกลับเป็น Weather Condition เดิม
y_pred_labels = encoder.inverse_transform(y_pred)

# แสดงผลลัพธ์
print("Predicted Weather Conditions:", y_pred_labels)
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
