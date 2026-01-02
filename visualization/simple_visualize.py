"""
Simple Solar Cooling Visualizations
Generates 3 key figures from full_training_data.csv
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
print("Loading data...")
df = pd.read_csv('/Users/assolabasova/Downloads/SolarProjectSCVfiles/full_training_data.csv')
print(f"Loaded {len(df):,} samples from {df['region'].nunique()} regions")

# Region stats
region_stats = df.groupby('region').agg({
    'should_cool': 'mean',
    'panel_temp': 'mean',
    'energy_gain': 'mean'
}).reset_index()
region_stats['cooling_pct'] = region_stats['should_cool'] * 100
region_stats = region_stats.sort_values('cooling_pct', ascending=False)

# ============================================================================
# FIGURE 1: Regional Overview
# ============================================================================
print("\n[1/3] Creating regional overview...")
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Top: Bar chart of cooling benefit
ax = axes[0]
colors = plt.cm.RdYlGn(region_stats['cooling_pct'] / region_stats['cooling_pct'].max())
ax.barh(region_stats['region'], region_stats['cooling_pct'], color=colors)
ax.set_xlabel('Cooling Benefit (% of Hours)')
ax.set_title('Cooling Effectiveness by Region', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
for i, val in enumerate(region_stats['cooling_pct']):
    ax.text(val + 1, i, f'{val:.1f}%', va='center', fontsize=9)

# Bottom: Heatmap
ax = axes[1]
pivot = df.groupby(['region', 'hour'])['should_cool'].mean().unstack()
pivot = pivot.loc[region_stats['region']]
sns.heatmap(pivot, cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Cooling Probability'})
ax.set_xlabel('Hour of Day')
ax.set_ylabel('Region')
ax.set_title('Cooling Patterns: Region × Hour', fontweight='bold')

plt.tight_layout()
plt.savefig('01_regional_overview.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_regional_overview.png")
plt.close()

# ============================================================================
# FIGURE 2: Decision Analysis
# ============================================================================
print("[2/3] Creating decision analysis...")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# A) Pie chart
ax = axes[0, 0]
counts = df['should_cool'].value_counts()
ax.pie(counts, labels=['No Cooling', 'Cooling'], autopct='%1.1f%%',
       colors=['#d73027', '#1a9850'], startangle=90)
ax.set_title('Overall Distribution')

# B) Temperature by decision
ax = axes[0, 1]
no_cool = df[df['should_cool'] == 0]['panel_temp']
cool = df[df['should_cool'] == 1]['panel_temp']
ax.hist([no_cool, cool], bins=50, label=['No Cooling', 'Cooling'],
        color=['#d73027', '#1a9850'], alpha=0.7)
ax.axvline(45, color='black', linestyle='--', linewidth=2)
ax.set_xlabel('Panel Temperature (°C)')
ax.set_ylabel('Frequency')
ax.set_title('Temperature Distribution')
ax.legend()
ax.grid(alpha=0.3)

# C) Scatter plot
ax = axes[1, 0]
sample = df.sample(min(2000, len(df)))
scatter = ax.scatter(sample['Irradiance_Wm2'], sample['panel_temp'],
                    c=sample['should_cool'], cmap='RdYlGn_r', alpha=0.5, s=10)
ax.axhline(45, color='red', linestyle='--', alpha=0.7)
ax.axvline(600, color='blue', linestyle='--', alpha=0.7)
ax.set_xlabel('Irradiance (W/m²)')
ax.set_ylabel('Panel Temp (°C)')
ax.set_title('Decision Boundary')
ax.grid(alpha=0.3)
plt.colorbar(scatter, ax=ax, label='Should Cool')

# D) Energy gain
ax = axes[1, 1]
cooling_data = df[df['should_cool'] == 1]
if len(cooling_data) > 0:
    ax.hist(cooling_data['energy_gain'], bins=40, color='#1a9850', alpha=0.7)
    mean_gain = cooling_data['energy_gain'].mean()
    ax.axvline(mean_gain, color='red', linestyle='--', linewidth=2,
               label=f'Mean: {mean_gain:.2f}W')
    ax.set_xlabel('Energy Gain (W)')
    ax.set_ylabel('Frequency')
    ax.set_title('Energy Gain When Cooling')
    ax.legend()
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('02_decision_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_decision_analysis.png")
plt.close()

# ============================================================================
# FIGURE 3: Top Regions Comparison
# ============================================================================
print("[3/3] Creating regional comparison...")
fig, axes = plt.subplots(3, 2, figsize=(14, 12))

top_6 = region_stats.head(6)['region'].tolist()

for idx, region in enumerate(top_6):
    ax = axes[idx // 2, idx % 2]
    
    region_data = df[df['region'] == region].groupby('hour').agg({
        'panel_temp': 'mean',
        'AmbientTemp_C': 'mean',
        'should_cool': 'mean'
    })
    
    ax.plot(region_data.index, region_data['panel_temp'], 
           'r-', linewidth=2.5, marker='o', label='Panel Temp')
    ax.plot(region_data.index, region_data['AmbientTemp_C'], 
           'b--', linewidth=2, label='Ambient Temp')
    
    ax2 = ax.twinx()
    ax2.fill_between(region_data.index, 0, region_data['should_cool'] * 100,
                     alpha=0.3, color='green')
    ax2.set_ylabel('Cooling %', color='green')
    ax2.set_ylim(0, 100)
    
    cooling_pct = top_6[idx]
    pct_val = region_stats[region_stats['region'] == region]['cooling_pct'].values[0]
    ax.set_title(f"{region.replace('_', ' ').title()} ({pct_val:.1f}% cooling)")
    ax.set_xlabel('Hour')
    ax.set_ylabel('Temperature (°C)')
    ax.legend(loc='upper left', fontsize=8)
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('03_top_regions.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_top_regions.png")
plt.close()

# ============================================================================
# Summary Stats
# ============================================================================
print("\n" + "="*60)
print("SUMMARY STATISTICS".center(60))
print("="*60)
print(f"\nTotal Samples: {len(df):,}")
print(f"Regions: {df['region'].nunique()}")
print(f"Cooling Active: {df['should_cool'].sum():,} ({df['should_cool'].mean()*100:.1f}%)")
print(f"\nPanel Temp - Mean: {df['panel_temp'].mean():.2f}°C, Max: {df['panel_temp'].max():.2f}°C")
print(f"Irradiance - Mean: {df['Irradiance_Wm2'].mean():.2f} W/m²")

if len(cooling_data) > 0:
    print(f"\nEnergy Gain (when cooling): {cooling_data['energy_gain'].mean():.2f}W avg")

print(f"\nTop 5 Regions by Cooling Benefit:")
for i, row in region_stats.head(5).iterrows():
    print(f"  {row['region']:<20} {row['cooling_pct']:>6.2f}%")

print("\n" + "="*60)
print("✓ Generated 3 visualizations successfully!")
print("="*60)
