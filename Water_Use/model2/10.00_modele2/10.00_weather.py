import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\10.00_weather.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
data["Weather Condition"] = encoder.fit_transform(data["Weather Condition"])

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values  # Target
X = data.drop(columns=["Weather Condition"]).values.astype(float)  # Features

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Random Forest Classifier
rf_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=0)

# เทรนโมเดล
rf_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model2\10.00_modele2\10.00_weather.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(rf_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทดสอบทำนาย Weather Condition
y_pred = model.predict(X_test)

# แปลงค่าตัวเลขกลับเป็น Weather Condition เดิม
y_pred_labels = encoder.inverse_transform(y_pred)

# แสดงผลลัพธ์
print("Predicted Weather Conditions:", y_pred_labels)

# คำนวณ Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

# ตรวจสอบคลาสที่ปรากฏใน y_test และ y_pred
valid_classes = np.unique(np.concatenate((y_test, y_pred)))  # รวม class ที่มีจริง
valid_class_labels = encoder.inverse_transform(valid_classes).astype(str).tolist()  # แปลงเป็น string และใช้ .tolist()

# แสดง Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred, labels=valid_classes, target_names=valid_class_labels))
