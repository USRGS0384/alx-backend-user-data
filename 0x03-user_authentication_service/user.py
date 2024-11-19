#!/usr/bin/env python3
"""
Users model
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for ORM models
Base = declarative_base()

# Define the User model
class User(Base):
    """
    SQLAlchemy model for the 'users' table.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)

# Example usage: setting up a SQLite database
def main():
    # Create the database engine (replace SQLite with your DB URI if needed)
    engine = create_engine('sqlite:///users.db', echo=True)

    # Create all tables in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Example: Add a new user
    new_user = User(
        email="example@example.com",
        hashed_password="hashed_password_123",
        session_id=None,
        reset_token=None
    )
    session.add(new_user)
    session.commit()

    # Query and print users
    users = session.query(User).all()
    for user in users:
        print(f"ID: {user.id}, Email: {user.email}, Password: {user.hashed_password}")

    # Close the session
    session.close()

if __name__ == "__main__":
    main()
