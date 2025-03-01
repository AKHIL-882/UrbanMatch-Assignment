from sqlalchemy.orm import Session
from models import User  # Ensure this matches your FastAPI model
from database import SessionLocal

# Define dummy users
dummy_users = [
    {"name": "Alice", "age": 25, "email": "alice@example.com", "gender": "Female", "city": "New York", "interests": "Reading, Traveling,Coding"},
    {"name": "Bob", "age": 30, "email": "bob@example.com", "gender": "Male", "city": "Los Angeles", "interests": "Gaming, Hiking"},
    {"name": "Charlie", "age": 28, "email": "charlie@example.com", "gender": "Male", "city": "Chicago", "interests": "Music, Coding"},
    {"name": "Diana", "age": 24, "email": "diana@example.com", "gender": "Female", "city": "San Francisco", "interests": "Dancing, Painting, Hiking"},
]

# Create a database session
db: Session = SessionLocal()

# Insert users
for user in dummy_users:
    db.add(User(**user))

# Commit changes
db.commit()
db.close()

print("Dummy users added successfully!")
