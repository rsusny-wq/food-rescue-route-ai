from sqlalchemy.orm import Session
from typing import Dict


class ImpactService:
    """
    Calculate environmental and social impact metrics based on EPA WARM Model
    and USDA conversion factors.
    """
    
    # USDA constant: 1.2 pounds of food = 1 meal
    POUNDS_PER_MEAL = 1.2
    
    # EPA WARM Model: 1 lb food waste ≈ 2.5 lbs CO₂e
    CO2E_PER_POUND = 2.5
    
    # EPA: 1 ton food waste → 0.45 tons CH₄ avoided
    CH4_PER_TON = 0.45
    POUNDS_PER_TON = 2000
    
    # EPA: 1 cubic yard landfill density ≈ 450 lbs food waste
    POUNDS_PER_CUBIC_YARD = 450
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_impact(self, pounds_rescued: float) -> Dict[str, float]:
        """
        Calculate all impact metrics from pounds of food rescued.
        
        Returns:
            - meals: Number of meals provided
            - co2e_avoided: CO₂ equivalent avoided (lbs)
            - ch4_avoided_tons: Methane avoided (tons)
            - landfill_space_saved: Landfill space saved (cubic yards)
        """
        # Meals provided
        meals = pounds_rescued / self.POUNDS_PER_MEAL
        
        # CO₂e avoided
        co2e_avoided = pounds_rescued * self.CO2E_PER_POUND
        
        # Methane avoided
        tons_rescued = pounds_rescued / self.POUNDS_PER_TON
        ch4_avoided_tons = tons_rescued * self.CH4_PER_TON
        
        # Landfill space saved
        landfill_space_saved = pounds_rescued / self.POUNDS_PER_CUBIC_YARD
        
        return {
            "lbs_rescued": pounds_rescued,
            "meals": round(meals, 2),
            "co2e_avoided": round(co2e_avoided, 2),
            "ch4_avoided_tons": round(ch4_avoided_tons, 4),
            "landfill_space_saved": round(landfill_space_saved, 2)
        }
    
    def calculate_donation_impact(self, donation_id: int) -> Dict[str, float]:
        """Calculate impact for a specific donation"""
        from models import Donation
        
        donation = self.db.query(Donation).filter(Donation.id == donation_id).first()
        if not donation:
            return {}
        
        return self.calculate_impact(donation.quantity_lbs)

