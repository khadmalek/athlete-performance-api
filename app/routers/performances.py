from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import List
from app.schemas.performance import PerformanceCreate, PerformanceResponse
from app.database import get_db_connection
from datetime import datetime

router = APIRouter(prefix="/performances", tags=["Performances"])

# Fonction pour vérifier l'authentification via token
def get_current_user(token: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_user FROM users WHERE token = ?", (token,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expiré")

    return user["id_user"]

# Fonction pour extraire le token de l'Authorization header
def get_token_from_header(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token manquant dans les headers")
    token = authorization.split("Bearer ")[-1]  # Supposer que le format est 'Bearer <token>'
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    return token

# Créer une performance
@router.post("/", response_model=PerformanceResponse)
def create_performance(performance: PerformanceCreate, token: str = Depends(get_token_from_header)):
    id_user = get_current_user(token)
    date_performance = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Enregistre la date et l'heure actuelles

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO performances (id_user, power_max, hr_max, vo2_max, rf_max, cadence_max, vo2_class, ressenti, date_performance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (id_user, performance.power_max, performance.hr_max, performance.vo2_max,
          performance.rf_max, performance.cadence_max, performance.vo2_class, 
          performance.ressenti, date_performance))
    conn.commit()

    id_performance = cursor.lastrowid
    cursor.execute("SELECT * FROM performances WHERE id_performance = ?", (id_performance,))
    new_performance = cursor.fetchone()
    conn.close()

    return dict(new_performance)

# Lire toutes les performances d'un utilisateur
@router.get("/", response_model=List[PerformanceResponse])
def get_performances(token: str = Depends(get_token_from_header)):
    id_user = get_current_user(token)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performances WHERE id_user = ?", (id_user,))
    performances = cursor.fetchall()
    conn.close()

    return [dict(performance) for performance in performances]

# Lire une seule performance par ID
@router.get("/{id_performance}", response_model=PerformanceResponse)
def get_performance(id_performance: int, token: str = Depends(get_token_from_header)):
    id_user = get_current_user(token)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performances WHERE id_performance = ? AND id_user = ?", (id_performance, id_user))
    performance = cursor.fetchone()
    conn.close()

    if not performance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performance introuvable")

    return dict(performance)

# Mettre à jour une performance
@router.put("/{id_performance}", response_model=PerformanceResponse)
def update_performance(id_performance: int, performance: PerformanceCreate, token: str = Depends(get_token_from_header)):
    id_user = get_current_user(token)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performances WHERE id_performance = ? AND id_user = ?", (id_performance, id_user))
    existing_performance = cursor.fetchone()

    if not existing_performance:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performance introuvable")

    cursor.execute(''' 
        UPDATE performances
        SET power_max=?, hr_max=?, vo2_max=?, rf_max=?, cadence_max=?, vo2_class=?, ressenti=?
        WHERE id_performance=? AND id_user=?
    ''', (performance.power_max, performance.hr_max, performance.vo2_max, 
          performance.rf_max, performance.cadence_max, performance.vo2_class, 
          performance.ressenti, id_performance, id_user))
    conn.commit()

    cursor.execute("SELECT * FROM performances WHERE id_performance = ?", (id_performance,))
    updated_performance = cursor.fetchone()
    conn.close()

    return dict(updated_performance)

# Supprimer une performance
@router.delete("/{id_performance}", response_model=PerformanceResponse, status_code=status.HTTP_200_OK)
def delete_performance(id_performance: int, token: str = Depends(get_token_from_header)):
    id_user = get_current_user(token)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM performances WHERE id_performance = ? AND id_user = ?", (id_performance, id_user))
    existing_performance = cursor.fetchone()

    if not existing_performance:
        conn.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Performance introuvable")

    # Sauvegarder les détails de la performance avant la suppression
    performance_to_delete = dict(existing_performance)

    # Supprimer la performance
    cursor.execute("DELETE FROM performances WHERE id_performance = ?", (id_performance,))
    conn.commit()
    conn.close()

    # Retourner la performance supprimée dans la réponse
    return performance_to_delete

