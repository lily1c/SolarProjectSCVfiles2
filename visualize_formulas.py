"""
Thermal Modeling Pipeline with Mathematical Formulas
Shows the complete decision flow with proper equation formatting
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# Professional colors
BLUE = '#1f77b4'
ORANGE = '#ff7f0e'
GREEN = '#2ca02c'
RED = '#d62728'
PURPLE = '#9467bd'
LIGHT_BLUE = '#e3f2fd'
LIGHT_ORANGE = '#fff3e0'
LIGHT_GREEN = '#e8f5e9'
LIGHT_PURPLE = '#f3e5f5'
LIGHT_YELLOW = '#fffde7'

plt.rcParams['font.size'] = 11

# ============================================================================
# THERMAL MODELING PIPELINE WITH FORMULAS
# ============================================================================
print("Creating Thermal Modeling Pipeline...")

fig, ax = plt.subplots(figsize=(12, 16))
ax.set_xlim(0, 12)
ax.set_ylim(0, 16)
ax.axis('off')

# Title
ax.text(6, 15.5, 'Thermal Modeling & Cooling Decision Pipeline', 
        fontsize=18, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor=LIGHT_BLUE, 
                 edgecolor='black', linewidth=3))

# ============================================================================
# STEP 1: Weather Data Input
# ============================================================================
y_pos = 14.2

step1_box = Rectangle((1, y_pos-0.4), 10, 1, facecolor=LIGHT_BLUE,
                      edgecolor=BLUE, linewidth=3)
ax.add_patch(step1_box)

ax.text(6, y_pos+0.3, '1. WEATHER DATA COLLECTION', fontsize=13, 
       fontweight='bold', ha='center')

# Input parameters with nice formatting
ax.text(2, y_pos-0.05, r'$T_{\mathrm{ambient}}$ (°C)', fontsize=11, 
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=BLUE, linewidth=2))
ax.text(5.5, y_pos-0.05, r'$G_{\mathrm{irradiance}}$ (W/m²)', fontsize=11,
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor=BLUE, linewidth=2))
ax.text(9.5, y_pos-0.05, 'NASA POWER API', fontsize=9, ha='center', style='italic')

# Arrow down
arrow1 = FancyArrowPatch((6, y_pos-0.5), (6, y_pos-1), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow1)

# ============================================================================
# STEP 2: NOCT Equation
# ============================================================================
y_pos = 12.5

step2_box = Rectangle((1, y_pos-0.6), 10, 1.3, facecolor=LIGHT_ORANGE,
                      edgecolor=ORANGE, linewidth=3)
ax.add_patch(step2_box)

ax.text(6, y_pos+0.5, '2. NOCT EQUATION', fontsize=13, fontweight='bold', ha='center')

# Main formula with proper LaTeX
formula1 = r'$T_{\mathrm{panel}} = T_{\mathrm{ambient}} + \frac{\mathrm{NOCT} - 20}{800} \times G_{\mathrm{irradiance}}$'
ax.text(6, y_pos+0.1, formula1, fontsize=13, ha='center',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2))

# Parameters
ax.text(2, y_pos-0.35, 'NOCT = 45°C', fontsize=9,
       bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9c4'))
ax.text(6, y_pos-0.35, 'DOKIO FSP-100M', fontsize=9, style='italic')
ax.text(10, y_pos-0.35, 'Standard: IEC 61215', fontsize=8, style='italic')

# Arrow down
arrow2 = FancyArrowPatch((6, y_pos-0.7), (6, y_pos-1.2), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow2)

# ============================================================================
# STEP 3: Panel Temperature
# ============================================================================
y_pos = 10.5

step3_box = Rectangle((1, y_pos-0.5), 10, 1.1, facecolor=LIGHT_GREEN,
                      edgecolor=GREEN, linewidth=3)
ax.add_patch(step3_box)

ax.text(6, y_pos+0.4, '3. PANEL TEMPERATURE CALCULATION', fontsize=13, 
       fontweight='bold', ha='center')

# Temperature scenarios
temps_text = r'Uncooled: $T_{\mathrm{panel}}$ = 55-60°C  |  Cooled: $T_{\mathrm{panel}}$ = 35°C  |  Threshold: 45°C'
ax.text(6, y_pos-0.05, temps_text, fontsize=10, ha='center',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=1.5))

ax.text(6, y_pos-0.35, 'Sensor: LM35/DS18B20 (±2°C accuracy)', fontsize=9, 
       ha='center', style='italic')

# Arrow down
arrow3 = FancyArrowPatch((6, y_pos-0.6), (6, y_pos-1.1), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow3)

# ============================================================================
# STEP 4: Temperature-Dependent Efficiency
# ============================================================================
y_pos = 8.7

step4_box = Rectangle((1, y_pos-0.6), 10, 1.3, facecolor=LIGHT_PURPLE,
                      edgecolor=PURPLE, linewidth=3)
ax.add_patch(step4_box)

ax.text(6, y_pos+0.5, '4. TEMPERATURE-DEPENDENT EFFICIENCY', fontsize=13, 
       fontweight='bold', ha='center')

# Efficiency formula
formula2 = r'$\eta = \eta_{\mathrm{ref}} \times [1 - \beta \times (T_{\mathrm{panel}} - 25)]$'
ax.text(6, y_pos+0.1, formula2, fontsize=13, ha='center',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2))

# Parameters
param_text = r'$\eta_{\mathrm{ref}}$ = 18%  |  $\beta$ = 0.005/°C  |  Loss: -0.5%/°C above 25°C'
ax.text(6, y_pos-0.25, param_text, fontsize=9, ha='center')

ax.text(2.5, y_pos-0.45, 'At 60°C: η = 15.3%', fontsize=9, color=RED, fontweight='bold')
ax.text(6, y_pos-0.45, 'At 35°C: η = 16.65%', fontsize=9, color=GREEN, fontweight='bold')
ax.text(9.5, y_pos-0.45, 'Gain: +1.35%', fontsize=9, color=BLUE, fontweight='bold')

# Arrow down
arrow4 = FancyArrowPatch((6, y_pos-0.7), (6, y_pos-1.2), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow4)

# ============================================================================
# STEP 5: Power Output
# ============================================================================
y_pos = 6.8

step5_box = Rectangle((1, y_pos-0.5), 10, 1.1, facecolor=LIGHT_YELLOW,
                      edgecolor=ORANGE, linewidth=3)
ax.add_patch(step5_box)

ax.text(6, y_pos+0.4, '5. POWER OUTPUT CALCULATION', fontsize=13, 
       fontweight='bold', ha='center')

# Power formula
formula3 = r'$P = \eta \times G \times A_{\mathrm{panel}}$'
ax.text(6, y_pos+0.05, formula3, fontsize=13, ha='center',
       bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black', linewidth=2))

# Results
ax.text(3, y_pos-0.25, r'$A_{\mathrm{panel}}$ = 0.2835 m²', fontsize=9)
ax.text(6, y_pos-0.25, 'At 1000 W/m²:', fontsize=9, fontweight='bold')
ax.text(9, y_pos-0.25, 'P(60°C)=83W → P(35°C)=92W', fontsize=9, color=GREEN, fontweight='bold')

# Arrow down
arrow5 = FancyArrowPatch((6, y_pos-0.6), (6, y_pos-1.1), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow5)

# ============================================================================
# STEP 6: Energy Economics
# ============================================================================
y_pos = 5

step6_box = Rectangle((1, y_pos-0.6), 10, 1.3, facecolor='#e1f5fe',
                      edgecolor=BLUE, linewidth=3)
ax.add_patch(step6_box)

ax.text(6, y_pos+0.5, '6. ENERGY ECONOMICS (Gain vs. Cost)', fontsize=13, 
       fontweight='bold', ha='center')

# Economics formulas
formula4 = r'$E_{\mathrm{gain}} = (\eta_{\mathrm{cooled}} - \eta_{\mathrm{uncooled}}) \times G \times A$'
ax.text(6, y_pos+0.1, formula4, fontsize=11, ha='center',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=1.5))

formula5 = r'$E_{\mathrm{cost}} = \frac{P_{\mathrm{pump}}}{\mathrm{efficiency}} = \frac{2\,\mathrm{W}}{0.85} = 2.35\,\mathrm{W}$'
ax.text(6, y_pos-0.25, formula5, fontsize=10, ha='center')

# Net gain
ax.text(6, y_pos-0.5, r'Net Gain = $E_{\mathrm{gain}} - E_{\mathrm{cost}}$ = +5.78 W/h average', 
       fontsize=10, ha='center', fontweight='bold', color=GREEN,
       bbox=dict(boxstyle='round,pad=0.3', facecolor='#c8e6c9'))

# Arrow down
arrow6 = FancyArrowPatch((6, y_pos-0.7), (6, y_pos-1.2), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow6)

# ============================================================================
# STEP 7: Cooling Decision
# ============================================================================
y_pos = 3

step7_box = Rectangle((1, y_pos-0.7), 10, 1.5, facecolor='#ffebee',
                      edgecolor=RED, linewidth=3)
ax.add_patch(step7_box)

ax.text(6, y_pos+0.6, '7. COOLING DECISION LOGIC', fontsize=13, 
       fontweight='bold', ha='center')

# Decision criteria
decision_text = r'IF $(T_{\mathrm{panel}} > 45°\mathrm{C})$ AND $(G > 600\,\mathrm{W/m}^2)$ AND $(E_{\mathrm{gain}} > 0.8 \times E_{\mathrm{cost}})$'
ax.text(6, y_pos+0.2, decision_text, fontsize=10, ha='center',
       bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=2))

ax.text(6, y_pos-0.15, 'THEN: Activate Cooling System', fontsize=11, ha='center',
       fontweight='bold', color=GREEN)

# Staged response
staged_text = '<25°C: OFF  |  25-39°C: Stage 1  |  40-59°C: Stage 2  |  ≥60°C: Critical'
ax.text(6, y_pos-0.45, staged_text, fontsize=9, ha='center',
       bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff9c4'))

# Arrow down
arrow7 = FancyArrowPatch((6, y_pos-0.8), (6, y_pos-1.3), arrowstyle='->', 
                        mutation_scale=35, linewidth=4, color='black')
ax.add_patch(arrow7)

# ============================================================================
# FINAL OUTPUT: Hardware Control
# ============================================================================
y_pos = 1.2

output_box = Rectangle((1, y_pos-0.5), 10, 1, facecolor='#c8e6c9',
                       edgecolor='black', linewidth=3)
ax.add_patch(output_box)

ax.text(6, y_pos+0.3, 'ARDUINO HARDWARE CONTROL', fontsize=14, 
       fontweight='bold', ha='center')

control_text = 'Green LED + Red LED + Relay → Water Pump Activation'
ax.text(6, y_pos-0.1, control_text, fontsize=11, ha='center', fontweight='bold')

ax.text(6, y_pos-0.35, 'Response Time: <1 second  |  Accuracy: ±2°C  |  ML Validation: 89%', 
       fontsize=9, ha='center', style='italic')

plt.tight_layout()
plt.savefig('/Users/assolabasova/Desktop/Thermal_Pipeline_Formulas.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: Thermal_Pipeline_Formulas.png")
plt.close()


# ============================================================================
# BONUS: KEY EQUATIONS REFERENCE CARD
# ============================================================================
print("Creating Equations Reference Card...")

fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Title
ax.text(5, 7.5, 'Key Mathematical Formulas', fontsize=18, fontweight='bold', ha='center',
       bbox=dict(boxstyle='round,pad=0.8', facecolor=LIGHT_BLUE, edgecolor='black', linewidth=3))

# Equations with boxes
equations = [
    (6.5, 'Panel Temperature (NOCT)', 
     r'$T_{\mathrm{panel}} = T_{\mathrm{ambient}} + \frac{\mathrm{NOCT} - 20}{800} \times G$',
     LIGHT_ORANGE),
    
    (5.3, 'Temperature-Dependent Efficiency',
     r'$\eta = \eta_{\mathrm{ref}} \times [1 - \beta \times (T_{\mathrm{panel}} - 25)]$',
     LIGHT_PURPLE),
    
    (4.1, 'Power Output',
     r'$P = \eta \times G \times A_{\mathrm{panel}}$',
     LIGHT_YELLOW),
    
    (2.9, 'Energy Gain from Cooling',
     r'$E_{\mathrm{gain}} = (\eta_{\mathrm{cooled}} - \eta_{\mathrm{uncooled}}) \times G \times A$',
     LIGHT_GREEN),
    
    (1.7, 'Net Benefit',
     r'$\mathrm{Net\,Gain} = E_{\mathrm{gain}} - E_{\mathrm{cost}}$',
     LIGHT_BLUE),
]

for y, title, formula, color in equations:
    # Box
    box = Rectangle((0.5, y-0.3), 9, 0.9, facecolor=color,
                   edgecolor='black', linewidth=2)
    ax.add_patch(box)
    
    # Title
    ax.text(1, y+0.35, title, fontsize=11, fontweight='bold', va='center')
    
    # Formula
    ax.text(5, y, formula, fontsize=13, ha='center', va='center',
           bbox=dict(boxstyle='round,pad=0.4', facecolor='white', edgecolor='black', linewidth=1.5))

# Constants box at bottom
const_box = Rectangle((0.3, 0.2), 9.4, 1.2, facecolor='#f0f0f0',
                      edgecolor='black', linewidth=2)
ax.add_patch(const_box)

ax.text(5, 1.15, 'CONSTANTS & SPECIFICATIONS', fontsize=12, fontweight='bold', ha='center')

constants_text = r'''
$\eta_{\mathrm{ref}}$ = 0.18 (18%)  |  $\beta$ = 0.005/°C  |  NOCT = 45°C  |  $A_{\mathrm{panel}}$ = 0.2835 m²
$P_{\mathrm{pump}}$ = 2W  |  Efficiency = 0.85  |  $T_{\mathrm{threshold}}$ = 45°C  |  $T_{\mathrm{target}}$ = 35°C
'''

ax.text(5, 0.65, constants_text, fontsize=9, ha='center', va='center')

plt.tight_layout()
plt.savefig('/Users/assolabasova/Desktop/Equations_Reference_Card.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: Equations_Reference_Card.png")
plt.close()


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✅ FORMULA VISUALIZATIONS COMPLETE!".center(70))
print("="*70)
print("\nGenerated 2 poster-ready figures with LaTeX formulas:")
print("  1. Thermal_Pipeline_Formulas.png")
print("     - Complete 7-step pipeline")
print("     - All equations properly formatted")
print("     - Color-coded by stage")
print("")
print("  2. Equations_Reference_Card.png")
print("     - Quick reference of all key formulas")
print("     - Constants and specifications")
print("     - Clean and professional layout")
print("\n💡 Professional mathematical notation for your poster!")
print("="*70)
