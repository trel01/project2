from flask import Flask, request, render_template
import pickle
import numpy as np
import os
from datetime import datetime
import threading
import time

app = Flask(__name__)

# ตัวแปรเก็บโมเดลและ lock
all_models = {}
model_lock = threading.Lock()

# ---------- ฟังก์ชันโหลดโมเดล ----------
def load_all_models():
    """ โหลดโมเดลทั้งหมด """
    print("\n🔄 กำลังโหลดโมเดลใหม่...")
    base_path = r"C:\project2\Water_Use\model3"
    model_files = ["humidity", "temp", "wind_speed", "weather"]
    temp_models = {}

    for hour in range(24):
        time_str = f"{hour:02d}.00"
        model_path = os.path.join(base_path, f"{time_str}_model3")
        models_per_hour = {}

        if not os.path.exists(model_path):
            print(f"⚠️ ไม่พบโฟลเดอร์: {model_path}")
            continue

        missing = False
        for model_name in model_files:
            file_path = os.path.join(model_path, f"{time_str}_{model_name}.pkl")
            if not os.path.exists(file_path):
                print(f"⚠️ ไม่พบไฟล์: {file_path}")
                missing = True
                continue
            try:
                with open(file_path, 'rb') as f:
                    models_per_hour[model_name] = pickle.load(f)
                print(f"✅ โหลด {file_path} สำเร็จ!")
            except Exception as e:
                print(f"❌ โหลด {file_path} ไม่สำเร็จ: {e}")
                missing = True

        if not missing and len(models_per_hour) == len(model_files):
            temp_models[time_str] = models_per_hour
            print(f"🕐 โมเดล {time_str} พร้อมใช้งาน!")
        else:
            print(f"⚠️ โมเดล {time_str} ไม่ครบ ไม่เพิ่มเข้า all_models")

    # 🔒 อัปเดตโมเดลทั้งหมด
    with model_lock:
        all_models.clear()
        all_models.update(temp_models)
    print("🚀 โหลดโมเดลทั้งหมดเสร็จแล้ว!\n")

# ---------- Background Thread ----------
def auto_reload_models(interval=3600):
    """ Reload model ทุก X วินาที """
    while True:
        load_all_models()
        print(f"⏰ รอ {interval} วินาทีก่อนโหลดใหม่...\n")
        time.sleep(interval)

# ---------- เวลา ----------
def get_time_slot():
    current_hour = datetime.now().hour
    return f"{current_hour:02d}.00"

# ---------- Weather Dictionary ----------
weather_dict = {
    0: 'แจ่มใส', 
    1: 'ค่อนข้างแจ่มใส', 
    2: 'มีแดดเป็นส่วนใหญ่', 
    3: 'แดดจ้า', 
    4: 'มีเมฆมาก', 
    5: 'มืดครึ้มและหม่นหมอง', 
    6: 'มีเมฆเป็นช่วง ๆ', 
    7: 'มีเมฆมากเป็นส่วนใหญ่', 
    8: 'มีเมฆบางส่วน', 
    9: 'หมอก', 
    10: 'แดดจ้าแบบมีหมอกบาง', 
    11: 'มีเมฆมากและมีฝนตกเป็นช่วง ๆ', 
    12: 'ฝนตก ', 
    13: 'ฝนโปรย / ฝนตกเป็นช่วง ๆ ', 
    14: 'เย็น', 
    15: 'ร้อน', 
    16: 'มีลมแรง'
}


# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("Water_Model.html")
# ---------- Routes ----------# ---------- Routes ----------# ---------- Routes ----------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        form_values = list(request.form.values())
        print(f"📋 ค่าที่รับจากฟอร์ม: {form_values}")

        if not form_values or all(v.strip() == "" for v in form_values):
            return "❌ กรุณากรอกข้อมูลให้ครบถ้วน"

        float_features = [float(x) for x in form_values]
        final_input = np.array([float_features])

        selected_time = get_time_slot()

        # 🔒 ใช้ lock อ่าน models
        with model_lock:
            models = all_models.get(selected_time)

        if models is None:
            return f"❌ ไม่พบโมเดลสำหรับ {selected_time}"

        pred_humidity = models['humidity'].predict(final_input)[0]
        pred_temp = models['temp'].predict(final_input)[0]
        pred_wind_speed = models['wind_speed'].predict(final_input)[0]
        pred_weather = models['weather'].predict(final_input)[0]

        result = weather_dict.get(int(pred_weather), 'ไม่สามารถพยากรณ์ได้')

        return render_template(
            'Water_Model.html',
            word="พยากรณ์อากาศวันนี้:",
            answer="ข้อมูลที่กรอก:",
            pred=result,
            humidity_pred=f"{pred_humidity:.2f}%",
            temp_pred=f"{pred_temp:.2f}°C",
            wind_pred=f"{pred_wind_speed:.2f} m/s",
            model_used=f"📌 โมเดลที่ใช้: {selected_time}"
        )
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {e}"

@app.route('/predict_all', methods=['POST'])
def predict_all():
    try:
        form_values = list(request.form.values())
        print(f"📋 ค่าที่รับจากฟอร์ม: {form_values}")

        if not form_values or all(v.strip() == "" for v in form_values):
            return "❌ กรุณากรอกข้อมูลให้ครบถ้วน"

        float_features = [float(x) for x in form_values]
        final_input = np.array([float_features])

        # ✅ พยากรณ์ปัจจุบัน
        selected_time = get_time_slot()
        with model_lock:
            current_models = all_models.get(selected_time)

        if current_models is None:
            return f"❌ ไม่พบโมเดลสำหรับ {selected_time}"

        pred_humidity = current_models['humidity'].predict(final_input)[0]
        pred_temp = current_models['temp'].predict(final_input)[0]
        pred_wind_speed = current_models['wind_speed'].predict(final_input)[0]
        pred_weather = current_models['weather'].predict(final_input)[0]
        result = weather_dict.get(int(pred_weather), 'ไม่สามารถพยากรณ์ได้')

        # ✅ ปรับค่าผลลัพธ์ตามเงื่อนไขที่กำหนด
        pred_humidity = min(max(pred_humidity, 30.5), 98.4)
        pred_temp = min(max(pred_temp, 12.6), 36.8)
        pred_wind_speed = min(max(pred_wind_speed, 0), 5.2)

        # ✅ พยากรณ์เฉพาะเวลาที่เลือก
        valid_times = ['00.00', '03.00', '06.00', '09.00', '12.00', '15.00', '18.00', '21.00']
        results = []
        with model_lock:
            for time_str, models in all_models.items():
                if time_str in valid_times:
                    try:
                        pred_humidity_all = min(max(models['humidity'].predict(final_input)[0], 30.5), 98.4)
                        pred_temp_all = min(max(models['temp'].predict(final_input)[0], 12.6), 36.8)
                        pred_wind_speed_all = min(max(models['wind_speed'].predict(final_input)[0], 0), 5.2)
                        pred_weather_all = models['weather'].predict(final_input)[0]

                        result_text = weather_dict.get(int(pred_weather_all), 'ไม่สามารถพยากรณ์ได้')

                        results.append({
                            'time': time_str,
                            'humidity': f"{pred_humidity_all:.2f}%",
                            'temp': f"{pred_temp_all:.2f}°C",
                            'wind': f"{pred_wind_speed_all:.2f} m/s",
                            'weather': result_text
                        })
                    except Exception as e:
                        print(f"❌ พยากรณ์ {time_str} ล้มเหลว: {e}")
                        continue

        # ✅ render ผลลัพธ์เฉพาะเวลาที่เลือก
        return render_template(
            'Water_Model.html',
            word="พยากรณ์อากาศขณะนี้:",
            pred=result,
            humidity_pred=f"{pred_humidity:.2f}%",
            temp_pred=f"{pred_temp:.2f}°C",
            wind_pred=f"{pred_wind_speed:.2f} m/s",
            model_used=f"📌 โมเดลที่ใช้: {selected_time}",
            results=results,
            input_data=form_values
        )
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {e}"





# ---------- Main ----------
if __name__ == '__main__':
    load_all_models()
    threading.Thread(target=auto_reload_models, args=(3600,), daemon=True).start()
    app.run(debug=True, port=5050)
