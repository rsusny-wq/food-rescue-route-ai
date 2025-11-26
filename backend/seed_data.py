"""
Script to seed the database with sample data for testing.
Run this after setting up the database.
"""
import os
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Donor, Recipient, Driver, Donation, FoodCategory, StorageRequirement
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()


def seed_data():
    """Seed the database with sample data"""
    
    # Create sample donors
    donors = [
        Donor(
            name="Joe's Pizza",
            email="joe@pizza.com",
            phone="212-555-0101",
            address="123 Broadway, New York, NY 10001",
            latitude=40.7128,
            longitude=-74.0060,
            business_type="restaurant"
        ),
        Donor(
            name="Whole Foods Market",
            email="contact@wholefoods.com",
            phone="212-555-0102",
            address="250 7th Ave, New York, NY 10001",
            latitude=40.7489,
            longitude=-73.9940,
            business_type="grocery"
        ),
        Donor(
            name="NYU Dining Hall",
            email="dining@nyu.edu",
            phone="212-555-0103",
            address="383 Lafayette St, New York, NY 10003",
            latitude=40.7295,
            longitude=-73.9965,
            business_type="cafeteria"
        ),
    ]
    
    for donor in donors:
        db.add(donor)
    db.commit()
    print(f"Created {len(donors)} donors")
    
    # Create sample recipients
    recipients = [
        Recipient(
            name="NYC Food Bank",
            email="info@nycfoodbank.org",
            phone="212-555-0201",
            address="355 Food Center Dr, Bronx, NY 10474",
            latitude=40.8176,
            longitude=-73.8786,
            organization_type="food_bank",
            categories_needed=["produce", "packaged", "prepared", "bakery"],
            storage_capacity_lbs=5000.0,
            daily_time_windows=[
                {"start": "09:00", "end": "17:00"}
            ]
        ),
        Recipient(
            name="Community Fridge - Brooklyn",
            email="fridge@community.org",
            phone="212-555-0202",
            address="456 Atlantic Ave, Brooklyn, NY 11217",
            latitude=40.6881,
            longitude=-73.9808,
            organization_type="community_fridge",
            categories_needed=["produce", "packaged"],
            storage_capacity_lbs=200.0,
            daily_time_windows=[
                {"start": "08:00", "end": "20:00"}
            ]
        ),
        Recipient(
            name="Homeless Shelter - Manhattan",
            email="shelter@help.org",
            phone="212-555-0203",
            address="789 5th Ave, New York, NY 10022",
            latitude=40.7614,
            longitude=-73.9776,
            organization_type="shelter",
            categories_needed=["prepared", "packaged", "bakery"],
            storage_capacity_lbs=1000.0,
            daily_time_windows=[
                {"start": "10:00", "end": "18:00"}
            ]
        ),
    ]
    
    for recipient in recipients:
        db.add(recipient)
    db.commit()
    print(f"Created {len(recipients)} recipients")
    
    # Create sample drivers
    drivers = [
        Driver(
            name="John Volunteer",
            email="john@volunteer.com",
            phone="212-555-0301",
            current_location="100 Main St, New York, NY 10001",
            latitude=40.7128,
            longitude=-74.0060,
            driver_type="volunteer",
            availability_window=[
                {"start": "09:00", "end": "17:00"}
            ],
            completion_rate=0.95,
            volunteer_points=150
        ),
        Driver(
            name="Sarah Driver",
            email="sarah@driver.com",
            phone="212-555-0302",
            current_location="200 Park Ave, New York, NY 10017",
            latitude=40.7505,
            longitude=-73.9776,
            driver_type="volunteer",
            availability_window=[
                {"start": "10:00", "end": "16:00"}
            ],
            completion_rate=0.88,
            volunteer_points=89
        ),
    ]
    
    for driver in drivers:
        db.add(driver)
    db.commit()
    print(f"Created {len(drivers)} drivers")
    
    # Create sample donations
    now = datetime.now()
    donations = [
        Donation(
            donor_id=1,
            food_type="Fresh vegetables and fruits",
            food_category=FoodCategory.PRODUCE,
            quantity_lbs=25.0,
            pickup_window_start=now + timedelta(hours=2),
            pickup_window_end=now + timedelta(hours=4),
            address="123 Broadway, New York, NY 10001",
            latitude=40.7128,
            longitude=-74.0060,
            storage_requirement=StorageRequirement.COLD,
            perishability_score=7.5,
            status="pending"
        ),
        Donation(
            donor_id=2,
            food_type="Prepared meals - pasta and salads",
            food_category=FoodCategory.PREPARED,
            quantity_lbs=50.0,
            pickup_window_start=now + timedelta(hours=1),
            pickup_window_end=now + timedelta(hours=3),
            address="250 7th Ave, New York, NY 10001",
            latitude=40.7489,
            longitude=-73.9940,
            storage_requirement=StorageRequirement.HOT,
            perishability_score=8.5,
            status="pending"
        ),
        Donation(
            donor_id=3,
            food_type="Bakery items - bread and pastries",
            food_category=FoodCategory.BAKERY,
            quantity_lbs=30.0,
            pickup_window_start=now + timedelta(hours=3),
            pickup_window_end=now + timedelta(hours=5),
            address="383 Lafayette St, New York, NY 10003",
            latitude=40.7295,
            longitude=-73.9965,
            storage_requirement=StorageRequirement.SHELF_STABLE,
            perishability_score=6.0,
            status="pending"
        ),
    ]
    
    for donation in donations:
        db.add(donation)
    db.commit()
    print(f"Created {len(donations)} donations")
    
    print("\nDatabase seeded successfully!")
    print("\nSample data created:")
    print(f"  - {len(donors)} donors")
    print(f"  - {len(recipients)} recipients")
    print(f"  - {len(drivers)} drivers")
    print(f"  - {len(donations)} donations")


if __name__ == "__main__":
    seed_data()
    db.close()

