from fastapi import APIRouter, status, Depends, HTTPException
import schemas
from sqlalchemy.orm import Session
from database import get_db
from models import blog_model
from hashing import Hash

router = APIRouter(
    tags=['Users']
)


@router.post('/user', response_model=schemas.ShowUser, )
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = blog_model.User(name=request.name, email=request.email,
                               password=Hash.get_password_hash(password=request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{user_id}', response_model=schemas.ShowUser, )
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(blog_model.User).filter(blog_model.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} is not available")
    return user
