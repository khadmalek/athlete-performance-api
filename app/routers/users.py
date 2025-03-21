from fastapi import APIRouter, HTTPException
from app.database import get_db_connection
from app.schemas.user import UserCreate, UserResponse
from app.utils.security import generate_token, hash_password

router = APIRouter(prefix="/users", tags=["Users"])

# Création d'un utilisateur
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user.

    Args:
        user (UserCreate):

    Raises:
        HTTPException:  User already exists

    Returns:
        UserResponse: User created successfully
    
    Post: localhost:8000/admin/users/, Body:{
    "username": "_username",
    "nom": "_nom",
    "prenom": "_prenom",
    "email": "_email@example.com",
    "password": "_passwo",
    "role": "athlete"
    }
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 🔹 Générer un token avant insertion
        token = generate_token(user.email)

        # 🔹 Insérer l'utilisateur avec son token directement
        cursor.execute(''' 
            INSERT INTO users (username, nom, prenom, email, password, role, token)
            VALUES (?, ?, ?, ?, ?, ?, ?) 
        ''', (user.username, user.nom, user.prenom, user.email, hash_password(user.password), user.role, token))
        
        conn.commit()
        user_id = cursor.lastrowid

    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")

    conn.close()

    return UserResponse(id_user=user_id, **user.dict(exclude={"password"}), token=token)

# Récupérer un utilisateur par son ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Recupérer un utilisateur par son ID.

    Args:
        user_id (int): id de l'utilisateur

    Raises:
        HTTPException: User not found

    Returns:
       UserResponse: User found successfully
    
    Get: localhost:8000/admin/users/1
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_user, username, nom, prenom, email, token, role FROM users WHERE id_user = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**dict(user))

# Mettre à jour un utilisateur
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate):
    """Mis à jour d'un utilisateur.

    Args:
        user_id (int): id de l'utilisateur

    Raises:
        HTTPException: Email already in use
        HTTPException: User not found
        HTTPException: Username already in use

    Returns:
        UserResponse: User updated successfully

    Put: localhost:8000/admin/users/1, 
    Body:
    {
    "username": "_username",
    "nom": "_nom",
    "prenom": "_prenom",
    "email": "mail@example.com",
    "password": "_password",
    "role": "coach"
    }

    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si l'utilisateur existe
    cursor.execute("SELECT id_user FROM users WHERE id_user = ?", (user_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Vérifier si l'email est déjà utilisé par un autre utilisateur
    cursor.execute("SELECT id_user FROM users WHERE email = ? AND id_user != ?", (user.email, user_id))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already in use")

    # Vérifier si le username est déjà utilisé par un autre utilisateur
    cursor.execute("SELECT id_user FROM users WHERE username = ? AND id_user != ?", (user.username, user_id))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already in use")

    # Mettre à jour l'utilisateur sans modifier le token
    cursor.execute(''' 
        UPDATE users
        SET username = ?, nom = ?, prenom = ?, email = ?, password = ?, role = ?
        WHERE id_user = ?
    ''', (user.username, user.nom, user.prenom, user.email, hash_password(user.password), user.role, user_id))

    conn.commit()
    conn.close()

    # Retourner la réponse sans le password
    return UserResponse(id_user=user_id, token="generated_token", **user.dict(exclude={"password"}))

# Supprimer un utilisateur
@router.delete("/{user_id}")
def delete_user(user_id: int):
    """supprimer un utilisateur.

    Args:
        user_id (int): id de l'utilisateur

    Returns:
        "message": "User deleted successfully"
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Vérifier si l'utilisateur existe
    cursor.execute("SELECT * FROM users WHERE id_user = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return {"error": "User not found"}

    # Si l'utilisateur existe, procéder à la suppression
    cursor.execute("DELETE FROM users WHERE id_user = ?", (user_id,))
    conn.commit()
    conn.close()

    return {"message": "User deleted successfully"}

