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
    id_romancista: int


class LivroDB(LivroSchema):
    id: int


class LivroList(BaseModel):
    livros: list[LivroDB]


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaDB(RomancistaSchema):
    id: int


class RomancistaList(BaseModel):
    romancistas: list[RomancistaDB]
