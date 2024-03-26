from fastapi import FastAPI

from database import engine

from models import blog_model
from routers import blog, user

app = FastAPI()

# create sqlite table
blog_model.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)

