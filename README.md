# Athlete Performance API

L'**Athlete Performance API** est une application FastAPI conçue pour gérer les performances des athlètes. Elle permet aux utilisateurs (coachs et athlètes) de suivre et d'analyser les performances sportives, telles que la puissance maximale, la VO2 max, et d'autres métriques clés.

---

## Fonctionnalités principales

- **Gestion des utilisateurs** : Création, lecture, mise à jour et suppression des utilisateurs (coachs et athlètes).
- **Gestion des performances** : Enregistrement et analyse des performances sportives.
- **Authentification** : Sécurisation des routes avec des tokens JWT.
- **Base de données SQLite** : Stockage des données dans une base de données locale.

---

## Technologies utilisées

- **FastAPI** : Framework Python pour la création d'API.
- **SQLite** : Base de données légère et facile à utiliser.
- **Pydantic** : Validation des données et schémas.
- **JWT** : Authentification sécurisée avec des tokens.
- **Bcrypt** : Hachage des mots de passe.

---

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/athlete-performance-api.git
   cd athlete-performance-api
   ```

2. Créez un environnement virtuel :
   ```bash
   python -m venv .venv
   ```

3. Activez l'environnement virtuel :
   - Sur Windows :
     ```bash
     .venv\Scripts\activate
     ```
   - Sur macOS/Linux :
     ```bash
     source .venv/bin/activate
     ```

4. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

5. Créez un fichier `.env` à la racine du projet avec les variables suivantes :
   ```bash
   SECRET_KEY="votre_clé_secrète"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES="1440"
   ```

6. Lancez l'application :
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Utilisation

### Routes disponibles

#### Authentification
- **POST `/auth/login`** : Connexion d'un utilisateur.
- **POST `/auth/register`** : Enregistrement d'un nouvel utilisateur.

#### Utilisateurs
- **POST `/admin/users/`** : Créer un utilisateur.
- **GET `/admin/users/{user_id}`** : Récupérer un utilisateur par son ID.
- **PUT `/admin/users/{user_id}`** : Mettre à jour un utilisateur.
- **DELETE `/admin/users/{user_id}`** : Supprimer un utilisateur.

#### Performances
- **POST `/performance/performances/`** : Créer une performance.
- **GET `/performance/performances/`** : Récupérer toutes les performances.
- **GET `/performance/performances/{id_performance}`** : Récupérer une performance par son ID.
- **PUT `/performance/performances/{id_performance}`** : Mettre à jour une performance.
- **DELETE `/performance/performances/{id_performance}`** : Supprimer une performance.

#### Détails des utilisateurs
- **POST `/admin/details/{id_user}`** : Créer des détails pour un utilisateur.
- **GET `/admin/details/{id_user}`** : Récupérer les détails d'un utilisateur.
- **PUT `/admin/details/{id_user}`** : Mettre à jour les détails d'un utilisateur.
- **DELETE `/admin/details/{id_user}`** : Supprimer les détails d'un utilisateur.

---

## Exemples de requêtes

### Créer un utilisateur
```bash
curl -X POST "http://localhost:8000/admin/users/" \
-H "Content-Type: application/json" \
-d '{
  "username": "johndoe",
  "nom": "Doe",
  "prenom": "John",
  "email": "john.doe@example.com",
  "password": "password123",
  "role": "athlete"
}'
```

### Créer une performance
```bash
curl -X POST "http://localhost:8000/performance/performances/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{
  "power_max": 300,
  "hr_max": 180,
  "vo2_max": 60,
  "rf_max": 90,
  "cadence_max": 100,
  "vo2_class": "excellent",
  "ressenti": 8
}'
```

---

## Structure du projet

```
athlete-performance-api/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── details.py
│   │   ├── performances.py
│   │   └── users.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── details.py
│   │   ├── performance.py
│   │   └── user.py
│   └── utils/
│       ├── __init__.py
│       └── security.py
├── requirements.txt
└── README.md
```

---

## Contribution

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalité`).
3. Committez vos changements (`git commit -m 'Ajouter une nouvelle fonctionnalité'`).
4. Pushez la branche (`git push origin feature/nouvelle-fonctionnalité`).
5. Ouvrez une Pull Request.

---

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Auteur

- **Votre Nom** - [@votre-utilisateur](https://github.com/votre-utilisateur)

---

## Remerciements

- FastAPI pour leur excellent framework.
- La communauté Python pour son soutien.

---

**Enjoy!** 🚀
