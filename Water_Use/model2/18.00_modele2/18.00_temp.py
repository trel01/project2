import numpy as np
import pandas as pd
from sklearn.svm import SVR  # ใช้ SVR แทน SVC สำหรับ regression
from sklearn.model_selection import train_test_split
import warnings
import pickle

warnings.filterwarnings("ignore")

# โหลดข้อมูล
data = pd.read_csv(r"C:\project2\Water_Use\CSV2\18.00_temp.csv")

# ลบค่าที่หายไป (ถ้ามี)
data = data.dropna()

# ตรวจสอบข้อมูล Weather Condition
print(data["Weather Condition"].unique())  # ตรวจสอบค่าของ Weather Condition ที่มีในข้อมูล

# แยก features (X) และ labels (y)
y = data["Weather Condition"].values  # ใช้ Weather Condition เป็น target
X = data.drop(columns=["Weather Condition"]).values.astype(float)  # ลบ Weather Condition ออกจาก X

# ตรวจสอบว่า y มีค่าตั้งแต่ 10-40 หรือไม่
print("Unique values in Weather Condition (y):", np.unique(y))

# แบ่งข้อมูล train และ test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# ใช้ Support Vector Regressor (SVR) แทน SVC
svr_model = SVR(kernel='rbf', C=1.0, epsilon=0.1)

# เทรนโมเดล
svr_model.fit(X_train, y_train)

# บันทึกโมเดลด้วย pickle
model_path = r"C:\project2\Water_Use\model2\18.00_modele2\18.00_temp.pkl"
with open(model_path, 'wb') as file:
    pickle.dump(svr_model, file)

# โหลดโมเดลกลับมาใช้งาน
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# ทดสอบทำนาย Weather Condition
y_pred = model.predict(X_test)

# แสดงผลลัพธ์
print("Predicted Weather Conditions:", y_pred)
print("X_train shape:", X_train.shape)  # จำนวน features ตอน train
print("X_test shape:", X_test.shape)    # จำนวน features ตอน test
