from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base, SessionLocal

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    tasks = relationship("Task", back_populates="user")

    @property
    def task_count(self):
        return len(self.tasks)

    @classmethod
    def create(cls, **kwargs):
        db = SessionLocal()
        user = cls(**kwargs)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    def delete(cls, user_id):
        db = SessionLocal()
        user = db.query(cls).filter(cls.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

    @classmethod
    def get_all(cls):
        db = SessionLocal()
        return db.query(cls).all()

    @classmethod
    def find_by_id(cls, user_id):
        db = SessionLocal()
        return db.query(cls).filter(cls.id == user_id).first()

    def __repr__(self):
        return f"<User(name={self.name})>"