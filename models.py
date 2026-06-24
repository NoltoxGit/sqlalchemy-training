from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from database import Base


class Liste_Telephones(Base):
    __tablename__ = "telephones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    marque: Mapped[str] = mapped_column(String(50), nullable=False)
    modele: Mapped[str] = mapped_column(String(100), nullable=False)
    espace_stockage: Mapped[int] = mapped_column(Integer, nullable=False)
    memoire_ram: Mapped[int] = mapped_column(Integer, nullable=False)
    prix: Mapped[int] = mapped_column(Integer, nullable=False)