# Flask Face Auth — Authentification Sécurisée avec Reconnaissance Faciale

Application web moderne permettant une authentification hybride :

- 🔐 Email / Mot de passe  
- 👤 Reconnaissance faciale via webcam  
- ☁️ Stockage cloud avec DynamoDB  

---

## Présentation

Ce projet consiste à développer une application web sécurisée basée sur Flask, intégrant :

- une authentification classique
- une authentification biométrique (visage)
- une base de données NoSQL (DynamoDB)

---

## Fonctionnalités

### Authentification classique
- Inscription avec email + mot de passe
- Validation des champs
- Refus des doublons
- Hash sécurisé des mots de passe (bcrypt)
- Gestion de session avec Flask

### Authentification faciale
- Capture webcam (JavaScript)
- Conversion image → base64
- Extraction d’encodage facial (128 dimensions)
- Comparaison intelligente avec les données stockées

---

## Modélisation DynamoDB

### Table : `users`

| Attribut | Type | Description |
|--------|------|------------|
| PK (Partition Key) | email (String) | Identifiant unique |
| SK (Sort Key) | created_at (String) | Date de création |
| password | String | Mot de passe hashé |
| face_encoding | List<Float> | Encodage facial |
| created_at | String | Date |

---

## Structure du projet

flask-face-auth/
│── app.py  
│── connect.py  
│── face_auth.py  
│── requirements.txt  
│── Dockerfile  
│── docker-compose.yml  
│── templates/  
│   ├── login.html  
│   ├── register.html  
│   ├── index.html  
│── static/  
│   ├── js/  
│   │   └── face_capture.js  

---

## Installation

```bash
git clone https://github.com/MOUADx4/flask-face-auth.git
cd flask-face-auth
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Créer `.env` :

```
AWS_ACCESS_KEY_ID=xxxx
AWS_SECRET_ACCESS_KEY=xxxx
AWS_REGION=eu-west-1
```

Lancer :

```bash
python app.py
```

---

## Docker

```bash
docker compose up --build
```

---

## Sécurité

- Hash bcrypt
- Pas d’image stockée
- Données sensibles dans .env
- Sessions sécurisées

---

## Routes

- /register
- /login
- /login/face
- /logout

---

## Auteur

Mouad Bounokra
