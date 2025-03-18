from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_users():
    return {"message": "Liste des utilisateurs"}

@router.get("/{user_id}")
def get_user(user_id: int):
    return {"message": f"Utilisateur avec l'ID {user_id}"}