from pydantic import BaseModel
from typing import List, Optional


class StudentBase(BaseModel):
    name: str
    email: str


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True


class GroupBase(BaseModel):
    name: str


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int

    class Config:
        orm_mode = True


class StudentInGroup(BaseModel):
    student_id: int
    group_id: int
