from utils.token import create_access_token
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import auth

from database import SessionLocal, engine
from routers import prompt_routes

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(prompt_routes.router)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "API Running"}


@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        print("Signup called")

        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        print("Checked existing user")

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = auth.hash_password(user.password)
        print("Password hashed")

        new_user = models.User(
            email=user.email,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print("User saved")

        return {"message": "User created successfully"}

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}


@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if db_user is None:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    # 🔐 Create JWT token
    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }