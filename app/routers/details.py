from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas.details import DetailsCreate, DetailsResponse

router = APIRouter(prefix="/details", tags=["Details"])

@router.post("/{id_user}", response_model=DetailsResponse)
def create_details(id_user: int, details: DetailsCreate):
    """Créer des détails pour un utilisateur.
   
    Input: id_user, details

    Post: localhost:8000/admin/details/{id_user}, 
    
    Body:{
    "gender": "XXXX",
    "age": XX,
    "weight": XX,
    "height": XXX
    }
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Vérifier si l'utilisateur existe
        cursor.execute("SELECT id_user FROM users WHERE id_user = ?", (id_user,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Vérifier si l'utilisateur a déjà des détails
        cursor.execute("SELECT id_details FROM details WHERE id_user = ?", (id_user,))
        existing_details = cursor.fetchone()

        if existing_details:
            raise HTTPException(status_code=400, detail="User already has details")

        # Insérer les détails
        cursor.execute('''
            INSERT INTO details (id_user, gender, age, weight, height)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_user, details.gender, details.age, details.weight, details.height))

        conn.commit()
        details_id = cursor.lastrowid
        
        # Créer la réponse avec les données insérées
        return DetailsResponse(
            id_details=details_id, 
            id_user=id_user, 
            gender=details.gender,
            age=details.age,
            weight=details.weight,
            height=details.height
        )
    except HTTPException:
        conn.rollback()
        raise  # Relancer directement l'exception HTTP

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))  # Gestion des autres erreurs

    finally:
        cursor.close()
        conn.close()  # Assurez-vous que la connexion est toujours fermée proprement

@router.get("/{id_user}", response_model=DetailsResponse)
def get_details(id_user: int):
    """Récupérer les détails d'un utilisateur.

    Input: id_user

    Get, localhost:8000/admin/users/{id_user}
    
    Output: details"""

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM details WHERE id_user = ?", (id_user,))
    details = cursor.fetchone()
    conn.close()

    if not details:
        raise HTTPException(status_code=404, detail="Details not found")

    return DetailsResponse(**dict(details))

@router.put("/{id_user}")
def update_details(id_user: int, details: DetailsCreate):
    """Mettre à jour les détails d'un utilisateur.

    Input: id_user, details

    Put: localhost:8000/admin/users/{id_user}, 
    Body:{
    "username": "_username",
    "nom": "_nom",
    "prenom": "_prenom",
    "email": "mail@example.com",
    "password": "_password",
    "role": "coach"
    }
    
    Output: {"message": "Details updated successfully"}"""

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si les détails existent
    cursor.execute("SELECT id_details FROM details WHERE id_user = ?", (id_user,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Details not found")

    # Mettre à jour les détails
    cursor.execute(''' 
        UPDATE details 
        SET gender = ?, age = ?, weight = ?, height = ? 
        WHERE id_user = ? 
    ''', (details.gender, details.age, details.weight, details.height, id_user))

    conn.commit()
    conn.close()
    return {"message": "Details updated successfully"}

@router.delete("/{id_user}")
def delete_details(id_user: int):
    """Supprimer les détails d'un utilisateur.

    Input: id_user

    Delete: localhost:8000/admin/users/{id_user}
    
    Output: {"message": "Details deleted successfully"}"""

    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si les détails existent
    cursor.execute("SELECT id_details FROM details WHERE id_user = ?", (id_user,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Details not found")

    # Supprimer les détails
    cursor.execute("DELETE FROM details WHERE id_user = ?", (id_user,))
    conn.commit()
    conn.close()

    return {"message": "Details deleted successfully"}
