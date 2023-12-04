from fastapi import FastAPI
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
import pyodbc

import uvicorn
import httpie

'''
uvicorn main:app --reload
http POST http://127.0.0.1:8000/addacc name="кирилл" password="111"
http http://127.0.0.1:8000/acc
http PUT http://127.0.0.1:8000/updacc/2 name="новое_значение" password="новый_пароль"
http DELETE http://127.0.0.1:8000/delpeoples/2
'''

app = FastAPI()

# Подключение к базе данных с помощью SQLAlchemy
server_name = 'WWWEBLO'
database_name = 'people'
table_name = 'Accounts'

SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc:///?odbc_connect=DRIVER={SQL Server};SERVER=' + server_name +';DATABASE=' + database_name +';Trusted_Connection=yes;'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Модель данных для таблицы Peoples
class Accounts(Base):
    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(50))

# GET запрос - получение всех записей
@app.get('/acc')
def get_peoples():
    db = SessionLocal()
    peoples = db.query(Accounts).all()
    return {'accounts': [{'id': person.id, 'name': person.name, 'password': person.password} for person in peoples]}

# POST запрос - добавление новой записи
@app.post('/addacc')
def add_peoples(data: dict):
    db = SessionLocal()
    new_people = Accounts(name=data['name'], password=data['password'])
    db.add(new_people)
    db.commit()
    return {'message': 'Account added successfully'}

# PUT запрос - обновление записи
@app.put('/updacc/{id}')
def update_people(id: int, data: dict):
    db = SessionLocal()
    person = db.query(Accounts).filter(Accounts.id == id).first()
    if person:
        person.name = data['name']
        person.password = data['password']
        db.commit()
        return {'message': 'Account updated successfully'}
    return {'message': 'Account not found'}

# DELETE запрос - удаление записи
@app.delete('/delpeoples/{id}')
def delete_people(id: int):
    db = SessionLocal()
    deleted = db.query(Accounts).filter(Accounts.id == id).delete()
    db.commit()
    if deleted:
        return {'message': 'Accounts deleted successfully'}
    return {'message': 'Account not found'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)