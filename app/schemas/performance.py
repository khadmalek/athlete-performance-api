from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PerformanceBase(BaseModel):
    """
    Modèle de la performance d'un utilisateur
    """
    power_max: Optional[float] = None
    hr_max: Optional[float] = None
    vo2_max: Optional[float] = None
    rf_max: Optional[float] = None
    cadence_max: Optional[float] = None
    vo2_class: Optional[str] = None
    ressenti: Optional[int] = None

class PerformanceCreate(PerformanceBase):
    pass  # Pas d'id ni de date à fournir lors de la création

class PerformanceResponse(PerformanceBase):
    """
    Réponse de Performance d'un utilisateur
    """
    id_performance: int
    id_user: int
    date_performance: datetime

    class Config:
        from_attributes = True