from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
import auth

from database import SessionLocal, engine
from utils.token import create_access_token

# ✅ Import routers
from routers import prompt_routes
from routers import analytics_routes   # NEW

# ✅ Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Include routers
app.include_router(prompt_routes.router)
app.include_router(analytics_routes.router)   # NEW


# ✅ Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "API Running"}


# ✅ Signup
@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# ✅ Login (JWT)
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