from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
from hashing import Hash
from models import blog_model
import schemas

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.ShowUser)
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(blog_model.User).filter(blog_model.User.email == request.username).first()
    print(f"user is {user}")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {request.username} is not available")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is invalid")
    return user
