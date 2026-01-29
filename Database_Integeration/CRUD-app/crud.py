from sqlalchemy import select
from sqlalchemy.orm import Session
import models, schemas

def get_employees(db: Session):
    stmt = select(models.Employee)
    return db.scalars(stmt).all()

def get_employee(db: Session, emp_id: int):
    stmt = select(models.Employee).where(models.Employee.id == emp_id)
    employee = db.scalar(stmt)
    return employee

def create_employee(db:Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        name = employee.name,
        email = employee.email
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db:Session, emp_id: int, employee: schemas.EmployeeUpdate):
    stmt = select(models.Employee).where(models.Employee.id == emp_id)
    db_employee = db.scalar(stmt)
    if db_employee:
        db_employee.name = employee.name
        db_employee.email = employee.email
        
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db:Session, emp_id: int):
    stmt = select(models.Employee).where(models.Employee.id == emp_id)
    db_employee = db.scalar(stmt)
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
