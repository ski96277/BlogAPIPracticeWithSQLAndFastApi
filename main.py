from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

import schemas
from database import engine, SessionLocal
from hashing import Hash
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
@app.post('/blogs/create-blog', status_code=status.HTTP_201_CREATED)
def create_blog(blog_req: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = blog_model.BlogModel(title=blog_req.title, body=blog_req.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# Get all blogs
@app.get('/blogs/all', status_code=status.HTTP_200_OK)
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(blog_model.BlogModel).all()
    return blogs


# Get a single blog from the database
@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def get_blog_by_id(blog_id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(blog_model.BlogModel).filter(blog_model.BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} is not available")

    return blog


# Delete a blog by id
@app.delete('/blog/delete/{blog_id}')
def delete_a_blog(blog_id, response: Response, db: Session = Depends(get_db)):
    is_deleted_blog = db.query(blog_model.BlogModel).filter(blog_model.BlogModel.id == blog_id).delete(
        synchronize_session=False)
    db.commit()

    # id deleted blog 1 mean delete the blog 0 mean is not delete blog
    if is_deleted_blog != 1:
        print("blog is not found ")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog is not deleted due to the blog {blog_id} not found or others issues")

    else:
        return {'response': f"Deleted the blog id {blog_id}"}


@app.put('/blog/update/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id, response: Response, request: schemas.Blog, db: Session = Depends(get_db)):
    blog_update = db.query(blog_model.BlogModel).filter(blog_model.BlogModel.id == blog_id).update(
        {"title": request.title, "body": request.body})
    db.commit()
    print(f"Blog updates {blog_update}")
    if blog_update != 1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog is not updated {blog_id}")
    else:
        return {"response": f"Updated blog {blog_id}", 'status_code': status.HTTP_202_ACCEPTED}


@app.post('/user',response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = blog_model.User(name=request.name, email=request.email,
                               password=Hash.get_password_hash(password=request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
