# /app/tests/test_pets.py

import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models import Pet, UserTable
from fastapi_users.password import get_password_hash

from app.tests import utils

# All test coroutines in file will be treated as marked (async allowed).
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def default_user_pets(session: AsyncSession):
    return await utils.create_db_user(f"{uuid.uuid4().hex}@gmail.com", get_password_hash("password"), session)


async def test_create_new_pet(
    client: AsyncClient, default_user_headers, default_user_pets: UserTable
):
    access_token_res = await client.post(
        "/auth/jwt/login",
        data={
            "username": default_user_pets.email,
            "password": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert access_token_res.status_code == 200
    token = access_token_res.json()
    access_token = token["access_token"]
    
    # ----
    response = await client.post(
        app.url_path_for("create_new_pet"),
        headers={"Authorization": f"Bearer {access_token}"},
        json={"pet_name": "Tadeusz"},
    )
    assert response.status_code == 201
    result = response.json()
    assert result["user_id"] == str(default_user_pets.id)
    assert result["pet_name"] == "Tadeusz"


async def test_get_all_my_pets(
    client: AsyncClient, default_user_headers, default_user_pets: UserTable, session: AsyncSession
):
    access_token_res = await client.post(
        "/auth/jwt/login",
        data={
            "username": default_user_pets.email,
            "password": "password",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert access_token_res.status_code == 200
    token = access_token_res.json()
    access_token = token["access_token"]
    
    #--------------------------------

    pet1 = Pet(default_user_pets.id, "Pet_1")
    pet2 = Pet(default_user_pets.id, "Pet_2")
    session.add(pet1)
    session.add(pet2)
    await session.commit()

    response = await client.get(
        app.url_path_for("get_all_my_pets"),
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200

    assert response.json() == [
        {
            "user_id": str(pet1.user_id),
            "pet_name": pet1.pet_name,
            "id": pet1.id,
        },
        {
            "user_id": str(pet2.user_id),
            "pet_name": pet2.pet_name,
            "id": pet2.id,
        },
    ]
