from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os, datetime

app = Flask(__name__, static_folder=os.path.dirname(__file__))
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

# ── Seed data ────────────────────────────────────────────────────────────────
SEED = {
    "clients": [
        {"id_client": 10001, "nom": "Ben Ali",    "prenom": "Ahmed",   "telephone": "21 234 567", "email": "ahmed@mail.tn",   "num_chambre": 101},
        {"id_client": 10002, "nom": "Trabelsi",   "prenom": "Fatma",   "telephone": "25 876 543", "email": "fatma@mail.tn",   "num_chambre": -1},
        {"id_client": 10003, "nom": "Mansouri",   "prenom": "Karim",   "telephone": "29 111 222", "email": "karim@mail.tn",   "num_chambre": 203},
        {"id_client": 10004, "nom": "Chaouachi",  "prenom": "Sana",    "telephone": "20 333 444", "email": "sana@mail.tn",    "num_chambre": -1},
        {"id_client": 10005, "nom": "Riahi",      "prenom": "Youssef", "telephone": "52 555 666", "email": "youssef@mail.tn", "num_chambre": 302},
    ],
    "chambres": [
        {"num_chambre": 101, "type_chambre": 1, "prix": 120.00, "statut": 1},
        {"num_chambre": 102, "type_chambre": 1, "prix": 120.00, "statut": 0},
        {"num_chambre": 201, "type_chambre": 2, "prix": 200.00, "statut": 0},
        {"num_chambre": 203, "type_chambre": 2, "prix": 200.00, "statut": 1},
        {"num_chambre": 301, "type_chambre": 3, "prix": 350.00, "statut": 0},
        {"num_chambre": 302, "type_chambre": 3, "prix": 350.00, "statut": 1},
        {"num_chambre": 401, "type_chambre": 4, "prix": 500.00, "statut": 0},
    ],
    "reservations": [
        {"id_reservation": 1001, "id_client": 10001, "num_chambre": 101, "checkin": "2025-03-01", "checkout": "2025-03-07"},
        {"id_reservation": 1002, "id_client": 10003, "num_chambre": 203, "checkin": "2025-03-10", "checkout": "2025-03-15"},
        {"id_reservation": 1003, "id_client": 10005, "num_chambre": 302, "checkin": "2025-03-12", "checkout": "2025-03-20"},
    ]
}

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(SEED)
        return SEED
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

TYPE_LABELS = {1: "Simple", 2: "Double", 3: "Suite", 4: "Suite Prestige"}

import re
from datetime import datetime, date

def error(msg):
    return jsonify({"error": msg}), 400

def validate_alpha(s, field):
    s = s.strip()
    if not re.match(r"^[A-Za-zÀ-ÁÄÆÇÈ-ËÌ-ÏÐÑÒ-ÖØÙ-ÜÝßà-ÿ\\s]+$", s) or len(s) < 2:
        raise ValueError(f"{field} doit contenir alphabets seulement (min 2 chars)")
    return s

def validate_phone(s):
    s = re.sub(r"\\s+", " ", s.strip())
    if not re.match(r"^[0-9\\s]{8,12}$", s) or len(re.sub(r"\\s", "", s)) < 8:
        raise ValueError("Téléphone invalide (8-12 chiffres)")
    return s

def validate_email(s):
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$", s.strip()):
        raise ValueError("Email invalide")
    return s.strip()

def validate_int_positive(val, field, min_val=1):
    try:
        v = int(val)
        if v < min_val:
            raise ValueError(f"{field} doit être >= {min_val}")
        return v
    except:
        raise ValueError(f"{field} doit être un nombre entier")

def validate_float_positive(val, field):
    try:
        v = float(val)
        if v <= 0:
            raise ValueError(f"{field} doit être > 0")
        return v
    except:
        raise ValueError(f"{field} doit être un nombre")

def validate_date(dstr, field):
    try:
        d = date.fromisoformat(dstr)
        if d < date.today():
            raise ValueError(f"{field} doit être aujourd'hui ou future")
        return dstr
    except:
        raise ValueError(f"{field} date invalide (YYYY-MM-DD)")

def validate_client_body(body):
    body['id_client'] = validate_int_positive(body['id_client'], "ID Client", 10000)
    body['nom'] = validate_alpha(body['nom'], "Nom")
    body['prenom'] = validate_alpha(body['prenom'], "Prénom")
    body['telephone'] = validate_phone(body['telephone'])
    if 'email' in body:
        body['email'] = validate_email(body['email'])
    body.setdefault('num_chambre', -1)
    return body

def validate_chambre_body(body):
    body['num_chambre'] = validate_int_positive(body['num_chambre'], "N° Chambre")
    body['prix'] = validate_float_positive(body['prix'], "Prix")
    body['type_chambre'] = validate_int_positive(body['type_chambre'], "Type", 1)
    if body['type_chambre'] not in [1,2,3,4]:
        raise ValueError("Type chambre invalide (1-4)")
    body['statut'] = validate_int_positive(body['statut'], "Statut", 0)
    if body['statut'] not in [0,1]:
        raise ValueError("Statut invalide (0=dispo, 1=occupée)")
    return body

def validate_res_body(data, body):
    body['id_client'] = validate_int_positive(body['id_client'], "ID Client")
    body['num_chambre'] = validate_int_positive(body['num_chambre'], "N° Chambre")
    checkin = validate_date(body['checkin'], "Check-in")
    checkout = validate_date(body['checkout'], "Check-out")
    if date.fromisoformat(checkin) >= date.fromisoformat(checkout):
        raise ValueError("Check-out doit être après Check-in")
    client = next((c for c in data['clients'] if c['id_client'] == body['id_client']), None)
    if not client:
        raise ValueError("Client inexistant")
    chambre = next((ch for ch in data['chambres'] if ch['num_chambre'] == body['num_chambre']), None)
    if not chambre:
        raise ValueError("Chambre inexistante")
    if chambre['statut'] != 0:
        raise ValueError("Chambre occupée")
    return body

# ── CLIENTS ──────────────────────────────────────────────────────────────────
@app.route('/api/clients', methods=['GET'])
def get_clients():
    return jsonify(load_data()['clients'])

@app.route('/api/clients', methods=['POST'])
def add_client():
    data = load_data()
    try:
        body = validate_client_body(request.json)
    except ValueError as e:
        return error(str(e))
    if any(c['id_client'] == body['id_client'] for c in data['clients']):
        return error("ID Client déjà utilisé")
    data['clients'].append(body)
    save_data(data)
    return jsonify(body), 201

@app.route('/api/clients/<int:cid>', methods=['PUT'])
def update_client(cid):
    data = load_data()
    client = next((c for c in data['clients'] if c['id_client'] == cid), None)
    if not client:
        return jsonify({"error": "Client introuvable"}), 404
    try:
        body = validate_client_body({**request.json, 'id_client': cid})
    except ValueError as e:
        return error(str(e))
    client.update({k: v for k, v in body.items() if k != 'id_client'})
    save_data(data)
    return jsonify(client)

@app.route('/api/clients/<int:cid>', methods=['DELETE'])
def delete_client(cid):
    data = load_data()
    data['clients'] = [c for c in data['clients'] if c['id_client'] != cid]
    save_data(data)
    return jsonify({"ok": True})

# ── CHAMBRES ─────────────────────────────────────────────────────────────────
@app.route('/api/chambres', methods=['GET'])
def get_chambres():
    chambres = load_data()['chambres']
    for ch in chambres:
        ch['type_label'] = TYPE_LABELS.get(ch['type_chambre'], "Inconnu")
        ch['statut_label'] = "Occupée" if ch['statut'] == 1 else "Disponible"
    return jsonify(chambres)

@app.route('/api/chambres', methods=['POST'])
def add_chambre():
    data = load_data()
    try:
        body = validate_chambre_body(request.json)
    except ValueError as e:
        return error(str(e))
    if any(c['num_chambre'] == body['num_chambre'] for c in data['chambres']):
        return error("N° Chambre déjà utilisé")
    data['chambres'].append(body)
    save_data(data)
    return jsonify(body), 201

@app.route('/api/chambres/<int:num>', methods=['PUT'])
def update_chambre(num):
    data = load_data()
    chambre = next((ch for ch in data['chambres'] if ch['num_chambre'] == num), None)
    if not chambre:
        return jsonify({"error": "Chambre introuvable"}), 404
    try:
        body = validate_chambre_body({**request.json, 'num_chambre': num})
    except ValueError as e:
        return error(str(e))
    chambre.update({k: v for k, v in body.items() if k != 'num_chambre'})
    save_data(data)
    return jsonify(chambre)

@app.route('/api/chambres/<int:num>', methods=['DELETE'])
def delete_chambre(num):
    data = load_data()
    data['chambres'] = [c for c in data['chambres'] if c['num_chambre'] != num]
    save_data(data)
    return jsonify({"ok": True})

# ── RÉSERVATIONS ─────────────────────────────────────────────────────────────
@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    data = load_data()
    clients_map = {c['id_client']: c for c in data['clients']}
    chambres_map = {ch['num_chambre']: ch for ch in data['chambres']}
    result = []
    for r in data['reservations']:
        client = clients_map.get(r['id_client'], {})
        chambre = chambres_map.get(r['num_chambre'], {})
        result.append({
            **r,
            "client_nom": f"{client.get('prenom','')} {client.get('nom','')}".strip(),
            "type_chambre": TYPE_LABELS.get(chambre.get('type_chambre', 0), "—"),
            "prix": chambre.get('prix', 0),
        })
    return jsonify(result)

@app.route('/api/reservations', methods=['POST'])
def add_reservation():
    data = load_data()
    try:
        body = validate_res_body(data, request.json)
    except ValueError as e:
        return error(str(e))
    new_id = max((r['id_reservation'] for r in data['reservations']), default=1000) + 1
    body['id_reservation'] = new_id
    # Mark chambre as occupied
    for ch in data['chambres']:
        if ch['num_chambre'] == body['num_chambre']:
            ch['statut'] = 1
            break
    data['reservations'].append(body)
    save_data(data)
    return jsonify(body), 201

@app.route('/api/reservations/<int:rid>', methods=['DELETE'])
def delete_reservation(rid):
    data = load_data()
    res = next((r for r in data['reservations'] if r['id_reservation'] == rid), None)
    if res:
        for ch in data['chambres']:
            if ch['num_chambre'] == res['num_chambre']:
                ch['statut'] = 0
    data['reservations'] = [r for r in data['reservations'] if r['id_reservation'] != rid]
    save_data(data)
    return jsonify({"ok": True})

# ── STATS ─────────────────────────────────────────────────────────────────────
@app.route('/api/stats', methods=['GET'])
def get_stats():
    data = load_data()
    nb_dispo = sum(1 for c in data['chambres'] if c['statut'] == 0)
    nb_occ   = sum(1 for c in data['chambres'] if c['statut'] == 1)
    return jsonify({
        "nb_clients": len(data['clients']),
        "nb_chambres": len(data['chambres']),
        "nb_reservations": len(data['reservations']),
        "nb_disponibles": nb_dispo,
        "nb_occupees": nb_occ,
    })

if __name__ == '__main__':
    app.run(port=5050, debug=False)
