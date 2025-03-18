from fastapi import FastAPI
from app.routers import auth, details, users, performances
from app.database import create_tables

app = FastAPI(title="Athlete Performance API")

# Inclusion des routers
app.include_router(auth.router, prefix="/auth", tags=["Authentification"])
app.include_router(users.router, prefix="/admin", tags=["Utilisateurs"])
app.include_router(performances.router, prefix="/performance", tags=["Performances"])
app.include_router(details.router, prefix="/admin", tags=["Details"])

#creation de la base de données

create_tables()

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de gestion des performances des athlètes."}