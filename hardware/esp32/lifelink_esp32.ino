/*
 LifeLink ESP32 wearable prototype
 Sensors: MAX30102, MPU6050, DS18B20
 Libraries: SparkFun MAX3010x, Adafruit MPU6050, Adafruit Unified Sensor,
 OneWire, DallasTemperature

 IMPORTANT: SpO2 is NOT fabricated here. Integrate a validated SpO2
 algorithm before relying on SpO2 data. Fall thresholds are educational only.
*/
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <math.h>

#define TEMP_PIN 4
#define BUZZER_PIN 5
const char* WIFI_SSID="YOUR_WIFI_NAME";
const char* WIFI_PASSWORD="YOUR_WIFI_PASSWORD";
const char* API_URL="http://YOUR_COMPUTER_IP:5000/api/health/readings";
const char* JWT_TOKEN="PASTE_USER_JWT_HERE";

MAX30105 max30102;
Adafruit_MPU6050 mpu;
OneWire oneWire(TEMP_PIN);
DallasTemperature temp(&oneWire);
long lastBeat=0; float bpm=0; bool freeFall=false; unsigned long fallTime=0;

void setup(){
 Serial.begin(115200); pinMode(BUZZER_PIN,OUTPUT); Wire.begin(21,22); temp.begin();
 if(!mpu.begin()){Serial.println("MPU6050 not found");while(1)delay(100);}
 if(!max30102.begin(Wire,I2C_SPEED_FAST)){Serial.println("MAX30102 not found");while(1)delay(100);}
 max30102.setup(); max30102.setPulseAmplitudeRed(0x0A); max30102.setPulseAmplitudeIR(0x0A);
 WiFi.begin(WIFI_SSID,WIFI_PASSWORD); while(WiFi.status()!=WL_CONNECTED)delay(300);
}

void loop(){
 long ir=max30102.getIR();
 if(checkForBeat(ir)){long d=millis()-lastBeat;lastBeat=millis();float x=60.0/(d/1000.0);if(x>30&&x<220)bpm=x;}
 temp.requestTemperatures(); float tc=temp.getTempCByIndex(0);
 sensors_event_t a,g,t;mpu.getEvent(&a,&g,&t);
 float mag=sqrt(a.acceleration.x*a.acceleration.x+a.acceleration.y*a.acceleration.y+a.acceleration.z*a.acceleration.z);
 bool fall=false;
 if(mag<3.0){freeFall=true;fallTime=millis();}
 if(freeFall&&mag>20.0&&millis()-fallTime<1000){fall=true;freeFall=false;digitalWrite(BUZZER_PIN,HIGH);delay(1000);digitalWrite(BUZZER_PIN,LOW);}
 if(freeFall&&millis()-fallTime>=1000)freeFall=false;
 Serial.printf("HR %.1f | Temp %.2f C | Acc %.2f | Fall %s\n",bpm,tc,mag,fall?"YES":"NO");
 if(fall)sendData(bpm,-1,tc,a.acceleration.x,a.acceleration.y,a.acceleration.z,true);
 delay(500);
}

void sendData(float hr,float spo2,float tc,float ax,float ay,float az,bool fall){
 if(WiFi.status()!=WL_CONNECTED)return;
 HTTPClient http;http.begin(API_URL);http.addHeader("Content-Type","application/json");
 http.addHeader("Authorization",String("Bearer ")+JWT_TOKEN);
 String body="{"heart_rate":"+String(hr,1)+","spo2":"+String(spo2,1)+","temperature":"+String(tc,2)+","accel_x":"+String(ax,2)+","accel_y":"+String(ay,2)+","accel_z":"+String(az,2)+","fall_detected":"+(fall?String("true"):String("false"))+"}";
 Serial.printf("HTTP %d\n",http.POST(body));http.end();
}
