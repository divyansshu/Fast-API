import models, crud, schemas
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import  Session
from database import engine, sessionLocal
from typing import List
from models import Base


# create all tables
# This creates your tables using the SQLAlchemy 2.0 Declarative Base.
Base.metadata.create_all(bind = engine)

app = FastAPI()

# dependency -> DB session
# This gives each request its own DB session, closes it after use:
def get_db():
    db = sessionLocal()
    try:
        # yield db → FastAPI injects it into endpoints
        yield db
    finally:
        # finally: db.close() → cleans up
        db.close()

# end points
# 1: create an employee
@app.post('/employees', response_model=schemas.EmployeeOut)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, employee)

# 2: get all employees
@app.get('/employees', response_model = List[schemas.EmployeeOut])
def get_employees(db:Session = Depends(get_db)):
    return crud.get_employees(db)

# 3: get specific employee
@app.get('/employee/{emp_id}', response_model = schemas.EmployeeOut)
def get_employee(emp_id: int, db:Session = Depends(get_db)):
    employee = crud.get_employee(db, emp_id)
    if employee:
        return employee
    raise HTTPException(status_code=404, detail='Employee Not Found')

# 4: update employee
@app.put('/employees/{emp_id}', response_model = schemas.EmployeeOut)
def update_employee(emp_id: int, employee: schemas.EmployeeUpdate, db:Session = Depends(get_db)):
    db_employee = crud.update_employee(db, emp_id, employee)
    if db_employee:
        return db_employee
    raise HTTPException(status_code=404, detail="Employee Not Found")

# 5: delete employee
@app.delete('/employees/{emp_id}', response_model=dict)
def delete_employee(emp_id: int, db:Session = Depends(get_db)):
    db_employee = crud.delete_employee(db, emp_id)
    if db_employee:
        return {'detail': 'Employee Deleted Successfully'}
    raise HTTPException(status_code = 404, detail='Employee Not Found')