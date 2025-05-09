*SET UP FOR CODE *

*download dependencies with venv*

python -m venv venv

venv\Scripts\activate

pip install fastapi uvicorn pydantic sqlalchemy

python -m uvicorn app.main:app --reload

*AFTER SET UP*

*go to localhost address shown in cmd*

*Type in after local host address/docs to test app*

*EXITING*

*When you want to stop, type in cmd*

deactivate

*To exit from venv mode*
