from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "Login réussi"}

@router.post("/register")
def register():
    return {"message": "Utilisateur enregistré avec succès"}