from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_performances():
    return {"message": "Liste des performances"}

@router.get("/{performance_id}")
def get_performance(performance_id: int):
    return {"message": f"Performance avec l'ID {performance_id}"}
