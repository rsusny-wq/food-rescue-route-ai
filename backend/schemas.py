from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime
from models import DonationStatus, RouteStatus, FoodCategory, StorageRequirement


class DonorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: str
    business_type: Optional[str] = None


class RecipientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: str
    organization_type: Optional[str] = None
    categories_needed: List[str] = []
    storage_capacity_lbs: float
    daily_time_windows: List[Dict[str, str]] = []


class DriverCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    current_location: Optional[str] = None
    driver_type: str = "volunteer"
    availability_window: Optional[List[Dict[str, str]]] = None


class DonationCreate(BaseModel):
    donor_id: int
    food_type: str
    food_category: Optional[FoodCategory] = None
    quantity_lbs: float
    pickup_window_start: datetime
    pickup_window_end: datetime
    address: str
    storage_requirement: Optional[StorageRequirement] = None


class MatchScore(BaseModel):
    recipient_id: int
    recipient_name: str
    score: float
    distance_miles: float


class DonationResponse(BaseModel):
    donation_id: int
    recipient_options: List[int]
    match_scores: List[MatchScore]
    
    class Config:
        from_attributes = True


class RouteCreate(BaseModel):
    donation_id: int
    driver_id: int
    recipient_id: int


class RouteResponse(BaseModel):
    route_id: int
    status: RouteStatus
    estimated_duration_minutes: Optional[float] = None
    estimated_distance_miles: Optional[float] = None
    instructions: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        from_attributes = True


class ImpactResponse(BaseModel):
    lbs_rescued: float
    meals: float
    co2e_avoided: float
    ch4_avoided_tons: float
    landfill_space_saved: float

