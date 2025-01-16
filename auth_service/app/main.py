from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from . import models, schemas, database, auth
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.on_event("startup")
async def startup_event():
    try:
        # 确保导入了所有模型
        from . import models
        # 创建所有表
        database.Base.metadata.create_all(bind=database.engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
# 用户注册
@app.post("/register")
async def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return {"message": "User created successfully"}


# 用户登录
@app.post("/login")
async def login(request: Request, user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 记录登录历史
    login_history = models.LoginHistory(
        user_id=db_user.id,
        user_agent=str(request.headers.get("user-agent"))
    )
    db.add(login_history)
    db.commit()

    # 生成令牌
    access_token = auth.create_access_token({"sub": user.email})
    refresh_token = auth.create_refresh_token({"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# 刷新令牌
@app.post("/refresh")
async def refresh_token(token: schemas.RefreshToken):
    payload = auth.verify_token(token.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = auth.create_access_token({"sub": payload.get("sub")})
    return {"access_token": new_access_token}


# 更新用户信息
@app.put("/user/update")
async def update_user(
        user_update: schemas.UserUpdate,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    payload = auth.verify_token(token)
    db_user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()

    if user_update.email:
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = auth.get_password_hash(user_update.password)

    db.commit()
    return {"message": "User updated successfully"}


# 查看登录历史
@app.get("/user/history")
async def get_login_history(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(database.get_db)
):
    payload = auth.verify_token(token)
    db_user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()

    history = db.query(models.LoginHistory).filter(
        models.LoginHistory.user_id == db_user.id
    ).all()

    return history


# 退出登录
@app.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    auth.redis_client.sadd("blacklisted_tokens", token)
    return {"message": "Successfully logged out"}
