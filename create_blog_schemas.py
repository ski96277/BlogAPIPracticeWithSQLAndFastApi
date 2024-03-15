from pydantic import BaseModel


class CreateBlogSchemas(BaseModel):
    title: str
    body: str
