"""
SQL Alchemy models declaration.

Note, imported by alembic migrations logic, see `alembic/env.py`
"""

from typing import Any, cast

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm.decl_api import declarative_base

import uuid
from dataclasses import dataclass, field
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import registry, relationship
PetBase = registry()

Base = cast(Any, declarative_base())


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass

   
class Pet(Base):
    __tablename__ = "pets"
    
    def __init__(self, user_id, pet_name) -> None:
        super().__init__()
        self.user_id = user_id
        self.pet_name = pet_name
        
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    pet_name = Column(String(50), nullable=False)
