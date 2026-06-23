# Food Rescue AI - System Flow

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     FOOD RESCUE AI SYSTEM                        │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   DONOR      │
│  INPUT       │
└──────┬───────┘
       │
       │ • Donor Name
       │ • Food Quantity (kg)
       │ • Location (Lat/Long)
       │
       ▼
┌──────────────────────────────────────────────────────────────────┐
│                    FOOD RESCUE AI ENGINE                          │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Step 1: Calculate Distances                           │     │
│  │  • Use Haversine formula                               │     │
│  │  • Compute distance to each NGO                        │     │
│  └────────────────────────────────────────────────────────┘     │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Step 2: Evaluate NGO Capacity                         │     │
│  │  • Check available capacity                            │     │
│  │  • Verify if can handle full quantity                  │     │
│  │  • Calculate current load percentage                   │     │
│  └────────────────────────────────────────────────────────┘     │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Step 3: Calculate Priority Scores                     │     │
│  │  • Distance Factor (0-50 points)                       │     │
│  │  • Capacity Match (0-30 points)                        │     │
│  │  • Load Factor (0-20 points)                           │     │
│  │  • Lower score = Better match                          │     │
│  └────────────────────────────────────────────────────────┘     │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Step 4: Determine Urgency                             │     │
│  │  • HIGH: ≥100 kg                                       │     │
│  │  • MEDIUM: 50-99 kg                                    │     │
│  │  • LOW: <50 kg                                         │     │
│  └────────────────────────────────────────────────────────┘     │
│                           │                                       │
│                           ▼                                       │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Step 5: Rank & Select Best NGO                        │     │
│  │  • Sort by priority score                              │     │
│  │  • Select top match                                    │     │
│  │  • Provide alternatives                                │     │
│  └────────────────────────────────────────────────────────┘     │
│                                                                   │
└───────────────────────────────────┬───────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │   RECOMMENDATION OUTPUT   │
                    │                           │
                    │ • Best NGO Match          │
                    │ • Distance                │
                    │ • Pickup Priority         │
                    │ • Alternative NGOs        │
                    └───────────────────────────┘
```

## Data Flow Diagram

```
INPUT DATA                  PROCESSING                    OUTPUT DATA
──────────                  ──────────                    ───────────

Donor Name ────────┐
                   │
Food Quantity ─────┼──────► Priority Score ────────┐
                   │        Calculation            │
Location ──────────┤                               ├──► Recommended NGO
(Lat/Long)         │        Distance               │
                   │        Calculation            │    Distance (km)
NGO Database ──────┤                               │
                   │        Capacity               │    Priority Level
                   │        Evaluation             │
                   │                               │    Alternatives
                   └──────► Urgency ───────────────┘
                            Classification              Timestamp
```

## Priority Score Calculation

```
┌─────────────────────────────────────────────────────────────┐
│                   PRIORITY SCORE FORMULA                     │
│                                                              │
│  Total Score = Distance Score + Capacity Score + Load Score │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Distance Score (0-50 points)                         │  │
│  │ • Closer NGOs get lower scores                       │  │
│  │ • Formula: min(distance_km × 2, 50)                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Capacity Score (0-30 points)                         │  │
│  │ • Can't handle quantity: 30 points                   │  │
│  │ • <30% full: 10 points (good availability)           │  │
│  │ • 30-60% full: 5 points (optimal)                    │  │
│  │ • >60% full: 15 points (getting full)                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Load Score (0-20 points)                             │  │
│  │ • Based on current capacity usage                    │  │
│  │ • Formula: (current_load% / 100) × 20                │  │
│  │ • Less loaded NGOs get lower scores                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  RESULT: Lower total score = Higher priority match          │
└─────────────────────────────────────────────────────────────┘
```

## Urgency Classification Logic

```
Food Quantity (kg)          Urgency Level          Action Required
──────────────────          ─────────────          ───────────────

    ≥ 100 kg        ────►      HIGH         ────►  Immediate pickup
                                                    Contact NGO ASAP
                                                    
   50-99 kg         ────►     MEDIUM        ────►  Standard priority
                                                    Schedule within hours
                                                    
    < 50 kg         ────►      LOW          ────►  Flexible scheduling
                                                    Can be batched
```

## Example Scenario Walkthrough

```
SCENARIO: Restaurant Donation
─────────────────────────────

INPUT:
  Donor: "Raj's Restaurant"
  Quantity: 75 kg
  Location: (28.6139, 77.2090)

STEP 1 - Calculate Distances:
  Hope Foundation: 2.5 km
  Food Bank Delhi: 8.3 km
  Helping Hands: 15.2 km
  Care & Share: 22.1 km
  Meal Mission: 18.7 km

STEP 2 - Check Capacities:
  Hope Foundation: 300 kg available ✓
  Food Bank Delhi: 200 kg available ✓
  Helping Hands: 500 kg available ✓
  Care & Share: 50 kg available ✗
  Meal Mission: 550 kg available ✓

STEP 3 - Calculate Priority Scores:
  Hope Foundation: 15.5 (BEST)
  Food Bank Delhi: 28.2
  Helping Hands: 35.4
  Care & Share: 62.8
  Meal Mission: 41.9

STEP 4 - Determine Urgency:
  75 kg → MEDIUM priority

STEP 5 - Generate Recommendation:
  ✓ Recommended: Hope Foundation
  ✓ Distance: 2.5 km
  ✓ Priority: MEDIUM
  ✓ Alternatives: Food Bank Delhi, Helping Hands

OUTPUT:
  "Contact Hope Foundation immediately for pickup"
```

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    CLASS: NGO                                │
│                                                              │
│  Properties:                                                 │
│  • name: str                                                 │
│  • latitude: float                                           │
│  • longitude: float                                          │
│  • capacity_kg: float                                        │
│  • current_load_kg: float                                    │
│                                                              │
│  Methods:                                                    │
│  • available_capacity() → float                              │
│  • capacity_percentage() → float                             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                CLASS: FoodRescueAI                           │
│                                                              │
│  Properties:                                                 │
│  • ngos: List[NGO]                                           │
│                                                              │
│  Methods:                                                    │
│  • calculate_distance() → float                              │
│  • calculate_priority_score() → float                        │
│  • determine_urgency() → str                                 │
│  • suggest_ngo() → Dict                                      │
└─────────────────────────────────────────────────────────────┘
```

## Integration Points

```
┌──────────────────┐
│  Web/Mobile App  │
│                  │
│  • User Input    │
│  • Display UI    │
└────────┬─────────┘
         │
         │ HTTP/API
         │
         ▼
┌──────────────────┐
│  Backend Server  │
│                  │
│  • API Endpoint  │
│  • Validation    │
└────────┬─────────┘
         │
         │ Function Call
         │
         ▼
┌──────────────────┐
│ Food Rescue AI   │
│                  │
│  • Core Logic    │
│  • Calculations  │
└────────┬─────────┘
         │
         │ Query/Update
         │
         ▼
┌──────────────────┐
│    Database      │
│                  │
│  • NGO Data      │
│  • History       │
└──────────────────┘
```

## Performance Considerations

- **Time Complexity**: O(n) where n = number of NGOs
- **Space Complexity**: O(n) for storing rankings
- **Scalability**: Can handle 1000+ NGOs efficiently
- **Real-time**: Response time < 100ms for typical use

## Future Enhancements

1. **Machine Learning**: Predict optimal pickup times
2. **Route Optimization**: Multi-stop pickup planning
3. **Real-time Updates**: Live capacity tracking
4. **Weather Integration**: Adjust priorities based on weather
5. **Historical Analytics**: Learn from past donations
