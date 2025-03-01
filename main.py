from fastapi import FastAPI, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models
from sqlalchemy import func
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from models import User
from schemas import UserResponse
from fastapi import Request

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/users/create", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@app.post("/users/", response_class=RedirectResponse)
def create_user(
        name: str = Form(...),
        email: str = Form(...),
        gender: str = Form(...),
        age: int = Form(...),
        city: str = Form(...),
        interests: str = Form(...),
        db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(name=name, email=email, gender=gender, city=city, interests=interests, age=age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return RedirectResponse(url="/users", status_code=303)


@app.get("/users", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.get("/users/{user_id}", response_class=HTMLResponse)
def read_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_profile.html", {"request": request, "user": user})


@app.get("/users/{user_id}/update", response_class=HTMLResponse)
def update_user_form(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("update_user.html", {"request": request, "user": user})


@app.post("/users/{user_id}")
def update_user(
        user_id: int,
        name: str = Form(...),
        email: str = Form(...),
        gender: str = Form(...),
        age: int = Form(...),
        city: str = Form(...),
        interests: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = name
    user.email = email
    user.gender = gender
    user.age = age
    user.interests = interests
    user.city = city
    db.commit()
    db.refresh(user)

    return RedirectResponse(url=f"/users/{user_id}", status_code=303)


@app.get("/users/{user_id}/delete", response_class=RedirectResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return RedirectResponse(url="/users", status_code=303)


@app.get("/users/{user_id}/matches", response_model=List[UserResponse])
def find_matches(user_id: int, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    opposite_gender = "Male" if user.gender.lower() == "female" else "Female"
    potential_matches = db.query(User).filter(
        User.gender == opposite_gender,
        User.id != user.id,
        func.abs(User.age - user.age) <= 5
    ).all()

    # Debugging: Print or log potential matches
    print(f"Potential Matches for {user.name}: {[(m.id, m.name, m.age, m.interests) for m in potential_matches]}")

    # Filter matches based on common interests
    user_interests = set(interest.strip() for interest in user.interests.lower().split(","))

    final_matches = [
        match for match in potential_matches
        if any(interest.strip() in user_interests for interest in match.interests.lower().split(","))
    ]

    return templates.TemplateResponse("match_profile.html", {"request": request, "user": user, "matches": final_matches})

