from fastapi import APIRouter, Depends
import schemas
from sqlalchemy.orm import Session
from database import get_db
from repository import user

router = APIRouter(
    tags=['Users']
)


@router.post('/user', response_model=schemas.ShowUser, )
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(db=db, request=request)


@router.get('/user/{user_id}', response_model=schemas.ShowUser, )
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user.show(db=db, user_id=user_id)
