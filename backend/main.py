from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import SessionLocal, engine, Base
from models import Donor, Recipient, Donation, Driver, Route, RouteStop
from schemas import (
    DonationCreate, DonationResponse,
    RouteCreate, RouteResponse,
    ImpactResponse,
    DonorCreate, RecipientCreate, DriverCreate
)
from services.matching_service import MatchingService
from services.routing_service import RoutingService
from services.impact_service import ImpactService
from services.ai_agent import AIAgent
from services.nyc_data_service import NYCDataService

load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Rescue Route AI API",
    description="Intelligent Food Recovery & Route Optimization Platform",
    version="1.0.0"
)

# CORS middleware
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
# Add Netlify URL if provided
netlify_url = os.getenv("NETLIFY_URL")
if netlify_url:
    cors_origins.append(netlify_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Food Rescue Route AI API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}


@app.post("/donor", response_model=dict)
async def create_donor(donor: DonorCreate, db: Session = Depends(get_db)):
    """Create a new donor"""
    try:
        # Geocode address
        routing_service = RoutingService()
        coords = routing_service._geocode_address(donor.address)
        
        donor_data = donor.model_dump()
        if coords:
            donor_data["latitude"] = coords[0]
            donor_data["longitude"] = coords[1]
        
        db_donor = Donor(**donor_data)
        db.add(db_donor)
        db.commit()
        db.refresh(db_donor)
        return {"id": db_donor.id, "message": "Donor created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create donor: {str(e)}")


@app.post("/recipient", response_model=dict)
async def create_recipient(recipient: RecipientCreate, db: Session = Depends(get_db)):
    """Create a new recipient"""
    try:
        # Geocode address
        routing_service = RoutingService()
        coords = routing_service._geocode_address(recipient.address)
        
        recipient_data = recipient.model_dump()
        if coords:
            recipient_data["latitude"] = coords[0]
            recipient_data["longitude"] = coords[1]
        
        db_recipient = Recipient(**recipient_data)
        db.add(db_recipient)
        db.commit()
        db.refresh(db_recipient)
        return {"id": db_recipient.id, "message": "Recipient created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create recipient: {str(e)}")


@app.post("/driver", response_model=dict)
async def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    """Create a new driver"""
    try:
        driver_data = driver.model_dump()
        if driver.current_location:
            routing_service = RoutingService()
            coords = routing_service._geocode_address(driver.current_location)
            if coords:
                driver_data["latitude"] = coords[0]
                driver_data["longitude"] = coords[1]
        
        db_driver = Driver(**driver_data)
        db.add(db_driver)
        db.commit()
        db.refresh(db_driver)
        return {"id": db_driver.id, "message": "Driver created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create driver: {str(e)}")


@app.post("/donation", response_model=DonationResponse)
async def create_donation(donation: DonationCreate, db: Session = Depends(get_db)):
    """Create a new food donation and trigger matching"""
    try:
        matching_service = MatchingService(db)
        ai_agent = AIAgent()
        
        # Check if donor exists, if not create a default one
        donor = db.query(Donor).filter(Donor.id == donation.donor_id).first()
        if not donor:
            # Create a default donor for testing
            donor = Donor(
                id=donation.donor_id,
                name="Default Donor",
                email="donor@example.com",
                address=donation.address,
                business_type="restaurant"
            )
            db.add(donor)
            db.commit()
        
        # Use AI to classify food category if not provided
        if not donation.food_category:
            from datetime import datetime
            category_str = await ai_agent.classify_food_category(donation.food_type)
            # Map string to enum
            from models import FoodCategory
            category_map = {
                "produce": FoodCategory.PRODUCE,
                "bakery": FoodCategory.BAKERY,
                "prepared": FoodCategory.PREPARED,
                "packaged": FoodCategory.PACKAGED,
                "frozen": FoodCategory.FROZEN,
                "dairy": FoodCategory.DAIRY
            }
            donation.food_category = category_map.get(category_str, FoodCategory.PACKAGED)
        
        # Geocode address
        routing_service = RoutingService()
        coords = routing_service._geocode_address(donation.address)
        
        # Create donation record
        donation_data = donation.model_dump()
        if coords:
            donation_data["latitude"] = coords[0]
            donation_data["longitude"] = coords[1]
        
        db_donation = Donation(**donation_data)
        db.add(db_donation)
        db.commit()
        db.refresh(db_donation)
        
        # Calculate perishability score using AI
        from datetime import datetime
        perishability_score = matching_service.calculate_perishability_score(db_donation)
        # Also use AI to refine it
        ai_perishability = await ai_agent.estimate_perishability(
            db_donation.food_type,
            db_donation.food_category.value if db_donation.food_category else "packaged",
            str(db_donation.posted_at)
        )
        # Average of both
        db_donation.perishability_score = (perishability_score + ai_perishability) / 2
        db.commit()
        
        # Run matching to find recipients
        recipient_options = matching_service.find_matching_recipients(db_donation)
        
        # Calculate match scores
        match_scores = []
        for recipient in recipient_options:
            score = matching_service.calculate_match_score(db_donation, recipient)
            match_scores.append({
                "recipient_id": recipient.id,
                "recipient_name": recipient.name,
                "score": score,
                "distance_miles": matching_service.calculate_distance(
                    db_donation.address, recipient.address
                )
            })
        
        # Sort by score
        match_scores.sort(key=lambda x: x["score"], reverse=True)
        
        return DonationResponse(
            donation_id=db_donation.id,
            recipient_options=[r.id for r in recipient_options],
            match_scores=match_scores
        )
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Donation creation error: {error_details}")
        raise HTTPException(status_code=500, detail=f"Failed to create donation: {str(e)}")


@app.post("/assign_route", response_model=RouteResponse)
async def assign_route(route_data: RouteCreate, db: Session = Depends(get_db)):
    """Assign a route to a driver and optimize it"""
    try:
        routing_service = RoutingService()
        
        # Get donation
        donation = db.query(Donation).filter(Donation.id == route_data.donation_id).first()
        if not donation:
            raise HTTPException(status_code=404, detail="Donation not found")
        
        # Get driver
        driver = db.query(Driver).filter(Driver.id == route_data.driver_id).first()
        if not driver:
            raise HTTPException(status_code=404, detail="Driver not found")
        
        # Get recipient
        recipient = db.query(Recipient).filter(Recipient.id == route_data.recipient_id).first()
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")
        
        # Optimize route using routing service
        route_result = await routing_service.optimize_route(
            start_address=donation.address,
            end_address=recipient.address,
            driver_address=driver.current_location
        )
        
        # Create route record
        db_route = Route(
            donation_id=donation.id,
            driver_id=driver.id,
            recipient_id=recipient.id,
            status="assigned",
            estimated_duration_minutes=route_result["duration_minutes"],
            estimated_distance_miles=route_result["distance_miles"],
            route_instructions=route_result["instructions"]
        )
        db.add(db_route)
        
        # Update donation status
        donation.status = "assigned"
        
        db.commit()
        db.refresh(db_route)
        
        return RouteResponse(
            route_id=db_route.id,
            status=db_route.status,
            estimated_duration_minutes=db_route.estimated_duration_minutes,
            estimated_distance_miles=db_route.estimated_distance_miles,
            instructions=db_route.route_instructions
        )
    except Exception as e:
        import traceback
        print(f"Route assignment error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to assign route: {str(e)}")


@app.get("/impact", response_model=ImpactResponse)
async def get_impact(db: Session = Depends(get_db)):
    """Get cumulative impact metrics"""
    try:
        impact_service = ImpactService(db)
        
        # Get all completed donations
        completed_donations = db.query(Donation).filter(Donation.status == "completed").all()
        
        total_lbs = sum(d.quantity_lbs for d in completed_donations)
        
        impact = impact_service.calculate_impact(total_lbs)
        
        return ImpactResponse(**impact)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get impact: {str(e)}")


@app.get("/impact/realtime")
async def get_realtime_impact(db: Session = Depends(get_db)):
    """Get real-time impact metrics with AI insights"""
    try:
        impact_service = ImpactService(db)
        ai_agent = AIAgent()
        
        # Get all donations (pending, assigned, completed)
        all_donations = db.query(Donation).all()
        completed_donations = db.query(Donation).filter(Donation.status == "completed").all()
        pending_donations = db.query(Donation).filter(Donation.status == "pending").all()
        active_routes = db.query(Route).filter(Route.status.in_(["assigned", "in_progress"])).all()
        
        total_lbs = sum(d.quantity_lbs for d in completed_donations)
        pending_lbs = sum(d.quantity_lbs for d in pending_donations)
        
        impact = impact_service.calculate_impact(total_lbs)
        
        # Calculate potential impact from pending donations
        potential_impact = impact_service.calculate_impact(pending_lbs)
        
        # AI-generated insights
        ai_insight = await ai_agent.decide_driver_assignment(
            perishability_score=7.0,
            volunteer_available=len(active_routes) < 10,
            time_since_posted_minutes=30
        )
        
        return {
            **impact,
            "potential_impact": potential_impact,
            "pending_donations": len(pending_donations),
            "active_routes": len(active_routes),
            "total_donations": len(all_donations),
            "ai_insight": ai_insight.get("reason", "System operating normally"),
            "sustainability_score": min(100, (total_lbs / 1000) * 10)  # Score out of 100
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get realtime impact: {str(e)}")


@app.get("/donations")
async def list_donations(status: Optional[str] = None, db: Session = Depends(get_db)):
    """List all donations, optionally filtered by status"""
    try:
        matching_service = MatchingService(db)
        query = db.query(Donation)
        if status:
            query = query.filter(Donation.status == status)
        
        donations = query.all()
        results = []
        for donation in donations:
            recipient_options = matching_service.find_matching_recipients(donation)
            match_scores = []
            for recipient in recipient_options:
                score = matching_service.calculate_match_score(donation, recipient)
                match_scores.append({
                    "recipient_id": recipient.id,
                    "recipient_name": recipient.name,
                    "score": score,
                    "distance_miles": matching_service.calculate_distance(
                        donation.address, recipient.address
                    )
                })
            match_scores.sort(key=lambda x: x["score"], reverse=True)
            results.append(DonationResponse(
                donation_id=donation.id,
                recipient_options=[r.id for r in recipient_options],
                match_scores=match_scores
            ))
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list donations: {str(e)}")


@app.get("/routes")
async def list_routes(status: Optional[str] = None, db: Session = Depends(get_db)):
    """List all routes, optionally filtered by status"""
    try:
        query = db.query(Route)
        if status:
            query = query.filter(Route.status == status)
        
        routes = query.all()
        return [
            RouteResponse(
                route_id=r.id,
                status=r.status,
                estimated_duration_minutes=r.estimated_duration_minutes,
                estimated_distance_miles=r.estimated_distance_miles,
                instructions=r.route_instructions
            )
            for r in routes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list routes: {str(e)}")


@app.get("/routes/{route_id}/map")
async def get_route_map(route_id: int, db: Session = Depends(get_db)):
    """Get route map data for visualization"""
    try:
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        donation = db.query(Donation).filter(Donation.id == route.donation_id).first()
        recipient = db.query(Recipient).filter(Recipient.id == route.recipient_id).first()
        
        return {
            "route_id": route_id,
            "start": {
                "address": donation.address,
                "lat": donation.latitude,
                "lng": donation.longitude
            },
            "end": {
                "address": recipient.address,
                "lat": recipient.latitude,
                "lng": recipient.longitude
            },
            "distance_miles": route.estimated_distance_miles,
            "duration_minutes": route.estimated_duration_minutes,
            "instructions": route.route_instructions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get route map: {str(e)}")


@app.patch("/route/{route_id}/status")
async def update_route_status(
    route_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update route status"""
    try:
        route = db.query(Route).filter(Route.id == route_id).first()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        route.status = status
        if status == "completed":
            from datetime import datetime
            route.completed_at = datetime.now()
            # Update donation status
            donation = db.query(Donation).filter(Donation.id == route.donation_id).first()
            if donation:
                donation.status = "completed"
                donation.completed_at = datetime.now()
        
        db.commit()
        return {"message": "Route status updated", "route_id": route_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update route status: {str(e)}")


@app.post("/nyc-data/populate-recipients")
async def populate_nyc_recipients(db: Session = Depends(get_db)):
    """Populate recipients from NYC Open Data"""
    try:
        nyc_service = NYCDataService()
        count = await nyc_service.populate_recipients_from_nyc_data(db)
        return {"message": f"Populated {count} recipients from NYC Open Data", "count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to populate NYC data: {str(e)}")


@app.get("/nyc-data/food-pantries")
async def get_nyc_food_pantries(limit: int = 50):
    """Get food pantries from NYC Open Data"""
    try:
        nyc_service = NYCDataService()
        pantries = await nyc_service.get_food_pantries(limit=limit)
        return {"pantries": pantries, "count": len(pantries), "source": "NYC Open Data Portal"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get NYC data: {str(e)}")


@app.get("/geocode/autocomplete")
async def geocode_autocomplete(q: str, limit: int = 5):
    """Address autocomplete using Nominatim (OpenStreetMap) - Free and Open Source"""
    try:
        from geopy.geocoders import Nominatim
        geocoder = Nominatim(user_agent="food_rescue_route_ai")
        
        # Use Nominatim search for autocomplete
        results = geocoder.geocode(q, exactly_one=False, limit=limit)
        
        suggestions = []
        if results:
            for location in results:
                suggestions.append({
                    "display_name": location.address,
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude
                })
        
        return {
            "query": q,
            "suggestions": suggestions,
            "count": len(suggestions),
            "source": "OpenStreetMap (Nominatim) - Free & Open Source"
        }
    except Exception as e:
        return {"query": q, "suggestions": [], "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
