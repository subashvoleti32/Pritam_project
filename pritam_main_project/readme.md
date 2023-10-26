Step1:- Virtual Environment setup
python -m venv venv

step2:- venv\Scripts\activate

step3:- install required packages
1) pip install fastapi,pydantic,fastapi-sqlalchemy

step4:- running application

uvicorn main:app --reload 

step5:- fastapi swagger docs

localhost:8000/docs

