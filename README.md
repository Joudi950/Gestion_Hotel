# 🏨 Hôtel Royale — Système de Gestion Hôtelière

> Projet universitaire — Mini Projet C converti en application web full-stack.

---

## 📋 Description

Ce projet est un **système de gestion hôtelière** développé en deux phases :

1. **Phase 1 (C — Structures dynamiques)** : Application console en langage C utilisant des listes chaînées pour gérer les clients, les chambres et les réservations d'un hôtel. Les données sont persistées dans des fichiers `.txt`.

2. **Phase 2 (Web — Full Stack)** : Transformation du projet C en une application web moderne avec un backend Python (Flask) et un frontend HTML/CSS/JS, offrant une interface graphique complète pour toutes les opérations.

---

## ✨ Fonctionnalités

### 👤 Gestion des Clients
- Ajouter un client (CIN, nom, prénom, téléphone, email)
- Modifier les informations d'un client
- Supprimer un client
- Rechercher un client par nom ou CIN

### 🛏️ Gestion des Chambres
- Ajouter / modifier / supprimer une chambre
- Types : Simple, Double, Suite, Suite Prestige
- Suivi du statut en temps réel (Disponible / Occupée)
- Filtrage par statut

### 📅 Gestion des Réservations
- Créer une réservation (client + chambre + dates check-in / check-out)
- Annuler une réservation (libère automatiquement la chambre)
- Historique complet des réservations

### 📊 Tableau de Bord
- Statistiques en temps réel (nombre de clients, chambres, réservations)
- Taux d'occupation avec barre de progression
- Répartition des chambres par type

---

## 🛠️ Technologies utilisées

| Couche | Technologie |
|--------|-------------|
| Backend | Python 3 · Flask · Flask-CORS |
| Frontend | HTML5 · CSS3 · JavaScript (Vanilla) |
| Stockage | JSON (fichier local `data.json`) |
| Langage original | C (listes chaînées, fichiers .txt) |

---

##  Structure du projet

```
mini_projet/
│
├── app.py          # Backend Flask — API REST
├── index.html      # Frontend — Interface web complète
├── data.json       # Base de données JSON (générée automatiquement)
└── README.md       # Ce fichier
```

---

##  Installation & Lancement

### Prérequis
- Python 3.x installé
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-username/hotel-royale.git
cd hotel-royale

# 2. Installer les dépendances
pip install flask flask-cors

# 3. Lancer le serveur
python app.py

# 4. Ouvrir dans le navigateur
# http://127.0.0.1:5050
```

> ⚠️ `app.py` et `index.html` doivent être dans le **même dossier**.

---

##  API REST — Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/` | Interface web |
| GET | `/api/stats` | Statistiques générales |
| GET | `/api/clients` | Liste des clients |
| POST | `/api/clients` | Ajouter un client |
| PUT | `/api/clients/<id>` | Modifier un client |
| DELETE | `/api/clients/<id>` | Supprimer un client |
| GET | `/api/chambres` | Liste des chambres |
| POST | `/api/chambres` | Ajouter une chambre |
| PUT | `/api/chambres/<num>` | Modifier une chambre |
| DELETE | `/api/chambres/<num>` | Supprimer une chambre |
| GET | `/api/reservations` | Liste des réservations |
| POST | `/api/reservations` | Créer une réservation |
| DELETE | `/api/reservations/<id>` | Annuler une réservation |

---

##  Aperçu

```
┌─────────────────────────────────────────────────────┐
│  HÔTEL        ◈ Tableau de bord                     │
│  ROYALE       ◉ Clients          5 clients          │
│               ▣ Chambres         7 chambres          │
│  Système de   ◎ Réservations     3 réservations      │
│  Gestion                                             │
│               Taux d'occupation : 43%               │
└─────────────────────────────────────────────────────┘
```

---

##  Auteur

Projet réalisé dans le cadre d'un cours de **Structures de Données en C** (Séance 6 — Listes chaînées dynamiques), étendu vers une application web full-stack.

---

##  Licence

Projet académique — Usage éducatif uniquement.
