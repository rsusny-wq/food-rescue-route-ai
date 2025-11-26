"""
NYC Open Data Integration Service
Fetches data from NYC Open Data Portal APIs (free, no API key required)
"""
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime


class NYCDataService:
    """
    Service to fetch NYC open data for food pantries, neighborhoods, etc.
    All NYC Open Data APIs are free and don't require API keys.
    """
    
    BASE_URL = "https://data.cityofnewyork.us/resource"
    
    async def get_food_pantries(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch food pantries and emergency food locations from NYC DOHMH
        Dataset: Food Help NYC
        """
        try:
            url = f"{self.BASE_URL}/9cy3-7kc7.json"
            params = {
                "$limit": limit,
                "$where": "status='Open'",  # Only open locations
                "$order": "name ASC"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    data = response.json()
                    # Transform to our format
                    pantries = []
                    for item in data:
                        pantries.append({
                            "name": item.get("name", "Unknown"),
                            "address": item.get("address", ""),
                            "borough": item.get("borough", ""),
                            "latitude": float(item.get("latitude", 0)) if item.get("latitude") else None,
                            "longitude": float(item.get("longitude", 0)) if item.get("longitude") else None,
                            "phone": item.get("phone", ""),
                            "hours": item.get("hours", ""),
                            "type": "food_pantry"
                        })
                    return pantries
                else:
                    print(f"NYC Data API error: {response.status_code}")
                    return []
        except Exception as e:
            print(f"Error fetching food pantries: {e}")
            return []
    
    async def get_community_fridges(self) -> List[Dict[str, Any]]:
        """
        Fetch community fridge locations (if available in NYC Open Data)
        For now, returns empty list - can be extended when dataset is available
        """
        # NYC Open Data may have community fridge data in the future
        # For now, return empty or use food pantries as proxy
        return []
    
    async def get_neighborhood_data(self, neighborhood: str = None) -> Dict[str, Any]:
        """
        Fetch neighborhood data from NYC Neighborhood Tabulation Areas
        """
        try:
            url = f"{self.BASE_URL}/fn6f-htvy.json"
            params = {"$limit": 100}
            
            if neighborhood:
                params["$where"] = f"ntaname LIKE '%{neighborhood}%'"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
        except Exception as e:
            print(f"Error fetching neighborhood data: {e}")
            return {}
    
    async def get_traffic_data(self, location: str = None) -> Dict[str, Any]:
        """
        Fetch traffic volume data from NYC DOT
        Can be used to estimate delays
        """
        try:
            # NYC DOT Traffic Volume Counts
            url = f"{self.BASE_URL}/7ym2-wayt.json"
            params = {"$limit": 50}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {}
        except Exception as e:
            print(f"Error fetching traffic data: {e}")
            return {}
    
    async def populate_recipients_from_nyc_data(self, db) -> int:
        """
        Populate recipients table with NYC food pantry data
        Returns number of recipients added
        """
        from models import Recipient
        
        pantries = await self.get_food_pantries(limit=50)
        added_count = 0
        
        for pantry in pantries:
            # Check if recipient already exists
            existing = db.query(Recipient).filter(
                Recipient.name == pantry["name"],
                Recipient.address == pantry["address"]
            ).first()
            
            if not existing and pantry.get("latitude") and pantry.get("longitude"):
                recipient = Recipient(
                    name=pantry["name"],
                    email=f"contact@{pantry['name'].lower().replace(' ', '')}.org",
                    phone=pantry.get("phone", ""),
                    address=pantry["address"],
                    latitude=pantry["latitude"],
                    longitude=pantry["longitude"],
                    organization_type="food_pantry",
                    categories_needed=["produce", "packaged", "prepared", "bakery"],
                    storage_capacity_lbs=1000.0,  # Default capacity
                    daily_time_windows=[{"start": "09:00", "end": "17:00"}]
                )
                db.add(recipient)
                added_count += 1
        
        db.commit()
        return added_count

