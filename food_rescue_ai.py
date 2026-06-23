"""
Food Rescue AI System
Takes donor information and suggests nearest NGO with pickup priority
"""

import math
from datetime import datetime
from typing import List, Dict, Tuple

class NGO:
    """Represents an NGO with location and capacity"""
    def __init__(self, name: str, latitude: float, longitude: float, 
                 capacity_kg: float, current_load_kg: float = 0):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.capacity_kg = capacity_kg
        self.current_load_kg = current_load_kg
    
    def available_capacity(self) -> float:
        """Returns available capacity in kg"""
        return self.capacity_kg - self.current_load_kg
    
    def capacity_percentage(self) -> float:
        """Returns current capacity usage as percentage"""
        return (self.current_load_kg / self.capacity_kg) * 100 if self.capacity_kg > 0 else 0


class FoodRescueAI:
    """Main AI system for food rescue operations"""
    
    def __init__(self):
        # Sample NGO database (in real system, this would be from a database)
        self.ngos = [
            NGO("Hope Foundation", 28.6139, 77.2090, capacity_kg=500, current_load_kg=200),
            NGO("Food Bank Delhi", 28.7041, 77.1025, capacity_kg=800, current_load_kg=600),
            NGO("Helping Hands", 28.5355, 77.3910, capacity_kg=600, current_load_kg=100),
            NGO("Care & Share", 28.4595, 77.0266, capacity_kg=400, current_load_kg=350),
            NGO("Meal Mission", 28.6692, 77.4538, capacity_kg=700, current_load_kg=150),
        ]
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)
    
    def calculate_priority_score(self, distance: float, food_quantity: float, 
                                 ngo: NGO) -> float:
        """
        Calculate pickup priority score based on multiple factors
        Lower score = Higher priority
        
        Factors:
        - Distance (closer is better)
        - Food quantity vs NGO capacity
        - NGO current load (less loaded NGOs get priority)
        """
        # Distance factor (normalized, max 50 points)
        distance_score = min(distance * 2, 50)
        
        # Capacity match factor (0-30 points)
        available = ngo.available_capacity()
        if available < food_quantity:
            capacity_score = 30  # Penalize if can't handle full quantity
        else:
            # Reward NGOs with appropriate capacity
            capacity_usage = ngo.capacity_percentage()
            if capacity_usage < 30:
                capacity_score = 10  # Good availability
            elif capacity_usage < 60:
                capacity_score = 5   # Optimal
            else:
                capacity_score = 15  # Getting full
        
        # Load factor (0-20 points) - prefer less loaded NGOs
        load_score = (ngo.capacity_percentage() / 100) * 20
        
        total_score = distance_score + capacity_score + load_score
        return round(total_score, 2)
    
    def determine_urgency(self, food_quantity: float) -> str:
        """Determine pickup urgency based on food quantity"""
        if food_quantity >= 100:
            return "HIGH"
        elif food_quantity >= 50:
            return "MEDIUM"
        else:
            return "LOW"
    
    def suggest_ngo(self, donor_name: str, food_quantity: float, 
                   latitude: float, longitude: float) -> Dict:
        """
        Main function to suggest nearest NGO with pickup priority
        
        Args:
            donor_name: Name of the donor
            food_quantity: Amount of food in kg
            latitude: Donor's latitude
            longitude: Donor's longitude
        
        Returns:
            Dictionary with suggestion details
        """
        if food_quantity <= 0:
            return {
                "status": "error",
                "message": "Food quantity must be greater than 0"
            }
        
        # Calculate distances and priority scores for all NGOs
        ngo_rankings = []
        
        for ngo in self.ngos:
            distance = self.calculate_distance(latitude, longitude, 
                                              ngo.latitude, ngo.longitude)
            priority_score = self.calculate_priority_score(distance, food_quantity, ngo)
            
            ngo_rankings.append({
                "ngo": ngo,
                "distance_km": distance,
                "priority_score": priority_score,
                "available_capacity_kg": ngo.available_capacity(),
                "can_handle_full_quantity": ngo.available_capacity() >= food_quantity
            })
        
        # Sort by priority score (lower is better)
        ngo_rankings.sort(key=lambda x: x["priority_score"])
        
        # Get best match
        best_match = ngo_rankings[0]
        urgency = self.determine_urgency(food_quantity)
        
        # Prepare result
        result = {
            "status": "success",
            "donor_info": {
                "name": donor_name,
                "food_quantity_kg": food_quantity,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude
                }
            },
            "recommended_ngo": {
                "name": best_match["ngo"].name,
                "distance_km": best_match["distance_km"],
                "available_capacity_kg": best_match["available_capacity_kg"],
                "can_handle_full_quantity": best_match["can_handle_full_quantity"],
                "contact_priority": urgency
            },
            "pickup_priority": urgency,
            "priority_score": best_match["priority_score"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alternative_ngos": [
                {
                    "name": alt["ngo"].name,
                    "distance_km": alt["distance_km"],
                    "available_capacity_kg": alt["available_capacity_kg"]
                }
                for alt in ngo_rankings[1:3]  # Top 2 alternatives
            ]
        }
        
        return result


def main():
    """Main function to run the Food Rescue AI system"""
    print("=" * 60)
    print("FOOD RESCUE AI SYSTEM")
    print("=" * 60)
    print()
    
    # Initialize the AI system
    ai = FoodRescueAI()
    
    # Get donor information
    try:
        donor_name = input("Enter Donor Name: ").strip()
        if not donor_name:
            print("Error: Donor name cannot be empty!")
            return
        
        food_quantity = float(input("Enter Food Quantity (in kg): "))
        if food_quantity <= 0:
            print("Error: Food quantity must be greater than 0!")
            return
        
        print("\nEnter Donor Location:")
        latitude = float(input("  Latitude: "))
        longitude = float(input("  Longitude: "))
        
        # Validate coordinates
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
            print("Error: Invalid coordinates!")
            return
        
        print("\n" + "=" * 60)
        print("PROCESSING REQUEST...")
        print("=" * 60)
        
        # Get suggestion
        result = ai.suggest_ngo(donor_name, food_quantity, latitude, longitude)
        
        if result["status"] == "error":
            print(f"\nError: {result['message']}")
            return
        
        # Display results
        print("\n" + "=" * 60)
        print("RECOMMENDATION RESULT")
        print("=" * 60)
        
        print(f"\nDonor: {result['donor_info']['name']}")
        print(f"Food Quantity: {result['donor_info']['food_quantity_kg']} kg")
        print(f"Pickup Priority: {result['pickup_priority']}")
        print(f"Timestamp: {result['timestamp']}")
        
        print("\n" + "-" * 60)
        print("RECOMMENDED NGO")
        print("-" * 60)
        
        ngo = result['recommended_ngo']
        print(f"NGO Name: {ngo['name']}")
        print(f"Distance: {ngo['distance_km']} km")
        print(f"Available Capacity: {ngo['available_capacity_kg']} kg")
        print(f"Can Handle Full Quantity: {'Yes' if ngo['can_handle_full_quantity'] else 'No'}")
        print(f"Contact Priority: {ngo['contact_priority']}")
        print(f"Priority Score: {result['priority_score']} (lower is better)")
        
        print("\n" + "-" * 60)
        print("ALTERNATIVE NGOs")
        print("-" * 60)
        
        for i, alt in enumerate(result['alternative_ngos'], 1):
            print(f"\n{i}. {alt['name']}")
            print(f"   Distance: {alt['distance_km']} km")
            print(f"   Available Capacity: {alt['available_capacity_kg']} kg")
        
        print("\n" + "=" * 60)
        
    except ValueError as e:
        print(f"\nError: Invalid input! Please enter numeric values for quantity and coordinates.")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")


if __name__ == "__main__":
    main()

# Made with Bob
