# Modern SQLALchemy uses DeclarativeBase and type hints (Mapped)
# to define table schemas and python classes simultaneously

from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Employee(Base):
    # mapped_column automatically infers SQL types from Python types
    __tablename__ = 'employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    
    