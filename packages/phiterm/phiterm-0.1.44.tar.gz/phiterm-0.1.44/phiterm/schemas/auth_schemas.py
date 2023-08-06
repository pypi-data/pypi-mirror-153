from pydantic import BaseModel


class EmailPasswordSignInSchema(BaseModel):
    email: str
    password: str
    auth_source: str = "CLI"
