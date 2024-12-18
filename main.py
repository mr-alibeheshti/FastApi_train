import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
from typing import List
import schemas as _schemas
import services as _services
import uvicorn as _uvicorn
import models as _models
app = _fastapi.FastAPI()


@app.post("/api/v1/user/register")
async def register_user(user: _schemas.UserReq, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.getUserByEmail(email=user.email, db=db)
    if db_user:
        raise _fastapi.HTTPException(
            400, 'This Email Already Exist , Try Another Email')
    db_user = await _services.create_user(user=user, db=db)
    return await _services.create_token(user=db_user)


@app.post("/api/v1/user/login")
async def login_user(form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.login(email=form_data.username, password=form_data.password, db=db)
    if db_user:
        token = await _services.create_token(db_user)
    return token


@app.get("/api/v1/user/info", response_model=_schemas.UserRep)
async def get_user_info(user: _schemas.UserRep = _fastapi.Depends(_services.current_user)):
    return user


@app.get("/api/v1/user/{user_id}", response_model=_schemas.UserRep)
async def get_user_data(user_id: int, db: _orm.session = _fastapi.Depends(_services.get_db)):
    return await _services.get_user_details(user_id=user_id, db=db)


@app.post("/api/v1/post/create", response_model=_schemas.PostRes)
async def create_post(post_req: _schemas.PostReq, user: _schemas.UserReq = _fastapi.Depends(_services.current_user),
                      db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_post(user=user, db=db, post=post_req)


@app.get("/api/v1/post/post_per_user", response_model=list[_schemas.PostRes])
async def get_posts_by_user(user: _schemas.UserReq = _fastapi.Depends(_services.current_user),
                            db: _orm.session = _fastapi.Depends(
                                _services.get_db)
                            ):
    return await _services.get_posts_by_user(user=user, db=db)


@app.get("/api/v1/post/all")
async def get_all_posts(db: _orm.session = _fastapi.Depends(_services.get_db)
                        ):
    return await _services.get_all_posts(db=db)


@app.get("/api/v1/post/{post_id}", response_model=_schemas.PostRes)
async def get_post_detail(post_id: int, db: _orm.session = _fastapi.Depends(_services.get_db)):
    post = await _services.get_post_detail(post_id=post_id, db=db)
    return post


@app.delete("/api/v1/post/{post_id}")
async def delete_post_route(
    post_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
    user: _schemas.UserRep = _fastapi.Depends(_services.current_user)
):
    await _services.delete_post(post_id=post_id, user_id=user.id, db=db)
    return "Post Deleted Successfully."


@app.put("/api/v1/post/{post_id}")
async def Update_post(post_id: int, post_req: _schemas.PostReq, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_post = await _services.get_post_detail(post_id=post_id, db=db)
    return await _services.update_post(post_req=post_req, post=db_post, db=db)
