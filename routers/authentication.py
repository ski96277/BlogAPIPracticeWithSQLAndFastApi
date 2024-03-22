from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import database
from hashing import Hash
from models import blog_model
import schemas
from my_token import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.ShowUserDetails)
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(blog_model.User).filter(blog_model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {request.username} is not available")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is invalid")

    access_token = create_access_token(data={"sub": user.email})
    schemas.ShowUserDetails = user
    schemas.ShowUserDetails.token_type = "Bearer"
    schemas.ShowUserDetails.access_token = access_token
    return schemas.ShowUserDetails
