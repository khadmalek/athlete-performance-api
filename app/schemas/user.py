from pydantic import BaseModel
from typing import Optional

# Schéma pour la création d'un utilisateur
class UserCreate(BaseModel):
    """
    Schéma de création d'un utilisateur
    """
    username: str
    nom: str
    prenom: str
    email: str
    password: str
    role: str  # 'coach' ou 'athlete'

    class Config:
        orm_mode = True

# Schéma pour la réponse d'un utilisateur (sans mot de passe)
class UserResponse(BaseModel):
    """
    Schéma pour la réponse d'un utilisateur
    """
    id_user: int
    username: str
    nom: str
    prenom: str
    email: str
    token: Optional[str] = None  # Champ optionnel
    role: str  # 'coach' ou 'athlete'

    class Config:
        from_attributes = True
