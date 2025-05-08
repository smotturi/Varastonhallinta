from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/hyllypaikat",
    tags=["hyllypaikat"],
    responses={404: {"description": "Hyllypaikkaa ei löydy"}}
)


@router.post("/", response_model=schemas.HyllypaikkaBase, status_code=status.HTTP_201_CREATED)
def create_hyllypaikka(hyllypaikka: schemas.HyllypaikkaCreate, db: Session = Depends(get_db)):
    db_hyllypaikka = crud.get_hyllypaikka(db, id=hyllypaikka.id)
    if db_hyllypaikka:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Hyllypaikka koodilla {hyllypaikka.id} on jo olemassa"
        )
    return crud.create_hyllypaikka(db=db, hyllypaikka=hyllypaikka)


@router.get("/", response_model=List[schemas.HyllypaikkaBase])
def read_hyllypaikat(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hyllypaikat = crud.get_hyllypaikat(db, skip=skip, limit=limit)
    return hyllypaikat


@router.get("/{hyllypaikka_id}", response_model=schemas.HyllypaikkaWithTuotteet)
def read_hyllypaikka(hyllypaikka_id: str, db: Session = Depends(get_db)):
    db_hyllypaikka = crud.get_hyllypaikka(db, hyllypaikka_id)
    if db_hyllypaikka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hyllypaikkaa id:llä {hyllypaikka_id} ei löydy"
        )
    return db_hyllypaikka


@router.put("/{hyllypaikka_id}", response_model=schemas.HyllypaikkaBase)
def update_hyllypaikka(
    hyllypaikka_id: str, 
    hyllypaikka: schemas.HyllypaikkaMuokkaa, 
    db: Session = Depends(get_db)
):
    db_hyllypaikka = crud.get_hyllypaikka(db, hyllypaikka_id=hyllypaikka_id)
    if db_hyllypaikka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hyllypaikkaa id:llä {hyllypaikka_id} ei löydy"
        )
    return crud.update_hyllypaikka(db=db, hyllypaikka_id=hyllypaikka_id, hyllypaikka=hyllypaikka)


@router.delete("/{hyllypaikka_id}", response_model=schemas.HyllypaikkaBase)
def delete_hyllypaikka(hyllypaikka_id: str, db: Session = Depends(get_db)):
    db_hyllypaikka = crud.get_hyllypaikka(db, hyllypaikka_id=hyllypaikka_id)
    if db_hyllypaikka is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hyllypaikkaa id:llä {hyllypaikka_id} ei löydy"
        )
    return crud.delete_hyllypaikka(db=db, hyllypaikka_id=hyllypaikka_id)