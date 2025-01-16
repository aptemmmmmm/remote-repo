from sqlalchemy.orm import Session
from ..models.models import Student, Group
from ..schemas.schemas import StudentCreate

class StudentRepository:
    @staticmethod
    def create_student(db: Session, student: StudentCreate):
        db_student = Student(name=student.name, email=student.email)
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def get_student(db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    @staticmethod
    def get_students(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Student).offset(skip).limit(limit).all()

    @staticmethod
    def delete_student(db: Session, student_id: int):
        student = db.query(Student).filter(Student.id == student_id).first()
        if student:
            db.delete(student)
            db.commit()
            return True
        return False

    @staticmethod
    def add_student_to_group(db: Session, student_id: int, group_id: int):
        student = db.query(Student).filter(Student.id == student_id).first()
        group = db.query(Group).filter(Group.id == group_id).first()
        if student and group:
            student.groups.append(group)
            db.commit()
            return True
        return False

    @staticmethod
    def remove_student_from_group(db: Session, student_id: int, group_id: int):
        student = db.query(Student).filter(Student.id == student_id).first()
        group = db.query(Group).filter(Group.id == group_id).first()
        if student and group and group in student.groups:
            student.groups.remove(group)
            db.commit()
            return True
        return False
