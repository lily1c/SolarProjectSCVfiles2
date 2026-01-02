import requests
import csv
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 70)
print("🌍 NASA POWER API - Fetching Real Solar Data for Multiple Regions & Days")
print("=" * 70)

# ============================================================================
# STEP 1: 15 regions
# ============================================================================

regions = {
    'mount_vernon': {
        'name': 'Mount Vernon, OH',
        'latitude': 40.3934,
        'longitude': -82.4857,
        'description': 'Mild temperate'
    },
    'phoenix': {
        'name': 'Phoenix, AZ',
        'latitude': 33.4484,
        'longitude': -112.0740,
        'description': 'Hot desert'
    },
    'miami': {
        'name': 'Miami, FL',
        'latitude': 25.7617,
        'longitude': -80.1918,
        'description': 'Hot humid subtropical'
    },
    'riyadh': {
        'name': 'Riyadh, Saudi Arabia',
        'latitude': 24.7136,
        'longitude': 46.6753,
        'description': 'Extreme desert heat'
    },
    'seattle': {
        'name': 'Seattle, WA',
        'latitude': 47.6062,
        'longitude': -122.3321,
        'description': 'Cool marine, cloudy'
    },
    'las_vegas': {
        'name': 'Las Vegas, NV',
        'latitude': 36.1699,
        'longitude': -115.1398,
        'description': 'Hot arid desert'
    },
    'houston': {
        'name': 'Houston, TX',
        'latitude': 29.7604,
        'longitude': -95.3698,
        'description': 'Hot humid subtropical'
    },
    'denver': {
        'name': 'Denver, CO',
        'latitude': 39.7392,
        'longitude': -104.9903,
        'description': 'High altitude, dry'
    },
    'los_angeles': {
        'name': 'Los Angeles, CA',
        'latitude': 34.0522,
        'longitude': -118.2437,
        'description': 'Mediterranean climate'
    },
    'chicago': {
        'name': 'Chicago, IL',
        'latitude': 41.8781,
        'longitude': -87.6298,
        'description': 'Continental humid'
    },
        
    'el_paso': {
        'name': 'El Paso, TX',
        'latitude': 31.7619,
        'longitude': -106.4850,
        'description': 'Hot and dry desert climate near Mexico border'
    },
    'fresno': {
        'name': 'Fresno, CA',
        'latitude': 36.7378,
        'longitude': -119.7871,
        'description': 'Hot dry valley region with long summers'
    },
    'tucson': {
        'name': 'Tucson, AZ',
        'latitude': 32.2226,
        'longitude': -110.9747,
        'description': 'Extremely hot desert with high solar irradiance'
    },
    'palm_springs': {
        'name': 'Palm Springs, CA',
        'latitude': 33.8303,
        'longitude': -116.5453,
        'description': 'High solar radiation, desert resort area'
    },
    'las_cruces': {
        'name': 'Las Cruces, NM',
        'latitude': 32.3199,
        'longitude': -106.7637,
        'description': 'Hot arid desert region with strong sunlight'
    }

}

# ============================================================================
# STEP 2: get the datat range 
# ============================================================================

# Fetch 30 days of summer data (June 2022)
start_date = '20220601'
end_date = '20220630'

print(f"\n📅 Date range: {start_date} to {end_date} (30 days)")
print(f"📍 Regions: {len(regions)}")
print(f"📊 Expected samples: {len(regions)} regions × 30 days × 24 hours = {len(regions) * 30 * 24} samples\n")

# Output directory
output_dir = '/Users/assolabasova/Downloads/SolarProjectSCVfiles'
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# STEP 3: Fetch data from NASA POWER API for each region
# ============================================================================

all_regions_data = []
fetch_count = 0
total_fetches = len(regions)

for region_key, region_info in regions.items():
    fetch_count += 1
    print(f"🌐 [{fetch_count}/{total_fetches}] Fetching data for {region_info['name']}...")
    print(f"   Coordinates: ({region_info['latitude']}, {region_info['longitude']})")
    
    # NASA POWER API endpoint - Using date range
    api_url = (
        f"https://power.larc.nasa.gov/api/temporal/hourly/point"
        f"?parameters=ALLSKY_SFC_SW_DWN,T2M"
        f"&community=RE"
        f"&longitude={region_info['longitude']}"
        f"&latitude={region_info['latitude']}"
        f"&start={start_date}"
        f"&end={end_date}"
        f"&format=JSON"
        f"&time-standard=LST"
    )
    
    try:
        # Make the API request
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract hourly data
        irradiance_data = data['properties']['parameter']['ALLSKY_SFC_SW_DWN']
        temperature_data = data['properties']['parameter']['T2M']
        
        records_count = 0
        
        # Process hourly data
        for hour_str in sorted(irradiance_data.keys()):
            hour = int(hour_str)
            irradiance = irradiance_data[hour_str]
            temperature = temperature_data.get(hour_str, None)
            
            # Skip if data is missing
            if irradiance is None or temperature is None:
                continue
            
            all_regions_data.append({
                'Hour': hour,
                'Irradiance_Wm2': irradiance,
                'AmbientTemp_C': temperature,
                'Region': region_key
            })
            records_count += 1
        
        print(f"   ✅ Successfully fetched {records_count} hours of data\n")
        
    except requests.exceptions.Timeout:
        print(f"   ⚠️ Request timeout - try again later\n")
        continue
    except Exception as e:
        print(f"   ❌ Error fetching data: {e}\n")
        continue

print(f"✅ Total records fetched: {len(all_regions_data)}\n")

# ============================================================================
# STEP 4: Save individual CSV files for each region
# ============================================================================

print("💾 Saving individual region CSV files...\n")

for region_key in regions.keys():
    region_data = [d for d in all_regions_data if d['Region'] == region_key]
    
    if region_data:
        output_file = os.path.join(output_dir, f'{region_key}_data.csv')
        
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Hour', 'Irradiance_Wm2', 'AmbientTemp_C'])
            
            for row in region_data:
                writer.writerow([row['Hour'], row['Irradiance_Wm2'], row['AmbientTemp_C']])
        
        print(f"   ✅ {region_key}_data.csv ({len(region_data)} rows)")

# ============================================================================
# STEP 5: Calculate ML features and labels
# ============================================================================

print("\n🤖 Calculating ML features and labels...\n")

# Solar panel constants (FSP-100M from datasheet + paper specs)
A_panel = 0.63 * 0.45  # Panel area (m²) = 0.2835 m²
eta_ref = 0.18         # Reference efficiency at 25°C (18%)
beta = 0.005           # Temperature coefficient (0.5%/°C)
NOCT = 45              # Nominal Operating Cell Temperature (°C)
T_threshold = 43       # Cooling activates above 48°C (from paper!)
T_target = 35          # Cool to 38°C (from paper!)


# PUMP SPECIFICATIONS FROM PAPER (Table 2)
pump_power_rated = 2  # W 
pump_flow_rate = 25    # L/min (3000 L/H = 50 L/min, but effective is 25 L/min)
pump_efficiency = 0.85 # Typical submersible pump efficiency
min_runtime = 6        # Minutes (from paper: cooling takes 6 min)

# Actual pump power consumption (accounting for inefficiency)
pump_power_Wh = pump_power_rated / pump_efficiency  # 2 / 0.85 = 

print(f"📋 Panel Specifications:")
print(f"   Panel Area: {A_panel:.3f} m²")
print(f"   Reference Efficiency: {eta_ref*100:.1f}%")
print(f"   Temperature Coefficient: {beta*100:.2f}%/°C")
print(f"   NOCT: {NOCT}°C")
print(f"   Cooling Threshold: {T_threshold}°C (from paper)")
print(f"   Target Temperature: {T_target}°C (from paper)")
print(f"\n🔧 Pump Specifications (from paper Table 2):")
print(f"   Rated Power: {pump_power_rated}W")
print(f"   Flow Rate: {pump_flow_rate} L/min")
print(f"   Efficiency: {pump_efficiency*100:.0f}%")
print(f"   Actual Power Draw: {pump_power_Wh:.1f}W")
print(f"   Minimum Runtime: {min_runtime} minutes\n")

# Calculate features for ML training
training_data = []
cooling_stats = {key: 0 for key in regions.keys()}

# Set random seed for reproducibility
np.random.seed(42)

for idx, row in enumerate(all_regions_data):
    G = row['Irradiance_Wm2']
    T_amb = row['AmbientTemp_C']
    hour = row['Hour'] % 100  # Extract hour of day
    region = row['Region']
    
    # ========================================================================
    # ADD REALISTIC SENSOR NOISE (simulates real-world measurements)
    # ========================================================================
    
    # Irradiance sensor: ±15 W/m² accuracy (pyranometer typical error)
    G_measured = G + np.random.normal(0, 15)
    G_measured = max(0, G_measured)  # Can't be negative
    
    # Temperature sensor: ±0.5°C accuracy (typical thermocouple)
    T_amb_measured = T_amb + np.random.normal(0, 0.5)
    
    # Calculate panel temperature using Equation (1) from paper
    # T_m = T_amb + (NOCT - 20) * E / 800
    panel_temp = T_amb_measured + ((NOCT - 20) / 800) * G_measured
    
    # Panel temp sensor: ±2°C accuracy (IR sensor typical error)
    panel_temp_measured = panel_temp + np.random.normal(0, 2)
    
    # Add natural wind cooling effect (0-5 m/s typical)
    wind_speed = np.random.uniform(0, 5)
    wind_cooling = wind_speed * 0.3  # °C reduction
    panel_temp_measured = panel_temp_measured - wind_cooling
    
    # ========================================================================
    # ADD THRESHOLD VARIABILITY (not exactly 48°C due to hysteresis)
    # ========================================================================
    T_threshold_actual = np.random.uniform(46, 50)  # ±2°C hysteresis
    T_target_actual = np.random.uniform(36, 40)     # Target varies too
    
    # Initialize values
    energy_gain = 0
    cooling_cost = 0
    should_cool = 0
    cooling_cost_instantaneous = 0

    # Check if cooling is needed (only when there's meaningful irradiance)
    if panel_temp_measured > T_threshold_actual and G_measured > 100:
        # Efficiency without cooling
        eta_unc = max(eta_ref * (1 - beta * (panel_temp_measured - 25)), 0)
        P_unc = eta_unc * G_measured * A_panel
        
        # Efficiency with cooling
        eta_cool = max(eta_ref * (1 - beta * (T_target_actual - 25)), 0)
        P_cool = eta_cool * G_measured * A_panel
        
        # Energy gain from cooling (W)
        energy_gain = P_cool - P_unc
        
        # Cooling cost: pump must run for minimum 6 minutes
        # So cost is: pump_power * (min_runtime / 60 hours)
        cooling_cost = pump_power_Wh * (min_runtime / 60)  # Convert to Wh
        
        # But we also need immediate power for decision
        # Use instantaneous power comparison
        cooling_cost_instantaneous = pump_power_Wh
        
        # Decision: Cool if energy gain > pump power consumption
        # Add 20% margin for economic viability
        if energy_gain > cooling_cost_instantaneous * 1.2:
            should_cool = 1
            cooling_stats[region] += 1
    
    # ========================================================================
    # ADD DECISION NOISE (pump/control system isn't perfect)
    # ========================================================================
    
    # 3% chance of false positive (pump starts when it shouldn't)
    if should_cool == 0 and np.random.random() < 0.03:
        should_cool = 1
        cooling_stats[region] += 1
    
    # 5% chance of false negative (pump fails to start when it should)
    elif should_cool == 1 and np.random.random() < 0.05:
        should_cool = 0
        cooling_stats[region] -= 1
    
    training_data.append({
        'Hour': row['Hour'],
        'Irradiance_Wm2': round(G_measured, 2),
        'AmbientTemp_C': round(T_amb_measured, 2),
        'region': region,
        'hour': hour,
        'panel_temp': round(panel_temp_measured, 2),
        'energy_gain': round(energy_gain, 3),
        'cooling_cost': round(cooling_cost_instantaneous, 3),
        'should_cool': should_cool
    })

# ============================================================================
# STEP 6: Save complete training dataset
# ============================================================================

print("💾 Saving complete training dataset...\n")

# Convert to DataFrame
df_training = pd.DataFrame(training_data)

# Save to CSV
training_file = os.path.join(output_dir, 'full_training_data.csv')
df_training.to_csv(training_file, index=False)

print(f"   ✅ full_training_data.csv ({len(training_data)} rows)")

# ============================================================================
# STEP 7: Display summary statistics
# ============================================================================

print("\n" + "=" * 70)
print("📊 SUMMARY STATISTICS")
print("=" * 70 + "\n")

total_cool = sum(cooling_stats.values())
print(f"Total samples: {len(training_data)}")
print(f"Should cool (label=1): {total_cool} ({total_cool/len(training_data)*100:.1f}%)")
print(f"No cooling (label=0): {len(training_data) - total_cool} ({(len(training_data)-total_cool)/len(training_data)*100:.1f}%)\n")

print("Cooling beneficial hours by region:")
for region_key, count in cooling_stats.items():
    total_hours = len([d for d in training_data if d['region'] == region_key])
    print(f"   {regions[region_key]['name']}: {count}/{total_hours} hours ({count/total_hours*100:.1f}%)")

# Calculate class balance
print(f"\n⚖️ Class Balance:")
cool_ratio = total_cool / len(training_data)
if cool_ratio < 0.1 or cool_ratio > 0.9:
    print(f"   ⚠️ WARNING: Imbalanced dataset ({cool_ratio*100:.1f}% positive class)")
    print(f"   Consider adjusting T_threshold or pump power parameters")
else:
    print(f"   ✅ Good balance: {cool_ratio*100:.1f}% positive class")

# Additional statistics
df_cool = df_training[df_training['should_cool'] == 1]
if len(df_cool) > 0:
    print(f"\n📈 When Cooling is Beneficial:")
    print(f"   Avg panel temp: {df_cool['panel_temp'].mean():.1f}°C")
    print(f"   Avg irradiance: {df_cool['Irradiance_Wm2'].mean():.1f} W/m²")
    print(f"   Avg energy gain: {df_cool['energy_gain'].mean():.2f} W")
    print(f"   Max energy gain: {df_cool['energy_gain'].max():.2f} W")
    print(f"   Pump power cost: {pump_power_Wh:.1f} W (constant)")

print("\n" + "=" * 70)
print("✅ ALL FILES SAVED TO:")
print(f"   {output_dir}")
print("=" * 70)

print("\nFiles created:")
for i, region_key in enumerate(regions.keys(), 1):
    print(f"   {i}. {region_key}_data.csv")
print(f"   {len(regions)+1}. full_training_data.csv (with ML labels)")
print(f"\n🚀 Ready for ML training with {len(training_data)} samples!")
print(f"\n💡 NOTE: Using REALISTIC 24W pump (not 3W) with sensor noise added!")