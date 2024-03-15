from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from create_blog_schemas import CreateBlogSchemas
from database import engine, SessionLocal
from models import blog_model

app = FastAPI()

# create sqlite table
blog_model.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Post a blog to datanase
@app.post('/create-blog', status_code=status.HTTP_201_CREATED)
def create_blog(blog_req: CreateBlogSchemas, db: Session = Depends(get_db)):
    new_blog = blog_model.BlogModel(title=blog_req.title, body=blog_req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blogs
@app.get('/blogs', status_code= status.HTTP_200_OK)
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(blog_model.BlogModel).all()
    return blogs


# Get a single blog from the database
@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK)
def get_blog_by_id(blog_id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(blog_model.BlogModel).filter(blog_model.BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} is not available")

    return blog
