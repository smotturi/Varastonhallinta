from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas, crud
from app.database import get_db

# API-reitit tuotteiden käsittelyyn:

router = APIRouter(
    prefix="/tuotteet",
    tags=["tuotteet"],
    responses={404: {"description": "Tuotetta ei löydy"}}
)


@router.post("/", response_model=schemas.Tuote, status_code=status.HTTP_201_CREATED)
def create_tuote(tuote: schemas.TuoteCreate, db: Session = Depends(get_db)):
    # Tarkistetaan että hyllypaikka on olemassa
    db_hyllypaikka = crud.get_hyllypaikka(db, hyllypaikka_id=tuote.hyllypaikka_id)
    if not db_hyllypaikka:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hyllypaikkaa id:llä {tuote.hyllypaikka_id} ei löydy"
        )
    return crud.create_tuote(db=db, tuote=tuote)


@router.get("/", response_model=List[schemas.TuoteWithHyllypaikka])
def read_tuotteet(
    skip: int = 0, 
    limit: int = 100, 
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if search:
        tuotteet = crud.search_tuotteet(db, search_term=search, skip=skip, limit=limit)
    else:
        tuotteet = crud.get_tuotteet(db, skip=skip, limit=limit)
    return tuotteet


@router.get("/{tuote_id}", response_model=schemas.TuoteWithHyllypaikka)
def read_tuote(tuote_id: str, db: Session = Depends(get_db)):
    db_tuote = crud.get_tuote(db, tuote_id=tuote_id)
    if db_tuote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tuotetta id:llä {tuote_id} ei löydy"
        )
    return db_tuote


@router.get("/hyllypaikka/{hyllypaikka_id}", response_model=List[schemas.Tuote])
def read_tuotteet_by_hyllypaikka(
    hyllypaikka_id: str, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    # Tarkistetaan että hyllypaikka on olemassa
    db_hyllypaikka = crud.get_hyllypaikka(db, hyllypaikka_id=hyllypaikka_id)
    if not db_hyllypaikka:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hyllypaikkaa id:llä {hyllypaikka_id} ei löydy"
        )
    return crud.get_tuotteet_by_hyllypaikka(
        db, hyllypaikka_id=hyllypaikka_id, skip=skip, limit=limit
    )


@router.put("/{tuote_id}", response_model=schemas.Tuote)
def update_tuote(tuote_id: str, tuote: schemas.TuoteMuokkaa, db: Session = Depends(get_db)):
    db_tuote = crud.get_tuote(db, tuote_id=tuote_id)
    if db_tuote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tuotetta id:llä {tuote_id} ei löydy"
        )
    
    # Jos hyllypaikkaa muokataan, tarkista että se on olemassa
    if tuote.hyllypaikka_id is not None:
        db_hyllypaikka = crud.get_hyllypaikka(db, hyllypaikka_id=tuote.hyllypaikka_id)
        if not db_hyllypaikka:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Hyllypaikkaa id:llä {tuote.hyllypaikka_id} ei löydy"
            )
    
    return crud.update_tuote(db=db, tuote_id=tuote_id, tuote=tuote)

@router.delete("/{tuote_id}", response_model=schemas.Tuote)
def delete_tuote(tuote_id: str, db: Session = Depends(get_db)):
    db_tuote = crud.get_tuote(db, tuote_id=tuote_id)
    if db_tuote is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tuotetta id:llä {tuote_id} ei löydy"
        )
    return crud.delete_tuote(db=db, tuote_id=tuote_id)
