from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import models
from app.database import engine
from app.routes import hyllypaikat, tuotteet

# Luo tietokantataulut SQLAlchemyn avulla
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS-asetukset, sallitaan pyynnöt kaikista lähteistä kehitysympäristössä
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Kehitysympäristössä sallitaan kaikki lähteet
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Liitetään reitit sovellukseen
app.include_router(hyllypaikat.router)
app.include_router(tuotteet.router)


@app.get("/", tags=["info"])
def read_root():
    return {
        "sovellus": "Varastonhallintajärjestelmä",
        "versio": "0.1.0",
        "dokumentaatio": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)