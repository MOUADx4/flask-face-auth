from flask import Flask, render_template, request, redirect, flash, session, jsonify
from functools import wraps
from datetime import datetime
import bcrypt
import json
import numpy as np

from connect import get_users_table
from face_auth import extract_face_encoding, compare_encodings



#   CONFIG FLASK

app = Flask(__name__)
app.secret_key = "supersecretkey"   



#   DECORATEURS

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            flash("Vous devez être connecté.", "error")
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper



#   ROUTES 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        table = get_users_table()
        user = table.get_item(Key={"email": email})

        if "Item" not in user:
            flash("Email introuvable.", "error")
            return redirect("/login")

        user = user["Item"]

        if not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            flash("Mot de passe incorrect.", "error")
            return redirect("/login")

        session["user"] = email
        flash("Connexion réussie !", "success")
        return redirect("/")

    return render_template("login.html", title="Connexion")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        face_image = request.form.get("face_image") 

        table = get_users_table()

        # Vérifier doublon
        existing = table.get_item(Key={"email": email})
        if "Item" in existing:
            flash("Cet email est déjà utilisé.", "error")
            return redirect("/register")

        # Hash du mot de passe
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        # Extraction encodage facial
        face_encoding = None
        if face_image:
            encoding = extract_face_encoding(face_image)
            if encoding is None:
                flash("Aucun visage détecté. Réessayez.", "error")
                return redirect("/register")

            face_encoding = json.dumps(encoding.tolist())

        # Enregistrer dans DynamoDB
        table.put_item(Item={
            "email": email,
            "password": hashed,
            "created_at": datetime.utcnow().isoformat(),
            "face_encoding": face_encoding
        })

        flash("Compte créé avec succès !", "success")
        return redirect("/login")

    return render_template("register.html", title="Inscription")


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Vous êtes déconnecté.", "success")
    return redirect("/login")


@app.route("/test-db")
def test_db():
    table = get_users_table()
    return {"status": "ok", "table": table.table_name}



#   ROUTES PROTÉGÉES

@app.route("/")
@login_required
def index():
    return render_template("index.html", title="Accueil")


@app.route("/profile")
@login_required
def profile():
    table = get_users_table()
    user = table.get_item(Key={"email": session["user"]})

    if "Item" not in user:
        flash("Utilisateur introuvable.", "error")
        return redirect("/")

    return render_template("profile.html", user=user["Item"], title="Profil")


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")



#   API : AUTH FACIALE

@app.route("/login/face", methods=["POST"])
def login_face():
    data = request.get_json()

    if not data or "image" not in data:
        return jsonify({"success": False, "message": "Image manquante"}), 400

    email = data.get("email")
    if not email:
        return jsonify({"success": False, "message": "Email manquant"}), 400

    # Extraire encodage du visage envoyé
    candidate_encoding = extract_face_encoding(data["image"])
    if candidate_encoding is None:
        return jsonify({"success": False, "message": "Aucun visage détecté"}), 400

    # Récupérer utilisateur
    table = get_users_table()
    user = table.get_item(Key={"email": email})

    if "Item" not in user:
        return jsonify({"success": False, "message": "Utilisateur introuvable"}), 404

    user = user["Item"]

    if "face_encoding" not in user or not user["face_encoding"]:
        return jsonify({"success": False, "message": "Aucun visage enregistré"}), 400

    # Convertir JSON → numpy array
    stored_encoding = np.array(json.loads(user["face_encoding"]))

    # Comparaison
    match = compare_encodings(stored_encoding, candidate_encoding)

    if match:
        session["user"] = email
        return jsonify({"success": True, "message": "Connexion faciale réussie"})

    return jsonify({"success": False, "message": "Visage non reconnu"})


#   RUN

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


