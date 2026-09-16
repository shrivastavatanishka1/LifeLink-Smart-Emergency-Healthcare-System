from flask import Flask,send_from_directory,jsonify
from flask_cors import CORS
from database import init_db
from routes.users import users_bp
from routes.health import health_bp
from routes.alerts import alerts_bp
from routes.blood import blood_bp

app=Flask(__name__,static_folder="../frontend",static_url_path="")
CORS(app);init_db()
app.register_blueprint(users_bp);app.register_blueprint(health_bp);app.register_blueprint(alerts_bp);app.register_blueprint(blood_bp)

@app.get("/api/healthcheck")
def healthcheck(): return jsonify({"status":"ok","project":"LifeLink"})

@app.get("/")
def index(): return send_from_directory(app.static_folder,"index.html")

if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)
