from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class LivroSchema(BaseModel):
    ano: str
    titulo: str
    id_romancista: int


class LivroDB(LivroSchema):
    id: int
    ano: str
    titulo: str
    id_romancista: int
    model_config = ConfigDict(from_attributes=True)


class LivroList(BaseModel):
    livros: list[LivroDB]


class RomancistaSchema(BaseModel):
    nome: str


class RomancistaDB(RomancistaSchema):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class RomancistaList(BaseModel):
    romancistas: list[RomancistaDB]
