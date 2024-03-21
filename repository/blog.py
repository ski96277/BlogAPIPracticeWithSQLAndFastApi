from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from models import blog_model
import schemas


def get_all(db: Session):
    blogs = db.query(blog_model.BlogModel).all()
    return blogs


def create(db: Session, blog_req: schemas.Blog):
    new_blog = blog_model.BlogModel(title=blog_req.title, body=blog_req.body, user_id=blog_req.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get_blog(db: Session, blog_id):
    blog = db.query(blog_model.BlogModel).filter(blog_model.BlogModel.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {blog_id} is not available")

    return blog


def delete(db: Session, blog_id):
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


def update(db: Session, request: schemas.Blog, response: Response, blog_id):
    blog_update = db.query(blog_model.BlogModel).filter(blog_model.BlogModel.id == blog_id).update(
        {"title": request.title, "body": request.body})
    db.commit()
    print(f"Blog updates {blog_update}")
    if blog_update != 1:
        response.status_code = status.HTTP_404_NOT_FOUND
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog is not updated {blog_id}")
    else:
        return {"response": f"Updated blog {blog_id}", 'status_code': status.HTTP_202_ACCEPTED}
