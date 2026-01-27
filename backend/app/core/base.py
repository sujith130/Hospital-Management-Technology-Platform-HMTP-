from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import Column, String, Integer

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

class HospitalIdMixin:
    """
    Mixin to enforce multi-tenancy by requiring a hospital_id on every record.
    """
    hospital_id = Column(String, index=True, nullable=False)
