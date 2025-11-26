"""
Initialize database - creates tables and optionally seeds data
"""
import os
from sqlalchemy import create_engine, text
from database import Base, engine, SessionLocal
from models import *
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def check_database_connection():
    """Check if database connection works"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("\nPlease check your DATABASE_URL in .env file")
        print("For local PostgreSQL: postgresql://user:password@localhost:5432/food_rescue")
        print("For Docker: postgresql://foodrescue:foodrescue123@localhost:5432/food_rescue")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Food Rescue Route AI - Database Initialization")
    print("=" * 50)
    
    if check_database_connection():
        init_database()
        print("\nDatabase setup complete!")
        print("\nNext steps:")
        print("1. Run 'python seed_data.py' to add sample data")
        print("2. Run 'python -m uvicorn main:app --reload' to start the server")
    else:
        print("\nPlease fix database connection before proceeding")

