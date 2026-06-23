"""
Example usage of the Food Rescue AI System
This demonstrates how to use the system programmatically
"""

from food_rescue_ai import FoodRescueAI
import json

def example_1():
    """Example 1: Restaurant donation"""
    print("=" * 70)
    print("EXAMPLE 1: Restaurant Donation")
    print("=" * 70)
    
    ai = FoodRescueAI()
    
    # Donor details
    donor_name = "Raj's Restaurant"
    food_quantity = 75  # kg
    latitude = 28.6139
    longitude = 77.2090
    
    print(f"\nDonor: {donor_name}")
    print(f"Food Quantity: {food_quantity} kg")
    print(f"Location: ({latitude}, {longitude})")
    
    # Get recommendation
    result = ai.suggest_ngo(donor_name, food_quantity, latitude, longitude)
    
    # Display result
    print("\n" + "-" * 70)
    print("RECOMMENDATION:")
    print("-" * 70)
    print(f"Recommended NGO: {result['recommended_ngo']['name']}")
    print(f"Distance: {result['recommended_ngo']['distance_km']} km")
    print(f"Pickup Priority: {result['pickup_priority']}")
    print(f"Priority Score: {result['priority_score']}")
    print()


def example_2():
    """Example 2: Large event surplus"""
    print("=" * 70)
    print("EXAMPLE 2: Large Event Surplus")
    print("=" * 70)
    
    ai = FoodRescueAI()
    
    # Donor details
    donor_name = "Wedding Hall - Grand Palace"
    food_quantity = 150  # kg (HIGH priority)
    latitude = 28.5355
    longitude = 77.3910
    
    print(f"\nDonor: {donor_name}")
    print(f"Food Quantity: {food_quantity} kg")
    print(f"Location: ({latitude}, {longitude})")
    
    # Get recommendation
    result = ai.suggest_ngo(donor_name, food_quantity, latitude, longitude)
    
    # Display result
    print("\n" + "-" * 70)
    print("RECOMMENDATION:")
    print("-" * 70)
    print(f"Recommended NGO: {result['recommended_ngo']['name']}")
    print(f"Distance: {result['recommended_ngo']['distance_km']} km")
    print(f"Pickup Priority: {result['pickup_priority']} ⚠️")
    print(f"Can Handle Full Quantity: {result['recommended_ngo']['can_handle_full_quantity']}")
    
    print("\nAlternative NGOs:")
    for i, alt in enumerate(result['alternative_ngos'], 1):
        print(f"  {i}. {alt['name']} - {alt['distance_km']} km")
    print()


def example_3():
    """Example 3: Small donation"""
    print("=" * 70)
    print("EXAMPLE 3: Small Donation")
    print("=" * 70)
    
    ai = FoodRescueAI()
    
    # Donor details
    donor_name = "Home Kitchen - Sharma Family"
    food_quantity = 25  # kg (LOW priority)
    latitude = 28.7041
    longitude = 77.1025
    
    print(f"\nDonor: {donor_name}")
    print(f"Food Quantity: {food_quantity} kg")
    print(f"Location: ({latitude}, {longitude})")
    
    # Get recommendation
    result = ai.suggest_ngo(donor_name, food_quantity, latitude, longitude)
    
    # Display result
    print("\n" + "-" * 70)
    print("RECOMMENDATION:")
    print("-" * 70)
    print(f"Recommended NGO: {result['recommended_ngo']['name']}")
    print(f"Distance: {result['recommended_ngo']['distance_km']} km")
    print(f"Pickup Priority: {result['pickup_priority']}")
    print(f"Available Capacity: {result['recommended_ngo']['available_capacity_kg']} kg")
    print()


def example_4_json_output():
    """Example 4: Getting JSON output for API integration"""
    print("=" * 70)
    print("EXAMPLE 4: JSON Output (for API integration)")
    print("=" * 70)
    
    ai = FoodRescueAI()
    
    # Donor details
    donor_name = "Corporate Cafeteria - Tech Corp"
    food_quantity = 90  # kg
    latitude = 28.4595
    longitude = 77.0266
    
    # Get recommendation
    result = ai.suggest_ngo(donor_name, food_quantity, latitude, longitude)
    
    # Convert to JSON
    print("\nJSON Response:")
    print(json.dumps(result, indent=2))
    print()


def main():
    """Run all examples"""
    print("\n")
    print("*" * 70)
    print("FOOD RESCUE AI - EXAMPLE USAGE DEMONSTRATIONS")
    print("*" * 70)
    print("\n")
    
    example_1()
    input("Press Enter to continue to next example...")
    print("\n")
    
    example_2()
    input("Press Enter to continue to next example...")
    print("\n")
    
    example_3()
    input("Press Enter to continue to next example...")
    print("\n")
    
    example_4_json_output()
    
    print("*" * 70)
    print("All examples completed!")
    print("*" * 70)


if __name__ == "__main__":
    main()

# Made with Bob
