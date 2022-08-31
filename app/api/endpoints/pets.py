from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Pet, UserTable
from app.schemas.requests import PetCreateRequest
from app.schemas.responses import PetResponse
from typing import List

router = APIRouter()


@router.post("/create", response_model=PetResponse, status_code=201)
async def create_new_pet(
    new_pet: PetCreateRequest,
    session: AsyncSession = Depends(deps.get_session),
    current_user: UserTable = Depends(deps.get_current_user),
):
    """Creates new pet. Only for logged users."""

    pet = Pet(user_id=current_user.id, pet_name=new_pet.pet_name)

    session.add(pet)
    await session.commit()
    return pet


@router.get("/me", response_model=List[PetResponse], status_code=200)
async def get_all_my_pets(
    session: AsyncSession = Depends(deps.get_session),
    current_user: UserTable = Depends(deps.get_current_user),
):
    """Get list of pets for currently logged user."""

    pets = await session.execute(
        select(Pet)
        .where(
            Pet.user_id == current_user.id,
        )
        .order_by(Pet.pet_name)
    )
    return pets.scalars().all()
