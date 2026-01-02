import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.utils import resample
import joblib

print("=" * 70)
print("🤖 SOLAR PANEL COOLING ML MODEL - 5 REGION TRAINING")
print("=" * 70)

# ============================================================================
# STEP 1: Load data from 10 regions
# ============================================================================
print("\n📂 Loading data from regions...")

files = {
    'mount_vernon': 'mount_vernon_data.csv',
    'phoenix': 'phoenix_data.csv',
    'miami': 'miami_data.csv',
    'riyadh': 'riyadh_data.csv',
    'seattle': 'seattle_data.csv',
    'el_paso': 'el_paso_data.csv',
    'fresno': 'fresno_data.csv',
    'tucson': 'tucson_data.csv',
    'palm_springs': 'palm_springs_data.csv',
    'las_cruces': 'las_cruces_data.csv'
}

data_list = []
for region, file in files.items():
    df = pd.read_csv(f'/Users/assolabasova/Downloads/SolarProjectSCVfiles/{file}')
    df['region'] = region
    data_list.append(df)

all_data = pd.concat(data_list, ignore_index=True)
all_data = all_data[all_data['Irradiance_Wm2'] > 600].copy()

print(f"✅ After filtering low-irradiance rows: {len(all_data)} records remain")

# ============================================================================
# STEP 2: Calculate panel temperature and cooling decision
# ============================================================================
print("\n🔧 Calculating features and labels...")

# Panel & pump constants
A_panel = 0.63 * 0.45
eta_ref = 0.18
beta = 0.005
NOCT = 45
T_threshold = 45
T_target = 35
pump_power_rated = 2
pump_efficiency = 0.85
pump_power_Wh = pump_power_rated / pump_efficiency
min_runtime = 6

np.random.seed(42)

# Extract hour
all_data['hour'] = all_data['Hour'] % 100

# Initialize columns
all_data['panel_temp'] = 0.0
all_data['energy_gain'] = 0.0
all_data['cooling_cost'] = 0.0
all_data['should_cool'] = 0

# Calculate realistic panel temp and cooling labels
for idx, row in all_data.iterrows():
    G = row['Irradiance_Wm2']
    T_amb = row['AmbientTemp_C']

    # Add sensor noise
    G_measured = max(0, G + np.random.normal(0, 15))
    T_amb_measured = T_amb + np.random.normal(0, 0.5)

    # Panel temp
    panel_temp = T_amb_measured + ((NOCT - 20) / 800) * G_measured
    panel_temp_measured = panel_temp + np.random.normal(0, 2)
    wind_cooling = np.random.uniform(0, 5) * 0.3
    panel_temp_measured -= wind_cooling
    all_data.at[idx, 'panel_temp'] = panel_temp_measured

    # Threshold variability (slightly lower for more positives)
    T_threshold_actual = np.random.uniform(44, 48)
    T_target_actual = np.random.uniform(36, 40)

    # Only consider cooling when hot and sunny
    if panel_temp_measured > T_threshold_actual and G_measured > 100:
        eta_unc = max(eta_ref * (1 - beta * (panel_temp_measured - 25)), 0)
        P_unc = eta_unc * G_measured * A_panel

        eta_cool = max(eta_ref * (1 - beta * (T_target_actual - 25)), 0)
        P_cool = eta_cool * G_measured * A_panel

        energy_gain = P_cool - P_unc
        cooling_cost = pump_power_Wh

        all_data.at[idx, 'energy_gain'] = energy_gain
        all_data.at[idx, 'cooling_cost'] = cooling_cost

        # Reduced margin for decision to increase positives
        if energy_gain > cooling_cost * 0.8:
            all_data.at[idx, 'should_cool'] = 1

# Add decision noise (3% false positives, 5% false negatives)
for idx in all_data.index:
    if all_data.at[idx, 'should_cool'] == 0 and np.random.random() < 0.03:
        all_data.at[idx, 'should_cool'] = 1
    elif all_data.at[idx, 'should_cool'] == 1 and np.random.random() < 0.05:
        all_data.at[idx, 'should_cool'] = 0

# ============================================================================
# STEP 2B: Upsample positive samples to balance classes
# ============================================================================
df_majority = all_data[all_data.should_cool == 0]
df_minority = all_data[all_data.should_cool == 1]

df_minority_upsampled = resample(
    df_minority,
    replace=True,
    n_samples=len(df_majority),
    random_state=42
)

all_data_balanced = pd.concat([df_majority, df_minority_upsampled])
print(f"\n📊 After upsampling: {all_data_balanced['should_cool'].value_counts().to_dict()}")

# ============================================================================
# STEP 3: Prepare features
# ============================================================================
feature_cols = ['AmbientTemp_C', 'Irradiance_Wm2', 'panel_temp', 'hour']
X = all_data_balanced[feature_cols]
y = all_data_balanced['should_cool']

# ============================================================================
# STEP 4: Train/test split
# ============================================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ============================================================================
# STEP 5: Train Random Forest
# ============================================================================
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)
model.fit(X_train, y_train)

# ============================================================================
# STEP 6: Evaluate
# ============================================================================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy:.2%}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['No Cooling', 'Should Cool']))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ============================================================================
# STEP 7: Save model
# ============================================================================
joblib.dump(model, 'cooling_decision_model.pkl')
print("\n✅ Model saved as: cooling_decision_model.pkl")
