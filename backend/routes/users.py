from flask import Blueprint, request, jsonify
from database import get_db
from auth import hash_password, verify_password, create_token, token_required

users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.post("/register")
def register():
    d = request.get_json(silent=True) or {}
    if not d.get("name") or not d.get("password") or not d.get("role"):
        return jsonify({"error":"name, role and password are required"}),400
    if d["role"] not in ("patient","caregiver","doctor"):
        return jsonify({"error":"invalid role"}),400
    age = int(d["age"]) if d.get("age") else None
    if age is not None and not 0 < age <= 130:
        return jsonify({"error":"invalid age"}),400
    conn=get_db()
    cur=conn.execute("""INSERT INTO users
    (role,name,age,blood_group,emergency_contact,allergies,medicines,medical_history,password_hash)
    VALUES (?,?,?,?,?,?,?,?,?)""",(
        d["role"],d["name"].strip(),age,d.get("blood_group"),d.get("emergency_contact",""),
        d.get("allergies",""),d.get("medicines",""),d.get("medical_history",""),
        hash_password(d["password"])))
    conn.commit(); conn.close()
    return jsonify({"message":"Registration successful","user_id":cur.lastrowid}),201

@users_bp.post("/login")
def login():
    d=request.get_json(silent=True) or {}
    conn=get_db()
    user=conn.execute("SELECT * FROM users WHERE name=? ORDER BY id DESC LIMIT 1",(str(d.get("name","")).strip(),)).fetchone()
    conn.close()
    if not user or not verify_password(d.get("password",""),user["password_hash"]):
        return jsonify({"error":"Invalid name or password"}),401
    return jsonify({"token":create_token(user),"user":{"id":user["id"],"name":user["name"],"role":user["role"],"blood_group":user["blood_group"]}})

@users_bp.get("/me")
@token_required()
def me(payload):
    conn=get_db()
    user=conn.execute("""SELECT id,role,name,age,blood_group,emergency_contact,allergies,medicines,medical_history,created_at FROM users WHERE id=?""",(payload["sub"],)).fetchone()
    conn.close()
    return jsonify(dict(user)) if user else (jsonify({"error":"not found"}),404)
