import numpy as np
from flask import jsonify
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import re

# Load Data Frame to retrive random record with the predicted planet type
df=pd.read_csv("Scientific_Info.csv") 

# Load trained model
model = joblib.load(r'C:\Users\IShop\Documents\AI NASA\Saved_Model\XGBoost_model.joblib')



# Constants for conversions
JUPITER_TO_EARTH_MASS = 317.8
JUPITER_TO_EARTH_RADIUS = 11.2

# Parsing function
def parse_value(value_str):
    """Parses a value like '12.47 Jupiters' or '1.13 x Earth' into numerical value and planet."""
    pattern = r'([\d.]+)\s*(x\s*)?(Jupiters|Jupiter|Earths|Earth)'
    match = re.match(pattern, value_str)
    
    if match:
        value = float(match.group(1))
        unit = match.group(3).lower()
        return value, unit
    return None, None

# Conversion function
def convert_to_earth_units(mass_str, radius_str):
    """Converts mass and radius to Earth units."""
    mass_value, mass_unit = parse_value(mass_str)
    radius_value, radius_unit = parse_value(radius_str)
    
    # Convert mass to Earth units
    if mass_unit == 'jupiters' or mass_unit == 'jupiter':
        mass_in_earths = mass_value * JUPITER_TO_EARTH_MASS
    elif mass_unit == 'earths' or mass_unit == 'earth':
        mass_in_earths = mass_value
    
    # Convert radius to Earth units
    if radius_unit == 'jupiters' or radius_unit == 'jupiter':
        radius_in_earths = radius_value * JUPITER_TO_EARTH_RADIUS
    elif radius_unit == 'earths' or radius_unit == 'earth':
        radius_in_earths = radius_value
    
    return mass_in_earths, radius_in_earths

# Visualization function
def compare_exoplanet(mass_str, radius_str):
    # Constants for Earth and Jupiter (in Earth units)
    earth_mass = 1  # Earth's mass
    jupiter_mass = JUPITER_TO_EARTH_MASS  # Jupiter's mass in Earth units
    earth_radius = 1  # Earth's radius
    jupiter_radius = JUPITER_TO_EARTH_RADIUS  # Jupiter's radius in Earth units
    
    # Convert the exoplanet's mass and radius to Earth units
    planet_mass, planet_radius = convert_to_earth_units(mass_str, radius_str)
    
    # Data for comparison
    masses = [earth_mass, jupiter_mass, planet_mass]
    radii = [earth_radius, jupiter_radius, planet_radius]
    labels = ['Earth', 'Jupiter', 'Exoplanet']
    
    # Plot mass comparison
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(labels, masses, color=['blue', 'orange', 'green'])
    plt.title('Mass Comparison')
    plt.ylabel('Mass (in Earth units)')
    
    # Plot radius comparison
    plt.subplot(1, 2, 2)
    plt.bar(labels, radii, color=['blue', 'orange', 'green'])
    plt.title('Radius Comparison')
    plt.ylabel('Radius (in Earth units)')
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Prediction function with random record retrieval
def predict(data):
    # Assume response_mapping and model have been defined
    response_mapping = {
        
        'Nearby': 0, 'Intermediate': 1, 'Distant': 2, 
        
        'Small_planet_mass':0,'Large_planet_mass':1,
        
        'Low_host_radius':0,'Medium_host_radius':1, 'Large_host_radius':2,
        
        'Low_host_mass':0,'Medium_host_mass':1, 'Large_host_mass':2,
    
        'Low_eccentricity':0,'High_eccentricity':1,
        
        'Low_stellar_magnitude':0,'High_stellar_magnitude':1,
    
        'Cool': 0, 'Warm': 1, 'Hot': 2,
    
        'Sub-Neptune':0,'Super-Jovian':1, 'Mega-Earth':2, 'Mini-Neptune':3, 
        'Neptune-class':4, 'Jovian':5, 'Earth-like':6, 'Mini-Earth':7, 'Sub-Jovian':8, 
        'Super-Earth':9

    }
    # Mapping user responses to numerical features
    features = [response_mapping[answer] for answer in data['responses']]
    
    # Predict using the model
    prediction = model.predict([features])[0]
    
    # Mapping predicted numerical values to planet types
    planet_type_mapping = {
        0: 'Neptune-like',
        1: 'Gas Giant',
        2: 'Super Earth',
        3: 'Terrestrial'
    }
    
    predicted_planet_type = planet_type_mapping[prediction]
    
    # Search the DataFrame for records that match the predicted planet type
    filtered_df = df[df['planet_type'] == predicted_planet_type]
    
    if not filtered_df.empty:
        # Select a random record from the filtered DataFrame
        random_record = filtered_df.sample(1).to_dict(orient='records')[0]
    else:
        random_record = {"message": "No records found for the predicted planet type"}

    # Extract mass and radius from random_record
    mass_input = random_record.get('planet_mass', "1 Earths")
    radius_input = random_record.get('planet_radius', "1 Earths")
    
    # Call the compare_exoplanet function to visualize the comparison
    compare_exoplanet(mass_input, radius_input)
    
    # Return the prediction and a random record as JSON
    return jsonify({
        'predicted_planet_type': predicted_planet_type,
        'random_record': random_record['name']
    })