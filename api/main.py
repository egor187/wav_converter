import uuid

from fastapi import FastAPI, Depends, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse

from api.schemas import UserIn, UserOut
from api.db import get_db, User, File
from api.converter import save_audio
from sqlalchemy import orm, select

app = FastAPI()


@app.post("/user", response_model=UserOut)
async def create_user(user: UserIn, db_session: orm.Session = Depends(get_db)):
    if db_session.execute(select(User).where(User.name == user.name)).scalar():
        return JSONResponse(
            status_code=400,
            content={"message": "User with provided name already registered"},
        )
    db_user = User(**user.dict())
    db_session.add(db_user)
    db_session.commit()
    return db_user


@app.post("/upload")
async def upload_audio(
    file: UploadFile,
    user_token=Form(),
    user_id=Form(),
    db_session: orm.Session = Depends(get_db),
):
    if not db_session.execute(
        select(User).where(User.token == user_token, User.id == int(user_id))
    ).scalar():
        return JSONResponse(status_code=400, content={"message": "User not registered"})
    file_id = uuid.uuid4()
    path = save_audio(user_id, file, file_id)
    db_session.add(File(user_id=user_id, path=path))
    db_session.commit()
    return FileResponse(path, status_code=201, media_type="application/octet-stream")
