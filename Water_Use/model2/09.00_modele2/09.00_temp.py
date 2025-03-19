from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import pandas as pd
import pickle

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\09.00_temp.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# แปลงค่าข้อความเป็นตัวเลข
encoder = LabelEncoder()
data["Weather Condition"] = encoder.fit_transform(data["Weather Condition"])

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values
X = data.drop(columns=["Weather Condition"]).values.astype(float)

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Logistic Regression (GLM) สำหรับการจำแนกประเภท
glm_model = LogisticRegression(max_iter=1000, random_state=0, multi_class='ovr', solver='lbfgs')

# เทรนโมเดล
glm_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model2\09.00_modele2\09.00_temp.pkl"
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

# แสดง Classification Report
print("\nClassification Report:")
print(classification_report(y_test, y_pred))  # ใช้ classification_report ที่นำเข้าแล้ว
