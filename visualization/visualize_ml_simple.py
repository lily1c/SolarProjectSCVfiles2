"""
Simplified ML Visualizations for Research Poster
Clean, tall, professional designs with better colors
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Rectangle, FancyArrowPatch

# Professional color scheme
BLUE = '#1f77b4'
ORANGE = '#ff7f0e'
GREEN = '#2ca02c'
RED = '#d62728'
PURPLE = '#9467bd'
GRAY = '#7f7f7f'
LIGHT_BLUE = '#aec7e8'
LIGHT_ORANGE = '#ffbb78'
LIGHT_GREEN = '#98df8a'

plt.rcParams['font.size'] = 14
plt.rcParams['font.weight'] = 'normal'

# ============================================================================
# FIGURE 1: SIMPLE TRAINING FLOW (TALL)
# ============================================================================
print("Creating Training Flow...")

fig, ax = plt.subplots(figsize=(8, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Title
ax.text(5, 13.5, 'Machine Learning Training Process', 
        fontsize=20, fontweight='bold', ha='center')

# Step boxes - clean and simple
steps = [
    (12, 'Data Collection', '15 Climate Regions\n10 Training | 5 Testing\n10,800 Total Samples', BLUE),
    (10.5, 'Filter Data', 'Irradiance > 600 W/m²', ORANGE),
    (9, 'Calculate Features', 'Panel Temp\nEnergy Gain', GREEN),
    (7.5, 'Balance Classes', 'Upsample to 50-50', PURPLE),
    (6, 'Split Training Data', '80% Train\n20% Validation', RED),
    (4.5, 'Train Model', 'Random Forest\n100 Trees', BLUE),
    (3, 'Evaluate & Test', 'Training Accuracy: 89%\nTest on 5 New Regions', GREEN),
]

for y_pos, title, content, color in steps:
    # Box
    rect = Rectangle((2, y_pos-0.4), 6, 1, 
                     facecolor=color, edgecolor='black', linewidth=2, alpha=0.3)
    ax.add_patch(rect)
    
    # Title
    ax.text(5, y_pos+0.15, title, fontsize=16, fontweight='bold', 
           ha='center', va='center')
    # Content
    ax.text(5, y_pos-0.15, content, fontsize=13, ha='center', va='center')
    
    # Arrow to next step (except last)
    if y_pos > 3:
        arrow = FancyArrowPatch((5, y_pos-0.4), (5, y_pos-1.1),
                               arrowstyle='->', mutation_scale=30, 
                               linewidth=3, color='black')
        ax.add_patch(arrow)

# Final result box
rect_final = Rectangle((1.5, 1.2), 7, 1.3, 
                       facecolor=LIGHT_GREEN, edgecolor='black', 
                       linewidth=3, alpha=0.5)
ax.add_patch(rect_final)
ax.text(5, 2.2, 'Model Ready for Deployment', 
       fontsize=18, fontweight='bold', ha='center')
ax.text(5, 1.7, 'Predicts: Cool vs No Cool', fontsize=14, ha='center')

plt.tight_layout()
plt.savefig('ML_1_Training_Flow.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ML_1_Training_Flow.png")
plt.close()


# ============================================================================
# FIGURE 2: MODEL PERFORMANCE (TALL, SIMPLE)
# ============================================================================
print("Creating Performance Metrics...")

fig, axes = plt.subplots(3, 1, figsize=(8, 14))
fig.suptitle('Model Performance', fontsize=22, fontweight='bold', y=0.995)

# A) Accuracy Bar Chart (TOP)
ax = axes[0]
metrics = ['Overall\nAccuracy', 'Precision\n(Cool)', 'Recall\n(Cool)', 'F1-Score']
values = [0.89, 0.88, 0.91, 0.89]
colors = [BLUE, GREEN, ORANGE, PURPLE]

bars = ax.bar(metrics, values, color=colors, edgecolor='black', linewidth=2, width=0.6)
ax.set_ylabel('Score', fontsize=16, fontweight='bold')
ax.set_title('A) Classification Metrics', fontsize=18, fontweight='bold', pad=20)
ax.set_ylim(0, 1.0)
ax.grid(axis='y', alpha=0.3, linewidth=1.5)
ax.axhline(0.85, color=RED, linestyle='--', linewidth=3, label='Target: 85%')

# Value labels
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.03,
           f'{val:.0%}', ha='center', va='bottom', fontsize=16, fontweight='bold')

ax.legend(fontsize=14, loc='lower right')
ax.tick_params(labelsize=13)

# B) Feature Importance (MIDDLE)
ax = axes[1]
features = ['Panel\nTemperature', 'Solar\nIrradiance', 'Ambient\nTemperature', 'Hour\nof Day']
importance = [0.45, 0.35, 0.15, 0.05]
colors_feat = [RED, ORANGE, BLUE, GRAY]

bars = ax.barh(features, importance, color=colors_feat, edgecolor='black', linewidth=2, height=0.6)
ax.set_xlabel('Importance', fontsize=16, fontweight='bold')
ax.set_title('B) Feature Importance', fontsize=18, fontweight='bold', pad=20)
ax.set_xlim(0, 0.5)
ax.grid(axis='x', alpha=0.3, linewidth=1.5)

# Value labels
for bar, val in zip(bars, importance):
    width = bar.get_width()
    ax.text(width + 0.015, bar.get_y() + bar.get_height()/2.,
           f'{val:.0%}', ha='left', va='center', fontsize=15, fontweight='bold')

ax.tick_params(labelsize=13)

# C) Confusion Matrix (BOTTOM)
ax = axes[2]
conf_matrix = np.array([[850, 120], [90, 880]])

# Simple color matrix
im = ax.imshow(conf_matrix, cmap='Blues', aspect='auto', vmin=0, vmax=1000)

# Add text annotations
for i in range(2):
    for j in range(2):
        text_color = 'white' if conf_matrix[i, j] > 500 else 'black'
        ax.text(j, i, f'{conf_matrix[i, j]}',
               ha='center', va='center', fontsize=24, fontweight='bold', color=text_color)

ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(['No Cool', 'Cool'], fontsize=14, fontweight='bold')
ax.set_yticklabels(['No Cool', 'Cool'], fontsize=14, fontweight='bold')
ax.set_xlabel('Predicted', fontsize=16, fontweight='bold')
ax.set_ylabel('Actual', fontsize=16, fontweight='bold')
ax.set_title('C) Confusion Matrix', fontsize=18, fontweight='bold', pad=20)

# Add colorbar
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Count', fontsize=14, fontweight='bold')
cbar.ax.tick_params(labelsize=12)

plt.tight_layout()
plt.savefig('ML_2_Performance.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ML_2_Performance.png")
plt.close()


# ============================================================================
# FIGURE 3: MODEL ARCHITECTURE (TALL, CLEAN)
# ============================================================================
print("Creating Model Architecture...")

fig, ax = plt.subplots(figsize=(8, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

# Title
ax.text(5, 13.5, 'Random Forest Architecture', 
        fontsize=20, fontweight='bold', ha='center')

# Input layer
ax.text(5, 12.5, 'INPUT FEATURES', fontsize=16, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor=LIGHT_BLUE, edgecolor='black', linewidth=2))

inputs = [
    (11.5, 'Ambient Temperature (°C)'),
    (10.8, 'Solar Irradiance (W/m²)'),
    (10.1, 'Panel Temperature (°C)'),
    (9.4, 'Hour of Day'),
]

for y_pos, label in inputs:
    rect = Rectangle((2, y_pos-0.15), 6, 0.3, 
                    facecolor=LIGHT_BLUE, edgecolor='black', linewidth=1.5)
    ax.add_patch(rect)
    ax.text(5, y_pos, label, fontsize=13, ha='center', va='center')

# Arrow down
arrow1 = FancyArrowPatch((5, 9.2), (5, 8.8), arrowstyle='->', 
                        mutation_scale=30, linewidth=4, color='black')
ax.add_patch(arrow1)

# Random Forest box
rect_rf = Rectangle((1.5, 6.5), 7, 2, 
                   facecolor=LIGHT_GREEN, edgecolor='black', linewidth=3)
ax.add_patch(rect_rf)

ax.text(5, 8.1, 'RANDOM FOREST', fontsize=18, fontweight='bold', ha='center')
ax.text(5, 7.6, '100 Decision Trees', fontsize=14, ha='center')
ax.text(5, 7.2, 'Max Depth: 10', fontsize=14, ha='center')
ax.text(5, 6.8, 'Class Weighted: Balanced', fontsize=14, ha='center')

# Arrow down
arrow2 = FancyArrowPatch((5, 6.5), (5, 6.1), arrowstyle='->', 
                        mutation_scale=30, linewidth=4, color='black')
ax.add_patch(arrow2)

# Voting box
rect_vote = Rectangle((2, 5), 6, 0.8, 
                     facecolor=LIGHT_ORANGE, edgecolor='black', linewidth=2)
ax.add_patch(rect_vote)
ax.text(5, 5.4, 'Majority Voting', fontsize=16, fontweight='bold', ha='center')

# Arrow down
arrow3 = FancyArrowPatch((5, 5), (5, 4.6), arrowstyle='->', 
                        mutation_scale=30, linewidth=4, color='black')
ax.add_patch(arrow3)

# Output layer
ax.text(5, 4.1, 'OUTPUT', fontsize=16, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', edgecolor='black', linewidth=2))

# Decision boxes
rect_no = Rectangle((1, 3), 3.5, 0.6, 
                   facecolor='#ffcccc', edgecolor='black', linewidth=2)
ax.add_patch(rect_no)
ax.text(2.75, 3.3, 'NO COOLING (0)', fontsize=14, fontweight='bold', ha='center')

rect_yes = Rectangle((5.5, 3), 3.5, 0.6, 
                    facecolor='#ccffcc', edgecolor='black', linewidth=2)
ax.add_patch(rect_yes)
ax.text(7.25, 3.3, 'COOLING (1)', fontsize=14, fontweight='bold', ha='center')

# Info box at bottom
info_box = Rectangle((0.5, 0.3), 9, 2.2, 
                    facecolor='#f0f0f0', edgecolor='black', linewidth=2)
ax.add_patch(info_box)

ax.text(5, 2.2, 'KEY CHARACTERISTICS', fontsize=16, fontweight='bold', ha='center')

info_text = """
✓ Ensemble Learning: Combines 100 trees
✓ Reduces Overfitting: Better generalization
✓ Handles Noise: Robust to sensor errors
✓ Binary Classification: Cool or No Cool
"""

ax.text(0.8, 1.8, info_text, fontsize=13, va='top', fontweight='normal')

plt.tight_layout()
plt.savefig('ML_3_Architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ML_3_Architecture.png")
plt.close()


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✅ SIMPLIFIED ML VISUALIZATIONS COMPLETE!".center(70))
print("="*70)
print("\nGenerated 3 poster-ready figures:")
print("  1. ML_1_Training_Flow.png - Clean vertical workflow")
print("  2. ML_2_Performance.png - Simple metrics display")
print("  3. ML_3_Architecture.png - Clear model structure")
print("\n💡 Tall format perfect for poster columns!")
print("   Better colors, cleaner design, straightforward layout")
print("="*70)