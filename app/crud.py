from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas

# Sisältää kaikki tietokantaoperaatiot

# Hyllypaikka CRUD operaatiot

def get_hyllypaikka(db: Session, hyllypaikka_id: str):
    return db.query(models.Hyllypaikka).filter(models.Hyllypaikka.id == hyllypaikka_id).first()


def get_hyllypaikat(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Hyllypaikka).offset(skip).limit(limit).all()


def create_hyllypaikka(db: Session, hyllypaikka: schemas.HyllypaikkaCreate):
    db_hyllypaikka = models.Hyllypaikka(**hyllypaikka.model_dump())
    db.add(db_hyllypaikka)
    db.commit()
    db.refresh(db_hyllypaikka)
    return db_hyllypaikka


def update_hyllypaikka(db: Session, hyllypaikka_id: str, hyllypaikka: schemas.HyllypaikkaMuokkaa):
    db_hyllypaikka = get_hyllypaikka(db, hyllypaikka_id)
    if db_hyllypaikka:
        update_data = hyllypaikka.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_hyllypaikka, key, value)
        db.commit()
        db.refresh(db_hyllypaikka)
    return db_hyllypaikka


def delete_hyllypaikka(db: Session, hyllypaikka_id: str):
    db_hyllypaikka = get_hyllypaikka(db, hyllypaikka_id)
    if db_hyllypaikka:
        db.delete(db_hyllypaikka)
        db.commit()
    return db_hyllypaikka


# Tuote CRUD operaatiot

def get_tuote(db: Session, tuote_id: str):
    return db.query(models.Tuote).filter(models.Tuote.id == tuote_id).first()


def search_tuotteet(db: Session, search_term: str, skip: int = 0, limit: int = 100):
    """Haku tuotteiden nimestä tai koodista"""
    return db.query(models.Tuote).filter(
        or_(
            models.Tuote.id.ilike(f"%{search_term}%"),
            models.Tuote.nimi.ilike(f"%{search_term}%")
        )
    ).offset(skip).limit(limit).all()


def get_tuotteet(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tuote).offset(skip).limit(limit).all()


def get_tuotteet_by_hyllypaikka(db: Session, hyllypaikka_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Tuote).filter(models.Tuote.hyllypaikka_id == hyllypaikka_id).offset(skip).limit(limit).all()


def create_tuote(db: Session, tuote: schemas.TuoteCreate):
    # Tarkistetaan onko id jo olemassa
    existing_tuote = db.query(models.Tuote).filter(models.Tuote.id == tuote.id).first()
    if existing_tuote:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tuote ID '{tuote.id}' on jo olemassa."
        )
    db_tuote = models.Tuote(**tuote.model_dump())
    db.add(db_tuote)
    db.commit()
    db.refresh(db_tuote)
    return db_tuote


def update_tuote(db: Session, tuote_id: str, tuote: schemas.TuoteMuokkaa):
    db_tuote = get_tuote(db, tuote_id)
    if db_tuote:
        update_data = tuote.model_dump(exclude_unset=True)
        
        if "nimi" in update_data and update_data["nimi"] == "":
            update_data.pop("nimi")
            
        
            
        for key, value in update_data.items():
            setattr(db_tuote, key, value)
        db.commit()
        db.refresh(db_tuote)
    return db_tuote




def delete_tuote(db: Session, tuote_id: str):
    db_tuote = get_tuote(db, tuote_id)
    if db_tuote:
        db.delete(db_tuote)
        db.commit()
    return db_tuote