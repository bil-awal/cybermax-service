"""
app/repositories/base.py - Base repository with common CRUD operations
"""
from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel

from app.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base repository class with common CRUD operations"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        try:
            return db.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        try:
            return db.query(self.model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = obj_in.dict()
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def update(self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        try:
            obj_data = obj_in.dict(exclude_unset=True)
            for field, value in obj_data.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def delete(self, db: Session, *, id: Any) -> Optional[ModelType]:
        try:
            obj = db.query(self.model).get(id)
            if obj:
                db.delete(obj)
                db.commit()
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    def count(self, db: Session) -> int:
        try:
            return db.query(self.model).count()
        except SQLAlchemyError as e:
            db.rollback()
            raise e
