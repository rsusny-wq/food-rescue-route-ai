from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum


class DonationStatus(str, enum.Enum):
    PENDING = "pending"
    MATCHED = "matched"
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    COMPLETED = "completed"
    EXPIRED = "expired"


class RouteStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FoodCategory(str, enum.Enum):
    PRODUCE = "produce"
    BAKERY = "bakery"
    PREPARED = "prepared"
    PACKAGED = "packaged"
    FROZEN = "frozen"
    DAIRY = "dairy"


class StorageRequirement(str, enum.Enum):
    HOT = "hot"
    COLD = "cold"
    FROZEN = "frozen"
    SHELF_STABLE = "shelf_stable"


class Donor(Base):
    __tablename__ = "donors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    business_type = Column(String)  # restaurant, grocery, cafeteria, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    donations = relationship("Donation", back_populates="donor")


class Recipient(Base):
    __tablename__ = "recipients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    organization_type = Column(String)  # food_bank, shelter, community_fridge, etc.
    categories_needed = Column(JSON)  # List of FoodCategory values
    storage_capacity_lbs = Column(Float)
    daily_time_windows = Column(JSON)  # List of time windows
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    routes = relationship("Route", back_populates="recipient")


class Driver(Base):
    __tablename__ = "drivers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=False)
    current_location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    driver_type = Column(String)  # volunteer or courier
    availability_window = Column(JSON)  # Time windows when available
    completion_rate = Column(Float, default=1.0)
    volunteer_points = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    routes = relationship("Route", back_populates="driver")


class Donation(Base):
    __tablename__ = "donations"
    
    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False)
    food_type = Column(String, nullable=False)
    food_category = Column(SQLEnum(FoodCategory))
    quantity_lbs = Column(Float, nullable=False)
    pickup_window_start = Column(DateTime(timezone=True), nullable=False)
    pickup_window_end = Column(DateTime(timezone=True), nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    storage_requirement = Column(SQLEnum(StorageRequirement))
    perishability_score = Column(Float)  # 0-10
    status = Column(SQLEnum(DonationStatus), default=DonationStatus.PENDING)
    posted_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    donor = relationship("Donor", back_populates="donations")
    routes = relationship("Route", back_populates="donation")


class Route(Base):
    __tablename__ = "routes"
    
    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("donations.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("recipients.id"), nullable=False)
    status = Column(SQLEnum(RouteStatus), default=RouteStatus.ASSIGNED)
    estimated_duration_minutes = Column(Float)
    estimated_distance_miles = Column(Float)
    route_instructions = Column(JSON)  # Turn-by-turn instructions
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    donation = relationship("Donation", back_populates="routes")
    driver = relationship("Driver", back_populates="routes")
    recipient = relationship("Recipient", back_populates="routes")
    stops = relationship("RouteStop", back_populates="route")


class RouteStop(Base):
    __tablename__ = "route_stops"
    
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("routes.id"), nullable=False)
    stop_type = Column(String)  # pickup or delivery
    address = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    sequence = Column(Integer)  # Order in route
    estimated_arrival = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    route = relationship("Route", back_populates="stops")

