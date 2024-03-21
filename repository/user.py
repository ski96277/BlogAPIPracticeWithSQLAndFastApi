from sqlalchemy.orm import Session
from fastapi import status, HTTPException

import schemas
from models import blog_model

from hashing import Hash


def create(db: Session, request: schemas.User):
    new_user = blog_model.User(name=request.name, email=request.email,
                               password=Hash.get_password_hash(password=request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get(db: Session, user_id: int):
    user = db.query(blog_model.User).filter(blog_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} is not available")
    return user
