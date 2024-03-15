from fastapi import FastAPI, Depends
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


@app.post('/create-blog')
def create_blog(blog_req: CreateBlogSchemas, db: Session = Depends(get_db)):
    new_blog = blog_model.BlogModel(title=blog_req.title, body=blog_req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
