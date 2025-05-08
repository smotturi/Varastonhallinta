SET UP FOR CODE

python -m venv venv

venv\Scripts\activate

pip install fastapi uvicorn pydantic sqlalchemy

python -m uvicorn app.main:app --reload
