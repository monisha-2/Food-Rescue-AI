# Quick Start Guide - Food Rescue AI

## Overview
This Food Rescue AI system helps match food donors with nearby NGOs based on location, food quantity, and NGO capacity.

## What You Need
- Python 3.6 or higher installed on your system

## Installation Check

### Check if Python is installed:
```bash
python --version
```
or
```bash
python3 --version
```

### If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Mac/Linux**: Usually pre-installed, or use package manager

## Running the System

### Method 1: Interactive Mode (Recommended for first-time users)

```bash
python food_rescue_ai.py
```

Then follow the prompts:
1. Enter donor name
2. Enter food quantity in kg
3. Enter location (latitude and longitude)

**Example Input:**
```
Enter Donor Name: Raj's Restaurant
Enter Food Quantity (in kg): 75
Enter Donor Location:
  Latitude: 28.6139
  Longitude: 77.2090
```

### Method 2: Programmatic Usage

Run the example demonstrations:
```bash
python example_usage.py
```

This will show 4 different scenarios:
1. Restaurant donation (medium quantity)
2. Large event surplus (high priority)
3. Small home donation (low priority)
4. JSON output for API integration

### Method 3: Import as Module

Create your own Python script:

```python
from food_rescue_ai import FoodRescueAI

# Initialize the system
ai = FoodRescueAI()

# Get recommendation
result = ai.suggest_ngo(
    donor_name="My Restaurant",
    food_quantity=50,  # kg
    latitude=28.6139,
    longitude=77.2090
)

# Use the result
print(f"Recommended NGO: {result['recommended_ngo']['name']}")
print(f"Distance: {result['recommended_ngo']['distance_km']} km")
print(f"Priority: {result['pickup_priority']}")
```

## Understanding the Output

### Pickup Priority Levels
- **HIGH**: ≥100 kg - Requires immediate attention
- **MEDIUM**: 50-99 kg - Standard priority
- **LOW**: <50 kg - Can be scheduled flexibly

### Priority Score
- Lower score = Better match
- Factors considered:
  - Distance to NGO
  - NGO capacity availability
  - Current NGO load

### Sample Output
```
RECOMMENDED NGO
----------------------------------------------------------------
NGO Name: Hope Foundation
Distance: 2.5 km
Available Capacity: 300 kg
Can Handle Full Quantity: Yes
Contact Priority: MEDIUM
Priority Score: 15.5 (lower is better)

ALTERNATIVE NGOs
----------------------------------------------------------------
1. Helping Hands
   Distance: 5.2 km
   Available Capacity: 500 kg
```

## Getting Location Coordinates

### Option 1: Google Maps
1. Right-click on your location in Google Maps
2. Click on the coordinates to copy them
3. Format: First number is latitude, second is longitude

### Option 2: GPS Device
Use any GPS-enabled device or smartphone app

### Option 3: Address to Coordinates
Use online geocoding services to convert addresses to coordinates

## Sample Locations (Delhi, India)

For testing purposes:
- **Connaught Place**: 28.6139, 77.2090
- **Dwarka**: 28.5921, 77.0460
- **Rohini**: 28.7041, 77.1025
- **Noida**: 28.5355, 77.3910
- **Gurgaon**: 28.4595, 77.0266

## Troubleshooting

### "Python not found"
- Install Python from python.org
- Make sure to check "Add Python to PATH" during installation

### "Module not found"
- Make sure you're in the correct directory
- All files should be in the same folder

### Invalid coordinates
- Latitude must be between -90 and 90
- Longitude must be between -180 and 180

## Next Steps

1. **Test the system** with sample data
2. **Customize NGO database** in `food_rescue_ai.py`
3. **Integrate with your application** using the module import method
4. **Add real-time updates** by connecting to a database

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review the example_usage.py for code samples
- Modify the NGO database to match your region

## Future Integration Ideas

- Mobile app for donors
- SMS notifications to NGOs
- Real-time capacity tracking
- Route optimization for pickup
- Analytics dashboard
- Multi-language support
