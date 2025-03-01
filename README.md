# Welcome to the Marriage Matchmaking App


# Instructions to run the app

1. Clone the project
2. Start the project by the command => uvicorn main:app --reload
3. Seed the data with dummy data => python seed_users.py


#schemas.py

    from pydantic import BaseModel
    class UserResponse(BaseModel):
        id: int
        name: str
        age: int
        email: str
        gender: str
        city: str
        interests: str

    class Config:
        orm_mode = True

This Python file defines a `UserResponse` model using Pydantic, which ensures data validation for user attributes like `id`, `name`, `age`, `email`, `gender`, `city`, and `interests`. The `Config` class with `orm_mode = True` allows compatibility with ORM objects, enabling automatic conversion from database models to Pydantic schemas.


#models.py

    from sqlalchemy import Column, Integer, String
    from database import Base
    
    class User(Base):
        __tablename__ = "users"
    
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)
        age = Column(Integer)
        email = Column(String, unique=True, index=True)
        gender = Column(String)
        city = Column(String)
        interests = Column(String)


This file defines a SQLAlchemy model `User` representing a database table named `"users"`, inheriting from `Base`. It includes columns for `id`, `name`, `age`, `email`, `gender`, `city`, and `interests`, with `id` as the primary key and `email` marked as unique.

#database.py

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    
    DATABASE_URL = "sqlite:///./test.db"
    
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

This file sets up the database connection using SQLAlchemy with SQLite (`test.db`). It creates an `engine` for database interactions, a `SessionLocal` for managing sessions, and a `Base` class for defining ORM models.

#seed_users.py

This file inserts dummy user data into the database using SQLAlchemy. It creates a database session, iterates over a list of predefined users, adds them to the `users` table, commits the changes, and then closes the session.

#main.py

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Renders the homepage using `index.html`. |
| `/users/create` | `GET` | Displays the form to create a new user. |
| `/users/` | `POST` | Creates a new user and redirects to the users list. |
| `/users` | `GET` | Retrieves and displays a list of all users. |
| `/users/{user_id}` | `GET` | Retrieves and displays a specific user's profile. |
| `/users/{user_id}/update` | `GET` | Displays the update form for a specific user. |
| `/users/{user_id}` | `POST` | Updates a specific user's details and redirects to their profile. |
| `/users/{user_id}/delete` | `GET` | Deletes a specific user and redirects to the users list. |
| `/users/{user_id}/matches` | `GET` | Finds and displays potential matches for a user based on gender and shared interests. |


#templates folder

| Template File | Description |
|--------------|-------------|
| `index.html` | Homepage of the application. |
| `create_user.html` | Form page for creating a new user. |
| `match_profile.html` | Displays potential matches for a user. |
| `update_user.html` | Form page for updating a user's details. |
| `user_profile.html` | Displays the profile of a specific user. |
| `users.html` | Shows a list of all registered users. |



Thank You!
