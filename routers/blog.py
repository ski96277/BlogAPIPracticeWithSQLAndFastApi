from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
import schemas

from database import get_db

from models import blog_model
from repository import blog

router = APIRouter(
    tags=['Blogs']
)


# Get all blogs
@router.get('/blogs/all', status_code=status.HTTP_200_OK, )
def get_all_blogs(db: Session = Depends(get_db)):
    return blog.get_all(db=db)


@router.post('/blogs/create-blog', status_code=status.HTTP_201_CREATED, )
def create_blog(blog_req: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create(db=db, blog_req=blog_req)


# Get a single blog from the database
@router.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, )
def get_blog_by_id(blog_id, db: Session = Depends(get_db)):
    return blog.get_blog(db=db, blog_id=blog_id)


# Delete a blog by id
@router.delete('/blog/delete/{blog_id}', )
def delete_a_blog(blog_id, db: Session = Depends(get_db)):
    return blog.delete(db=db, blog_id=blog_id)


@router.put('/blog/update/{blog_id}', status_code=status.HTTP_202_ACCEPTED, )
def update_blog(blog_id, response: Response, request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.update(db=db, request=request, response=response, blog_id=blog_id)
