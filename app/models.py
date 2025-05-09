from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
import sqlalchemy.sql.functions as func

from app.database import Base

    # Määrittelee tietokantataulut SQLAlchemyn avulla

class Hyllypaikka(Base):
    __tablename__ = "hyllypaikat"

    id = Column(String, primary_key=True, index=True)
    nimi = Column(String, unique=True, index=True)  
    


    # Relaatio tuotteisiin

    tuotteet = relationship("Tuote", back_populates="hyllypaikka", cascade="all, delete-orphan")
    


class Tuote(Base):
    __tablename__ = "tuotteet"

    id = Column(String, primary_key=True, index=True)
    nimi = Column(String, index=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    hyllypaikka_id = Column(String, ForeignKey("hyllypaikat.id"), nullable=False)
    luotu = Column(DateTime(timezone=True), server_default=func.now())
    

    # Relaatio hyllypaikkaan
    hyllypaikka = relationship("Hyllypaikka", back_populates="tuotteet")