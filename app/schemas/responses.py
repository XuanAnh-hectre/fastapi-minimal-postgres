import uuid

from app.schemas import BaseRequestResponse

class PetResponse(BaseRequestResponse):
    id: int
    pet_name: str
    user_id: uuid.UUID
    