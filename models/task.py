from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base, SessionLocal
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    deadline = Column(DateTime)
    importance = Column(Integer)
    estimated_time = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")

    @property
    def is_past_due(self):
        return datetime.now() > self.deadline

    @classmethod
    def create(cls, **kwargs):
        db = SessionLocal()
        task = cls(**kwargs)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @classmethod
    def delete(cls, task_id):
        db = SessionLocal()
        task = db.query(cls).filter(cls.id == task_id).first()
        if task:
            db.delete(task)
            db.commit()
            return True
        return False

    @classmethod
    def get_all(cls):
        db = SessionLocal()
        return db.query(cls).all()

    @classmethod
    def find_by_id(cls, task_id):
        db = SessionLocal()
        return db.query(cls).filter(cls.id == task_id).first()

    def __repr__(self):
        return f"<Task(title={self.title}, deadline={self.deadline})>"