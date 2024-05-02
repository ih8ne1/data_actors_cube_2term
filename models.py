from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, String, Text, func, Integer, Numeric

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Category(Base):
    __tablename__ = 'category'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150))
    birthday: Mapped[str] = mapped_column(DateTime, default=func.now())
    project: Mapped[str] = mapped_column(String(150))
    role: Mapped[str] = mapped_column(String(10))


