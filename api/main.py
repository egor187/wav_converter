from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse

from schemas import UserIn, UserOut
from db import get_db, User
from sqlalchemy import orm, select

app = FastAPI()


@app.post('/user', response_model=UserOut)
async def create_user(user: UserIn, db_session: orm.Session = Depends(get_db)):
    if db_session.execute(select(User).where(User.name == user.name)).scalar():
        return JSONResponse(
            status_code=400, content={"message": "User with provided name already registered"}
        )
    db_user = User(**user.dict())
    db_session.add(db_user)
    db_session.commit()
    return db_user
