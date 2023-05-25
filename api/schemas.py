from pydantic import BaseModel, UUID4


class UserIn(BaseModel):
    name: str


class UserOut(BaseModel):
    id: int
    token: UUID4

    class Config:
        orm_mode = True


class UploadAudioUserIn(UserOut):
    pass
