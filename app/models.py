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


# @PetBase.mapped
# @dataclass
# class Pet:
#     __tablename__ = "pets"
#     __sa_dataclass_metadata_key__ = "sa"

#     id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
#     user_id: uuid.UUID = field(
#         metadata={"sa": Column(ForeignKey("user_model.id", ondelete="CASCADE"))},
#     )
#     pet_name: str = field(
#         metadata={"sa": Column(String(50), nullable=False)},
#     )
    
class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
    pet_name = Column(String(50), nullable=False)