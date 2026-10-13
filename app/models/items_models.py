from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, Text
from app.database.db_connection import Base

class ItemModel(Base):
    __tablename__ = "tb_items"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True, index=True)

    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)

    description: Mapped[str | None] = mapped_column(String(60), nullable=True)

    family: Mapped[str] = mapped_column(String(20), nullable=False, unique=False)

    price: Mapped[float] = mapped_column(Float, nullable=False)

    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)