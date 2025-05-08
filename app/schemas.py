from pydantic import BaseModel, Field
from typing import List, Optional

from datetime import datetime




# Hyllypaikka schemas

class HyllypaikkaBase(BaseModel):
    id: str
    nimi: str
    
    class Config:
        from_attributes = True


class HyllypaikkaCreate(HyllypaikkaBase):
    pass


class HyllypaikkaMuokkaa(BaseModel):
    nimi: Optional[str] = None
    



class HyllypaikkaWithTuotteet(HyllypaikkaBase):
    tuotteet: List["Tuote"] = []

    class Config:
        from_attributes = True


# Tuote schemas


class TuoteBase(BaseModel):
    id: str
    nimi: str
    quantity: int = Field(gt=0)  # varmistetaan että määrä on positiivinen
    


class TuoteCreate(TuoteBase):
    hyllypaikka_id: str


class TuoteMuokkaa(BaseModel):
    nimi: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    hyllypaikka_id: Optional[str] = None
    
    class Config:
        from_attributes = True


class Tuote(TuoteBase):
    id: str
    #hyllypaikka_id: str
    #luotu: datetime

    class Config:
        from_attributes = True


class TuoteWithHyllypaikka(TuoteBase):
    hyllypaikka: HyllypaikkaBase
    class Config:
        from_attributes = True


# Viittaus eteenpäin, koska luokat viittaavat toisiinsa
HyllypaikkaWithTuotteet.model_rebuild()