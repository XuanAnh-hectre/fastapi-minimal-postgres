

from app.schemas import BaseRequestResponse


class PetCreateRequest(BaseRequestResponse):
    pet_name: str