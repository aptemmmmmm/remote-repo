from sqlalchemy.orm import Session
from ..models.models import Group
from ..schemas.schemas import GroupCreate

class GroupRepository:
    @staticmethod
    def create_group(db: Session, group: GroupCreate):
        db_group = Group(name=group.name)
        db.add(db_group)
        db.commit()
        db.refresh(db_group)
        return db_group

    @staticmethod
    def get_group(db: Session, group_id: int):
        return db.query(Group).filter(Group.id == group_id).first()

    @staticmethod
    def get_groups(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Group).offset(skip).limit(limit).all()

    @staticmethod
    def delete_group(db: Session, group_id: int):
        group = db.query(Group).filter(Group.id == group_id).first()
        if group:
            db.delete(group)
            db.commit()
            return True
        return False

    @staticmethod
    def get_students_in_group(db: Session, group_id: int):
        group = db.query(Group).filter(Group.id == group_id).first()
        if group:
            return group.students
        return []
