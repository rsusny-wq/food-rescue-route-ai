import os
from typing import Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class AIAgent:
    """
    Lightweight AI agent for orchestration decisions using Google Gemini:
    - Classify food categories
    - Estimate perishability
    - Decide driver assignment vs courier fallback
    """
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if self.gemini_api_key:
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Gemini initialization error: {e}")
    
    async def classify_food_category(self, food_type: str) -> str:
        """Classify food into category using AI"""
        if not self.model:
            # Fallback: simple keyword matching
            food_lower = food_type.lower()
            if any(word in food_lower for word in ["produce", "vegetable", "fruit", "fresh"]):
                return "produce"
            elif any(word in food_lower for word in ["bread", "pastry", "bakery", "baked"]):
                return "bakery"
            elif any(word in food_lower for word in ["prepared", "meal", "cooked", "hot"]):
                return "prepared"
            elif any(word in food_lower for word in ["frozen", "ice"]):
                return "frozen"
            elif any(word in food_lower for word in ["milk", "cheese", "dairy", "yogurt"]):
                return "dairy"
            else:
                return "packaged"
        
        try:
            prompt = f"""You are a food classification system. Classify this food into one of these categories: produce, bakery, prepared, packaged, frozen, dairy.

Food: {food_type}

Return only the category name, nothing else."""
            
            response = self.model.generate_content(prompt)
            category = response.text.strip().lower()
            
            # Validate category
            valid_categories = ["produce", "bakery", "prepared", "packaged", "frozen", "dairy"]
            if category in valid_categories:
                return category
            else:
                # Fallback to keyword matching
                food_lower = food_type.lower()
                if any(word in food_lower for word in ["produce", "vegetable", "fruit", "fresh"]):
                    return "produce"
                elif any(word in food_lower for word in ["bread", "pastry", "bakery", "baked"]):
                    return "bakery"
                elif any(word in food_lower for word in ["prepared", "meal", "cooked", "hot"]):
                    return "prepared"
                elif any(word in food_lower for word in ["frozen", "ice"]):
                    return "frozen"
                elif any(word in food_lower for word in ["milk", "cheese", "dairy", "yogurt"]):
                    return "dairy"
                return "packaged"
        except Exception as e:
            print(f"AI classification error: {e}")
            return "packaged"  # Default fallback
    
    async def estimate_perishability(
        self,
        food_type: str,
        food_category: str,
        posted_time: str
    ) -> float:
        """Estimate perishability score (0-10) using AI"""
        if not self.model:
            # Fallback: use category-based estimation
            category_scores = {
                "produce": 7.0,
                "prepared": 8.5,
                "bakery": 6.0,
                "dairy": 7.5,
                "frozen": 2.0,
                "packaged": 3.0
            }
            return category_scores.get(food_category, 5.0)
        
        try:
            prompt = f"""You are a food safety expert. Estimate perishability on a scale of 0-10, where 10 is highly perishable (needs immediate pickup) and 0 is shelf-stable.

Food: {food_type}
Category: {food_category}
Posted: {posted_time}

Return only a number between 0 and 10, nothing else."""
            
            response = self.model.generate_content(prompt)
            score_text = response.text.strip()
            
            # Extract number
            try:
                score = float(''.join(filter(str.isdigit, score_text.split()[0] if score_text.split() else "5")))
                return min(10.0, max(0.0, score))
            except:
                # Fallback to category-based
                category_scores = {
                    "produce": 7.0,
                    "prepared": 8.5,
                    "bakery": 6.0,
                    "dairy": 7.5,
                    "frozen": 2.0,
                    "packaged": 3.0
                }
                return category_scores.get(food_category, 5.0)
        except Exception as e:
            print(f"AI perishability estimation error: {e}")
            return 5.0  # Default fallback
    
    async def decide_driver_assignment(
        self,
        perishability_score: float,
        volunteer_available: bool,
        time_since_posted_minutes: int
    ) -> Dict[str, Any]:
        """
        Decide whether to assign volunteer driver or trigger courier fallback.
        
        Returns:
            {
                "assignment_type": "volunteer" or "courier",
                "reason": "explanation"
            }
        """
        if not self.model:
            # Fallback logic
            if not volunteer_available:
                return {
                    "assignment_type": "courier",
                    "reason": "No volunteers available"
                }
            
            if perishability_score > 8.0 and time_since_posted_minutes > 30:
                return {
                    "assignment_type": "courier",
                    "reason": "Highly perishable food, urgent pickup needed"
                }
            
            return {
                "assignment_type": "volunteer",
                "reason": "Volunteer assignment appropriate"
            }
        
        try:
            prompt = f"""You are a food rescue logistics coordinator. Decide driver assignment for food rescue:

- Perishability score: {perishability_score}/10
- Volunteer available: {volunteer_available}
- Time since posted: {time_since_posted_minutes} minutes

Return JSON format: {{"assignment_type": "volunteer" or "courier", "reason": "brief explanation"}}

Return only valid JSON, nothing else."""
            
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Simple JSON parsing
            if "courier" in result_text.lower():
                return {
                    "assignment_type": "courier",
                    "reason": "AI determined courier needed based on urgency"
                }
            else:
                return {
                    "assignment_type": "volunteer",
                    "reason": "AI determined volunteer assignment appropriate"
                }
        except Exception as e:
            print(f"AI assignment decision error: {e}")
            return {
                "assignment_type": "volunteer",
                "reason": "Default to volunteer"
            }
