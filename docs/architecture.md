# Architecture

ESP32 sensors → Wi-Fi → Flask REST API → Database → Web dashboard.

Emergency flow:
Sensors → ESP32 → emergency logic → API alert → caregiver/doctor dashboard.

Main sensors:
MAX30102, MPU6050, DS18B20.
