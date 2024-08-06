from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDB(UserSchema):
    id: int


class UserPublic(BaseModel):
    id: int
    username: str
    email: str


class UserList(BaseModel):
    users: list[UserPublic]


class LivroSchema(BaseModel):
    ano: str
    titulo: str
    romancista_id: str


class RomancistaSchema(BaseModel):
    nome: str
    livros: str
