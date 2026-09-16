# LifeLink – Smart Emergency Healthcare Response System

College-project prototype combining an ESP32 wearable, emergency alerts, medical records, and blood availability checking.

## Features
- Patient/caregiver/doctor registration and login
- Medical profile
- ESP32 health monitoring
- Prototype fall detection
- Emergency alerts
- Blood compatibility lookup
- SQLite database
- REST API
- Responsive dashboard
- JWT authentication and password hashing

> Educational prototype only. It is not a medical device. Sensor thresholds and fall detection are not clinically validated.

## Run
```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## ESP32 libraries
- SparkFun MAX3010x Sensor Library
- Adafruit MPU6050
- Adafruit Unified Sensor
- OneWire
- DallasTemperature

Do not commit real patient data, passwords, API keys, or database files.
