from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    password = Column(String, nullable=False)
    super_user = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

    entries = relationship("Entry", back_populates="owner")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float)
    description = Column(String)
    supplier = Column(String, nullable=True)
    interval = Column(String)
    entry_date = Column(Date, nullable=True)
    url = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id"), nullable=True)

    owner = relationship("User", back_populates="entries")


class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True, index=True)
    nr = Column(Integer, unique=True)
    start_date = Column(Date)
    end_date = Column(Date)

    entries: Mapped[list[Entry]] = relationship()


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    entry_date = Column(Date, nullable=True)
    owner_id = Column(Integer, nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("periods.id"), nullable=True)
