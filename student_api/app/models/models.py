from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

# Таблица связи многие-ко-многим между студентами и группами
student_group = Table(
    'student_group',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    groups = relationship("Group", secondary=student_group, back_populates="students")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    students = relationship("Student", secondary=student_group, back_populates="groups")
