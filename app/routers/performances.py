import sqlite3
from fastapi import APIRouter, HTTPException, status, Depends, Header
from typing import List
from app.schemas.performance import PerformanceCreate, PerformanceResponse
from app.database import get_db_connection
from datetime import datetime

router = APIRouter(prefix="/performances", tags=["Performances"])

# Fonction pour vérifier l'authentification via token
def get_current_user(token: str):
    """Vérifie l'authentification de l'utilisateur via le token fourni.
    Args:
        token (str): Token d'authentification

    Raises:
        HTTPException: Token invalide ou expiréiption_

    Returns:
        _type_: user["id_user"]
    """
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
    """
        Args: authorization (str, optional): champ Autorization dans header

    Raises:
        HTTPException: Token manquant dans les headers ou invalide

    Returns:
         token
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token manquant dans les headers")
    token = authorization.split("Bearer ")[-1]  # Supposer que le format est 'Bearer <token>'
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
    return token

# Créer une performance
@router.post("/", response_model=PerformanceResponse)
def create_performance(performance: PerformanceCreate, token: str = Depends(get_token_from_header)):
    """Créer une performance pour l'utilisateur authentifié.
    Args:
        token (str): Token d'authentification
        performance (PerformanceCreate): Données de performance à insérer

    Post: http://localhost:8000/performance/performances/, 
    Body:
    {
    "power_max": XXX,
    "hr_max": XXX,
    "vo2_max": XXX,
    "rf_max": XXX,
    "cadence_max": XXX,
    "vo2_class": "XXX",
    "ressenti": XXX
    }
    """
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
    """Récupérer toutes les performances
    Args:
        token (str): Token d'authentification
        
    Get: http://localhost:8000/performance/performances/, 
    """
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
    """Récupérer une performance par son ID.

    Args:
        id_performance (int): performance ID
        token (str): Token d'authentification

    Raises:
        HTTPException: "Performance introuvable"

    Returns:
        _type_: PerformanceResponse
    """
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
    """Mettre à jour une performance.
    Args:
        id_performance (int): _description_
        performance (PerformanceCreate): _description_
        token (str): Token d'authentification

    Raises:
        HTTPException: Performance introuvable

    Returns:
        PerformanceResponse: Performance mise à jour
    """
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
    """Supprimer une performance.

    Args:
        id_performance (int): ID de la performance à supprimer
        token (str): Token d'authentification

    Raises:
        HTTPException: Performance introuvable

    Returns:
        PerformanceResponse: Performance supprimée
    """
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


# Lire puissance max
@router.get("/puissance/details")
def get_performance(token: str = Depends(get_token_from_header)):
    """Récupérer la performance avec la puissance maximale.
        
        token (str): Token d'authentification
        Returns:
        Performance maximale

    """
    id_user = get_current_user(token)


    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Accéder aux colonnes par nom
    cursor = conn.cursor()

    # Construction sécurisée de la requête SQL
    sql_query = f"""
        SELECT u.nom, u.prenom, date_performance,
               max(power_max) AS power_max, hr_max,
               vo2_max, rf_max, cadence_max,
               vo2_class, ressenti
        FROM performances p  join users u on p.id_user = u.id_user
    """

    cursor.execute(sql_query)
    row = cursor.fetchone()
    conn.close()

    if row:
        # Renvoie un dictionnaire avec uniquement les champs que vous voulez
        return {
            "nom": row["nom"],
            "prenom": row["prenom"],
            "date_performance": row["date_performance"],
            "power_max": row["power_max"],
            "hr_max": row["hr_max"],
            "vo2_max": row["vo2_max"],
            "rf_max": row["rf_max"],
            "cadence_max": row["cadence_max"],
            "vo2_class": row["vo2_class"],
            "ressenti": row["ressenti"]
        }
    else:
        return {"message": "Aucune performance trouvée."}

# Lire puissance max
@router.get("/puissance/detail/{id_user}")
def get_performance(id_user: int, token: str = Depends(get_token_from_header)):
    """Récupérer pour un utilisateur donnée la performance avec la puissance maximale.
        
        token (str): Token d'authentification
        Returns:
                Performance maximale
    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Accéder aux colonnes par nom
    cursor = conn.cursor()

    # Construction sécurisée de la requête SQL
    sql_query = f"""
        SELECT u.nom, u.prenom, date_performance,
               max(power_max) AS power_max, hr_max,
               vo2_max, rf_max, cadence_max,
               vo2_class, ressenti
        FROM performances p  join users u on p.id_user = u.id_user
        WHERE p.id_user = ?
    """

    cursor.execute(sql_query, (id_user,))
    row = cursor.fetchone()
    conn.close()

    if row:
        # Renvoie un dictionnaire avec uniquement les champs que vous voulez
        return {
            "nom": row["nom"],
            "prenom": row["prenom"],
            "date_performance": row["date_performance"],
            "power_max": row["power_max"],
            "hr_max": row["hr_max"],
            "vo2_max": row["vo2_max"],
            "rf_max": row["rf_max"],
            "cadence_max": row["cadence_max"],
            "vo2_class": row["vo2_class"],
            "ressenti": row["ressenti"]
        }
    else:
        return {"message": "Aucune performance trouvée."}

# Lire VO2max max
@router.get("/VO2max/details")
def get_performance(token: str = Depends(get_token_from_header)):
    """Récupérer la performance avec VO2max.
        
        token (str): Token d'authentification
        Returns:
        l'athlète avec la performance maximale (VO2max)

    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Accéder aux colonnes par nom
    cursor = conn.cursor()

    # Construction sécurisée de la requête SQL
    sql_query = f"""
        SELECT u.nom, u.prenom, date_performance,
               power_max, hr_max,
               max(vo2_max) AS VO2_max, rf_max, cadence_max,
               vo2_class, ressenti
        FROM performances p  join users u on p.id_user = u.id_user
    """

    cursor.execute(sql_query)
    row = cursor.fetchone()
    conn.close()

    if row:
        # Renvoie un dictionnaire avec uniquement les champs que vous voulez
        return {
            "nom": row["nom"],
            "prenom": row["prenom"],
            "date_performance": row["date_performance"],
            "power_max": row["power_max"],
            "hr_max": row["hr_max"],
            "vo2_max": row["vo2_max"],
            "rf_max": row["rf_max"],
            "cadence_max": row["cadence_max"],
            "vo2_class": row["vo2_class"],
            "ressenti": row["ressenti"]
        }
    else:
        return {"message": "Aucune performance trouvée."}
    
# Lire VO2max max
@router.get("/VO2max/detail/{id_user}")
def get_performance(id_user: int, token: str = Depends(get_token_from_header)):
    """Récupérer pour un utilisateur la performance avec VO2max.
        
        token (str): Token d'authentification
        Returns:
        l'athlète avec la performance maximale (VO2max)

    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Accéder aux colonnes par nom
    cursor = conn.cursor()

    # Construction sécurisée de la requête SQL
    sql_query = f"""
        SELECT u.nom, u.prenom, date_performance,
               power_max, hr_max,
               max(vo2_max) AS VO2_max, rf_max, cadence_max,
               vo2_class, ressenti
        FROM performances p  join users u on p.id_user = u.id_user
        WHERE p.id_user = ?
    """

    cursor.execute(sql_query, (id_user,))
    row = cursor.fetchone()
    conn.close()

    if row:
        # Renvoie un dictionnaire avec uniquement les champs que vous voulez
        return {
            "nom": row["nom"],
            "prenom": row["prenom"],
            "date_performance": row["date_performance"],
            "power_max": row["power_max"],
            "hr_max": row["hr_max"],
            "vo2_max": row["vo2_max"],
            "rf_max": row["rf_max"],
            "cadence_max": row["cadence_max"],
            "vo2_class": row["vo2_class"],
            "ressenti": row["ressenti"]
        }
    else:
        return {"message": "Aucune performance trouvée."}
    
# Lire rapport poids/puissance max
@router.get("/poidspuissance/details")
def get_performances(token: str = Depends(get_token_from_header)): 
    """Récupérer le meilleur rapport puissance max / poids moyenne .
        
        token (str): Token d'authentification
        Returns:
        l'athlète avec le rapport puissance max / poids maximum

    """
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Accéder aux colonnes par nom
    cursor = conn.cursor()

    # Construction sécurisée de la requête SQL
    sql_query = f"""
        SELECT u.nom, u.prenom, AVG(p.power_max / d.weight) AS rapport_moyen
        FROM users u
        JOIN performances p ON u.id_user = p.id_user
        JOIN details d ON u.id_user = d.id_user
        GROUP BY u.nom, u.prenom
        ORDER BY rapport_moyen DESC
        LIMIT 1;
    """

    cursor.execute(sql_query,)
    row = cursor.fetchone()
    conn.close()

    if row:
        # Renvoie un dictionnaire avec uniquement les champs que vous voulez
        return {
            "nom": row["nom"],
            "prenom": row["prenom"],
            "rapport_moyen": row["rapport_moyen"]
        }
    else:
        return {"message": "Aucune performance trouvée."}