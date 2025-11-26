from sqlalchemy.orm import Session
from typing import List
from models import Donation, Recipient, FoodCategory
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import os
import httpx
from datetime import datetime


class MatchingService:
    def __init__(self, db: Session):
        self.db = db
        self.geocoder = Nominatim(user_agent="food_rescue_route_ai")
    
    def _geocode_address(self, address: str):
        """Geocode address to get coordinates"""
        try:
            location = self.geocoder.geocode(address, timeout=10)
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            print(f"Geocoding error: {e}")
        return None
    
    def calculate_distance(self, address1: str, address2: str) -> float:
        """Calculate distance between two addresses in miles"""
        try:
            coords1 = self._geocode_address(address1)
            coords2 = self._geocode_address(address2)
            
            if coords1 and coords2:
                return geodesic(coords1, coords2).miles
            else:
                # Fallback estimate
                return 2.5
        except Exception:
            return 5.0  # Default distance
    
    def calculate_perishability_score(self, donation: Donation) -> float:
        """Calculate perishability score (0-10) based on food category and time"""
        # Food category decay factors (from USDA data)
        food_factors = {
            FoodCategory.PRODUCE: 0.7,
            FoodCategory.PREPARED: 1.2,
            FoodCategory.BAKERY: 0.9,
            FoodCategory.PACKAGED: 0.3,
            FoodCategory.FROZEN: 0.1,
            FoodCategory.DAIRY: 0.8
        }
        
        # Get time since posted
        time_since_posted = (datetime.now() - donation.posted_at).total_seconds() / 3600  # hours
        
        # Get decay factor for this food category
        decay_factor = food_factors.get(donation.food_category, 0.5)
        
        # Calculate decay rate
        decay_rate = decay_factor * time_since_posted
        
        # Perishability score (higher = more perishable, needs faster pickup)
        perishability_score = min(10.0, decay_rate * 2)
        
        return perishability_score
    
    def calculate_distance_score(self, distance_miles: float) -> float:
        """Calculate distance score (0-10, higher is better)"""
        # Distance score = 10 - (miles / 2)
        # Closer distances get higher scores
        distance_score = max(0.0, 10.0 - (distance_miles / 2))
        return distance_score
    
    def calculate_match_score(self, donation: Donation, recipient: Recipient) -> float:
        """Calculate overall match score between donation and recipient"""
        # Category match (0-1)
        category_match = 0.0
        if donation.food_category and recipient.categories_needed:
            if donation.food_category.value in recipient.categories_needed:
                category_match = 1.0
            elif any(cat in recipient.categories_needed for cat in ["all", "any"]):
                category_match = 0.8
        
        # Capacity match (0-1)
        capacity_match = 0.0
        if recipient.storage_capacity_lbs:
            if donation.quantity_lbs <= recipient.storage_capacity_lbs:
                capacity_match = 1.0
            else:
                # Partial match if donation is within 150% of capacity
                capacity_match = max(0.0, 1.0 - (donation.quantity_lbs / recipient.storage_capacity_lbs - 1.0))
        
        # Distance score (0-10, normalized to 0-1)
        distance_miles = self.calculate_distance(donation.address, recipient.address)
        distance_score = self.calculate_distance_score(distance_miles) / 10.0
        
        # Weighted match score
        match_score = (category_match * 0.5) + (capacity_match * 0.3) + (distance_score * 0.2)
        
        return match_score
    
    def find_matching_recipients(self, donation: Donation, limit: int = 5) -> List[Recipient]:
        """Find top N matching recipients for a donation"""
        # Get all recipients
        all_recipients = self.db.query(Recipient).all()
        
        # Calculate match scores for all
        scored_recipients = []
        for recipient in all_recipients:
            score = self.calculate_match_score(donation, recipient)
            if score > 0:  # Only include recipients with positive match
                scored_recipients.append((score, recipient))
        
        # Sort by score (descending)
        scored_recipients.sort(key=lambda x: x[0], reverse=True)
        
        # Return top N
        return [recipient for _, recipient in scored_recipients[:limit]]
