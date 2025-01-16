from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .database import get_db, engine
from . import models
from .models import models as models_file
from .schemas import schemas
from .repositories.student_repository import StudentRepository
from .repositories.group_repository import GroupRepository

models_file.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/students/", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return StudentRepository.create_student(db, student)

@app.get("/students/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = StudentRepository.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.get("/students/", response_model=List[schemas.Student])
def get_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return StudentRepository.get_students(db, skip, limit)

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not StudentRepository.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}

@app.post("/groups/", response_model=schemas.Group)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    return GroupRepository.create_group(db, group)

@app.get("/groups/{group_id}", response_model=schemas.Group)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = GroupRepository.get_group(db, group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@app.get("/groups/", response_model=List[schemas.Group])
def get_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return GroupRepository.get_groups(db, skip, limit)

@app.delete("/groups/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    if not GroupRepository.delete_group(db, group_id):
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted"}

@app.post("/students/{student_id}/groups/{group_id}")
def add_student_to_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    if not StudentRepository.add_student_to_group(db, student_id, group_id):
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student added to group"}

@app.delete("/students/{student_id}/groups/{group_id}")
def remove_student_from_group(student_id: int, group_id: int, db: Session = Depends(get_db)):
    if not StudentRepository.remove_student_from_group(db, student_id, group_id):
        raise HTTPException(status_code=404, detail="Student or group not found")
    return {"message": "Student removed from group"}

@app.get("/groups/{group_id}/students", response_model=List[schemas.Student])
def get_students_in_group(group_id: int, db: Session = Depends(get_db)):
    students = GroupRepository.get_students_in_group(db, group_id)
    if students is None:
        raise HTTPException(status_code=404, detail="Group not found")
    return students

@app.post("/students/{student_id}/transfer")
def transfer_student(
    student_id: int,
    from_group_id: int,
    to_group_id: int,
    db: Session = Depends(get_db)
):
    if not StudentRepository.remove_student_from_group(db, student_id, from_group_id):
        raise HTTPException(status_code=404, detail="Student not in source group")
    if not StudentRepository.add_student_to_group(db, student_id, to_group_id):
        raise HTTPException(status_code=404, detail="Cannot add student to target group")
    return {"message": "Student transferred successfully"}
