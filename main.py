import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import schemas as _schemas
import services as _services
import uvicorn as _uvicorn
app = _fastapi.FastAPI()


@app.post("/api/v1/users")
async def register_user(user: _schemas.UserReq, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.grtUserByEmail(email=user.email, db=db)
    if db_user:
        raise _fastapi.HTTPException(
            400, 'this email Already exist , try another Email')
    db_user = await _services.create_user(user=user, db=db)
    return await _services.create_token(user=db_user)
