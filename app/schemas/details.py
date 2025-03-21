from pydantic import BaseModel

class DetailsCreate(BaseModel):
    """
    Schéma de création des détails d'un utilisateur
    """
    gender: str
    age: int
    weight: float
    height: float

class DetailsResponse(BaseModel):
    """
    Détails d'un utilisateur
    """
    id_details: int
    id_user: int
    gender: str
    age: int
    weight: float
    height: float

    class Config:
        from_attributes = True