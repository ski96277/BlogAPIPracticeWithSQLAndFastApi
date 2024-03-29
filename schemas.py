from typing import List

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str
    user_id: int

    class Config:
        pass


class BlogShowOnUserId(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    id: int
    blogs: List[BlogShowOnUserId]

    class Config:
        pass


class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUser
