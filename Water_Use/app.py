from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# โหลดโมเดลจาก pickle
model_water_use = pickle.load(open(r"C:\project2\Water_Use\weather.pkl", 'rb'))
model_humidity = pickle.load(open(r"C:\project2\Water_Use\humidity.pkl", 'rb'))
model_temp = pickle.load(open(r"C:\project2\Water_Use\temp.pkl", 'rb'))
model_wind_speed = pickle.load(open(r"C:\project2\Water_Use\wind_speed.pkl", 'rb'))

# ตรวจสอบว่าโมเดลเป็น tuple หรือไม่
print("Model Types:")
print(f"Model Water Use: {type(model_water_use)}")
print(f"Model Humidity: {type(model_humidity)}")
print(f"Model Temp: {type(model_temp)}")
print(f"Model Wind Speed: {type(model_wind_speed)}")

# ถ้าโมเดลเป็น tuple ให้แยกโมเดลออกจาก tuple
if isinstance(model_water_use, tuple):
    model_water_use = model_water_use[0]
if isinstance(model_humidity, tuple):
    model_humidity = model_humidity[0]
if isinstance(model_temp, tuple):
    model_temp = model_temp[0]
if isinstance(model_wind_speed, tuple):
    model_wind_speed = model_wind_speed[0]

@app.route('/')
def hello_world():
    return render_template("Water_Use.html")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    # รับข้อมูลที่ผู้ใช้กรอกจาก form
    float_features = [float(x) for x in request.form.values()]
    final = np.array([float_features])  

    print("📌 Input Features:", float_features)
    print("Final Input Array:", final)

    # ตรวจสอบประเภทของโมเดล
    print("Model Type after checking:", type(model_humidity))

    try:
        # ทำนายผลลัพธ์จากโมเดลต่างๆ
        pred_water_use = model_water_use.predict(final)[0]
        pred_humidity = model_humidity.predict(final)[0]
        pred_temp = model_temp.predict(final)[0]
        pred_wind_speed = model_wind_speed.predict(final)[0]
    except Exception as e:
        print("Error during prediction:", e)
        return str(e)

    print(f"🔹 Water Use: {pred_water_use}, Humidity: {pred_humidity}, Temp: {pred_temp}, Wind Speed: {pred_wind_speed}")

    # กำหนดผลลัพธ์ของการทำนาย
    if 0 <= pred_water_use < 1:
        result = 'ท้องฟ้าแจ่มใส'
    elif 1 <= pred_water_use < 2:
        result = 'มีเมฆมาก'
    elif 2 <= pred_water_use < 3:
        result = 'หนาว'
    elif 3 <= pred_water_use < 4:
        result = 'มืดครึ้ม อึมครึม'
    elif 4 <= pred_water_use < 5:
        result = 'หมอก'
    elif 5 <= pred_water_use < 6:
        result = 'แดดมัว มีหมอกควัน'
    elif 6 <= pred_water_use < 7:
        result = 'ร้อน'
    elif 7 <= pred_water_use < 8:
        result = 'มีเมฆเป็นช่วง ๆ'
    elif 8 <= pred_water_use < 9:
        result = 'ค่อนข้างแจ่มใส'
    elif 9 <= pred_water_use < 10:
        result = 'มีเมฆมากและฝนตกเป็นช่วง ๆ'
    elif 10 <= pred_water_use < 11:
        result = 'มีเมฆมาก'
    elif 11 <= pred_water_use < 12:
        result = 'แดดจัดเป็นส่วนใหญ่'
    elif 12 <= pred_water_use < 13:
        result = 'มีเมฆบางส่วน'
    elif 13 <= pred_water_use < 14:
        result = 'ฝนตก'
    elif 14 <= pred_water_use < 15:
        result = 'ฝนโปรยปราย'
    elif 15 <= pred_water_use < 16:
        result = 'แดดจ้า'
    elif 16 <= pred_water_use < 17:
        result = 'ลมแรง'
    else:
        result = 'ผลการทำนายไม่สามารถระบุได้'

    # ส่งข้อมูลไปที่หน้า HTML
    return render_template(
        'Water_Use.html',
        word='พยากรณ์อากาศวันนี้:',
        answer='ข้อมูลที่กรอก:',
        a0=float_features[0], a1=float_features[1], a2=float_features[2], a3=float_features[3],
        a4=float_features[4], a5=float_features[5], a6=float_features[6], a7=float_features[7],
        a8=float_features[8], a9=float_features[9], a10=float_features[10], a11=float_features[11],
        a12=float_features[12], a13=float_features[13], a14=float_features[14], a15=float_features[15],
        a16=float_features[16], a17=float_features[17],                 
        pred=result,  
        humidity_pred=f"ความชื้นที่คาดการณ์: {pred_humidity:.2f}%",
        temp_pred=f"อุณหภูมิที่คาดการณ์: {pred_temp:.2f}°C",
        wind_pred=f"ความเร็วลมที่คาดการณ์: {pred_wind_speed:.2f} m/s",
        bhai=""
    )

if __name__ == '__main__':
    app.run(debug=True, port=5030)
