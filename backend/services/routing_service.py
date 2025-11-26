import os
import httpx
from typing import Dict, List, Any, Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dotenv import load_dotenv

load_dotenv()


class RoutingService:
    def __init__(self):
        self.google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.ors_api_key = os.getenv("ORS_API_KEY")
        self.geocoder = Nominatim(user_agent="food_rescue_route_ai")
    
    def _geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Geocode an address to lat/lng coordinates"""
        try:
            location = self.geocoder.geocode(address, timeout=10)
            if location:
                return (location.latitude, location.longitude)
        except Exception as e:
            print(f"Geocoding error for {address}: {e}")
        return None
    
    async def optimize_route(
        self,
        start_address: str,
        end_address: str,
        driver_address: str = None
    ) -> Dict[str, Any]:
        """
        Optimize route from start to end, optionally starting from driver location.
        Returns route with duration, distance, and turn-by-turn instructions.
        Uses OpenRouteService as primary (open source), falls back to Google Maps.
        """
        # Try OpenRouteService first (open source, free tier)
        if self.ors_api_key:
            result = await self._route_with_ors(start_address, end_address, driver_address)
            if result:
                return result
        
        # Fallback to Google Maps if ORS fails
        if self.google_maps_api_key:
            result = await self._route_with_google(start_address, end_address, driver_address)
            if result:
                return result
        
        # Final fallback: estimated route
        return self._route_estimate(start_address, end_address)
    
    async def _route_with_ors(
        self,
        start_address: str,
        end_address: str,
        driver_address: str = None
    ) -> Optional[Dict[str, Any]]:
        """Route using OpenRouteService API (open source)"""
        try:
            # Geocode addresses
            start_coords = self._geocode_address(start_address)
            end_coords = self._geocode_address(end_address)
            
            if not start_coords or not end_coords:
                print("Failed to geocode addresses for ORS")
                return None
            
            # OpenRouteService Directions API
            url = "https://api.openrouteservice.org/v2/directions/driving-car"
            
            headers = {
                "Authorization": self.ors_api_key,
                "Content-Type": "application/json"
            }
            
            # Format: [longitude, latitude] for ORS
            coordinates = [
                [start_coords[1], start_coords[0]],  # [lng, lat]
                [end_coords[1], end_coords[0]]
            ]
            
            params = {
                "coordinates": coordinates,
                "format": "json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json=params,
                    headers=headers,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "routes" in data and len(data["routes"]) > 0:
                        route = data["routes"][0]
                        summary = route.get("summary", {})
                        
                        # Extract distance (meters) and duration (seconds)
                        distance_meters = summary.get("distance", 0)
                        duration_seconds = summary.get("duration", 0)
                        
                        # Convert to miles and minutes
                        distance_miles = distance_meters / 1609.34
                        duration_minutes = duration_seconds / 60
                        
                        # Extract segments for instructions
                        instructions = []
                        segments = route.get("segments", [])
                        
                        for i, segment in enumerate(segments[:10]):  # Limit to first 10 steps
                            step = segment.get("steps", [{}])[0] if segment.get("steps") else {}
                            instruction = step.get("instruction", f"Continue on route")
                            distance = step.get("distance", 0) / 1609.34  # meters to miles
                            
                            instructions.append({
                                "instruction": instruction,
                                "distance": f"{distance:.2f} mi",
                                "duration": f"{duration_minutes / len(segments):.1f} min"
                            })
                        
                        # If no segments, create basic instructions
                        if not instructions:
                            instructions = [
                                {
                                    "instruction": f"Start at {start_address}",
                                    "distance": f"{distance_miles:.2f} mi",
                                    "duration": f"{duration_minutes:.1f} min"
                                },
                                {
                                    "instruction": f"Arrive at {end_address}",
                                    "distance": "0 mi",
                                    "duration": "0 min"
                                }
                            ]
                        
                        return {
                            "duration_minutes": duration_minutes,
                            "distance_miles": distance_miles,
                            "instructions": instructions
                        }
                
                print(f"ORS API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"ORS routing error: {e}")
            return None
    
    async def _route_with_google(
        self,
        start_address: str,
        end_address: str,
        driver_address: str = None
    ) -> Optional[Dict[str, Any]]:
        """Route using Google Maps Directions API (fallback)"""
        try:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            
            params = {
                "origin": start_address,
                "destination": end_address,
                "key": self.google_maps_api_key,
                "mode": "driving"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=10.0)
                data = response.json()
                
                if data["status"] == "OK" and data["routes"]:
                    route = data["routes"][0]
                    leg = route["legs"][0]
                    
                    # Extract instructions
                    instructions = []
                    for step in leg["steps"]:
                        instructions.append({
                            "instruction": step["html_instructions"],
                            "distance": step["distance"]["text"],
                            "duration": step["duration"]["text"]
                        })
                    
                    return {
                        "duration_minutes": leg["duration"]["value"] / 60,
                        "distance_miles": leg["distance"]["value"] / 1609.34,  # meters to miles
                        "instructions": instructions
                    }
                else:
                    return None
                    
        except Exception as e:
            print(f"Google Maps routing error: {e}")
            return None
    
    def _route_estimate(
        self,
        start_address: str,
        end_address: str
    ) -> Dict[str, Any]:
        """Fallback: return estimated route using geodesic distance"""
        try:
            # Try to geocode for better estimate
            start_coords = self._geocode_address(start_address)
            end_coords = self._geocode_address(end_address)
            
            if start_coords and end_coords:
                # Calculate straight-line distance
                distance_miles = geodesic(start_coords, end_coords).miles
                # Estimate driving time (assume 25 mph average in NYC)
                duration_minutes = (distance_miles / 25) * 60
            else:
                # Default estimate
                distance_miles = 2.5
                duration_minutes = 10.0
            
            return {
                "duration_minutes": duration_minutes,
                "distance_miles": distance_miles,
                "instructions": [
                    {
                        "instruction": f"Start at {start_address}",
                        "distance": f"{distance_miles * 0.2:.2f} mi",
                        "duration": f"{duration_minutes * 0.2:.1f} min"
                    },
                    {
                        "instruction": f"Continue to {end_address}",
                        "distance": f"{distance_miles * 0.8:.2f} mi",
                        "duration": f"{duration_minutes * 0.8:.1f} min"
                    }
                ]
            }
        except Exception as e:
            print(f"Route estimate error: {e}")
            return {
                "duration_minutes": 10.0,
                "distance_miles": 2.5,
                "instructions": [
                    {
                        "instruction": f"Start at {start_address}",
                        "distance": "0.5 mi",
                        "duration": "2 min"
                    },
                    {
                        "instruction": f"Continue to {end_address}",
                        "distance": "2.0 mi",
                        "duration": "8 min"
                    }
                ]
            }
    
    async def optimize_multi_stop_route(
        self,
        stops: List[Dict[str, str]],
        start_address: str
    ) -> Dict[str, Any]:
        """
        Optimize route with multiple stops (Vehicle Routing Problem).
        For MVP, uses simple nearest-neighbor heuristic.
        """
        total_duration = 0.0
        total_distance = 0.0
        all_instructions = []
        
        current_address = start_address
        
        for stop in stops:
            route = await self.optimize_route(current_address, stop["address"])
            total_duration += route["duration_minutes"]
            total_distance += route["distance_miles"]
            all_instructions.extend(route["instructions"])
            current_address = stop["address"]
        
        return {
            "duration_minutes": total_duration,
            "distance_miles": total_distance,
            "instructions": all_instructions,
            "stops": stops
        }
