from pydantic import BaseModel

class DetailsCreate(BaseModel):
    gender: str
    age: int
    weight: float
    height: float

class DetailsResponse(BaseModel):
    id_details: int
    id_user: int
    gender: str
    age: int
    weight: float
    height: float

    class Config:
        from_attributes = True