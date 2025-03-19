import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier  # ใช้ Gradient Boosting
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report  # เพิ่มการประเมินผล
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\16.00_wind_speed.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
data["Weather Condition"] = encoder.fit_transform(data["Weather Condition"])  # แปลงเป็นตัวเลข

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values  # ใช้ Weather Condition เป็น target
X = data.drop(columns=["Weather Condition"]).values.astype(float)  # ลบ Weather Condition ออกจาก X

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Gradient Boosting Classifier
gb_model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=0)

# เทรนโมเดล
gb_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model2\16.00_modele2\16.00_wind_speed.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(gb_model, file)

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

# ตรวจสอบคลาสที่มีอยู่ใน y_test และ y_pred
valid_classes = np.unique(np.concatenate((y_test, y_pred)))  # รวมคลาสที่มีจริง
valid_class_labels = encoder.inverse_transform(valid_classes).astype(str).tolist()  # แปลงเป็น string

# แสดง Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred, labels=valid_classes, target_names=valid_class_labels))
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test
