"""
Machine Learning Model Visualization for Research Poster
Creates publication-ready figures for Random Forest classifier
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mpatches

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 11
plt.rcParams['font.weight'] = 'bold'

# ============================================================================
# FIGURE 1: ML PIPELINE FLOWCHART
# ============================================================================
print("Creating ML Pipeline Flowchart...")

fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)

# Title
ax.text(5, 11.5, 'Random Forest Classifier: Training Pipeline', 
        fontsize=18, fontweight='bold', ha='center')

# Step 1: Data Collection
box1 = FancyBboxPatch((1, 9.5), 3, 1, boxstyle="round,pad=0.1", 
                       edgecolor='#2E86AB', facecolor='#A9D9F5', linewidth=3)
ax.add_patch(box1)
ax.text(2.5, 10, '1. DATA COLLECTION\n10 Climate Regions\n7,200 hourly samples', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow 1
arrow1 = FancyArrowPatch((2.5, 9.5), (2.5, 8.7), arrowstyle='->', 
                        mutation_scale=30, linewidth=3, color='black')
ax.add_patch(arrow1)

# Step 2: Feature Engineering
box2 = FancyBboxPatch((1, 7.5), 3, 1, boxstyle="round,pad=0.1",
                       edgecolor='#F77F00', facecolor='#FFD19A', linewidth=3)
ax.add_patch(box2)
ax.text(2.5, 8, '2. FEATURE ENGINEERING\nNOCT Calculations\nSensor Noise Injection', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow 2
arrow2 = FancyArrowPatch((2.5, 7.5), (2.5, 6.7), arrowstyle='->', 
                        mutation_scale=30, linewidth=3, color='black')
ax.add_patch(arrow2)

# Step 3: Class Balancing
box3 = FancyBboxPatch((1, 5.5), 3, 1, boxstyle="round,pad=0.1",
                       edgecolor='#9D4EDD', facecolor='#E0BBE4', linewidth=3)
ax.add_patch(box3)
ax.text(2.5, 6, '3. CLASS BALANCING\nUpsampling Minority\n50-50 Distribution', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow 3
arrow3 = FancyArrowPatch((2.5, 5.5), (2.5, 4.7), arrowstyle='->', 
                        mutation_scale=30, linewidth=3, color='black')
ax.add_patch(arrow3)

# Step 4: Train/Test Split
box4 = FancyBboxPatch((1, 3.5), 3, 1, boxstyle="round,pad=0.1",
                       edgecolor='#06A77D', facecolor='#B4E7CE', linewidth=3)
ax.add_patch(box4)
ax.text(2.5, 4, '4. TRAIN/TEST SPLIT\n80% Training\n20% Testing', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow 4
arrow4 = FancyArrowPatch((2.5, 3.5), (2.5, 2.7), arrowstyle='->', 
                        mutation_scale=30, linewidth=3, color='black')
ax.add_patch(arrow4)

# Step 5: Random Forest Training
box5 = FancyBboxPatch((0.5, 1.5), 4, 1, boxstyle="round,pad=0.1",
                       edgecolor='#D62828', facecolor='#F7B5B5', linewidth=3)
ax.add_patch(box5)
ax.text(2.5, 2, '5. RANDOM FOREST TRAINING\n100 Estimators | Max Depth: 10\nClass Weight: Balanced', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# Arrow 5
arrow5 = FancyArrowPatch((2.5, 1.5), (2.5, 0.7), arrowstyle='->', 
                        mutation_scale=30, linewidth=3, color='black')
ax.add_patch(arrow5)

# Step 6: Model Evaluation
box6 = FancyBboxPatch((1, 0), 3, 0.6, boxstyle="round,pad=0.1",
                       edgecolor='#1A535C', facecolor='#85C7B3', linewidth=3)
ax.add_patch(box6)
ax.text(2.5, 0.3, '6. MODEL EVALUATION\nAccuracy: 87-90%', 
        ha='center', va='center', fontsize=10, fontweight='bold')

# Right side: Key parameters box
param_box = FancyBboxPatch((5.5, 1), 4, 9.5, boxstyle="round,pad=0.15",
                           edgecolor='#003566', facecolor='#EEF4FF', linewidth=2)
ax.add_patch(param_box)

ax.text(7.5, 10, 'MODEL SPECIFICATIONS', fontsize=13, fontweight='bold', 
        ha='center', bbox=dict(boxstyle='round', facecolor='#003566', 
        edgecolor='black', linewidth=2, alpha=0.9))

# Parameters text
params_text = """
ALGORITHM:
• Random Forest Classifier
• Ensemble Method (100 Trees)

INPUT FEATURES (4):
• Ambient Temperature (°C)
• Solar Irradiance (W/m²)
• Panel Temperature (°C)
• Hour of Day

OUTPUT:
• Binary: Cool (1) / No Cool (0)

TRAINING DATA:
• 10 Climate Regions
• ~7,200 samples after filtering
• Balanced: 50-50 split

HYPERPARAMETERS:
• n_estimators = 100
• max_depth = 10
• class_weight = 'balanced'
• random_state = 42

VALIDATION:
• 80-20 Train-Test Split
• Stratified Sampling

NOISE INJECTION:
• Irradiance: ±15 W/m²
• Ambient Temp: ±0.5°C
• Panel Temp: ±2°C
• Wind Cooling: 0-5 m/s
"""

ax.text(5.7, 9.5, params_text, fontsize=9, va='top', family='monospace',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.savefig('ML_01_Training_Pipeline.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ML_01_Training_Pipeline.png")
plt.close()


# ============================================================================
# FIGURE 2: MODEL PERFORMANCE METRICS
# ============================================================================
print("Creating Model Performance Metrics...")

fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)

fig.suptitle('Random Forest Model: Performance Analysis', fontsize=18, fontweight='bold')

# A) Confusion Matrix
ax1 = fig.add_subplot(gs[0, 0])
# Example confusion matrix (replace with actual values)
conf_matrix = np.array([[850, 120], [90, 880]])
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax1, 
            cbar_kws={'label': 'Count'}, linewidths=2, linecolor='black')
ax1.set_xlabel('Predicted Label', fontweight='bold', fontsize=11)
ax1.set_ylabel('True Label', fontweight='bold', fontsize=11)
ax1.set_title('A) Confusion Matrix', fontweight='bold', fontsize=12, pad=10)
ax1.set_xticklabels(['No Cool', 'Cool'], fontweight='bold')
ax1.set_yticklabels(['No Cool', 'Cool'], fontweight='bold', rotation=0)

# B) Accuracy Metrics Bar Chart
ax2 = fig.add_subplot(gs[0, 1:])
metrics = ['Accuracy', 'Precision\n(No Cool)', 'Recall\n(No Cool)', 
           'Precision\n(Cool)', 'Recall\n(Cool)', 'F1-Score']
values = [0.89, 0.91, 0.88, 0.88, 0.91, 0.89]  # Example values
colors = ['#2E86AB', '#F77F00', '#F77F00', '#06A77D', '#06A77D', '#9D4EDD']

bars = ax2.bar(metrics, values, color=colors, edgecolor='black', linewidth=2, alpha=0.8)
ax2.set_ylabel('Score', fontweight='bold', fontsize=11)
ax2.set_title('B) Classification Metrics', fontweight='bold', fontsize=12, pad=10)
ax2.set_ylim(0, 1.0)
ax2.grid(axis='y', alpha=0.3)
ax2.axhline(0.85, color='red', linestyle='--', linewidth=2, label='Target: 85%')

# Add value labels on bars
for bar, val in zip(bars, values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02,
            f'{val:.2%}', ha='center', va='bottom', fontweight='bold', fontsize=10)
ax2.legend(fontsize=10)

# C) Feature Importance
ax3 = fig.add_subplot(gs[1, :])
features = ['Panel Temperature', 'Irradiance', 'Ambient Temperature', 'Hour of Day']
importance = [0.45, 0.35, 0.15, 0.05]  # Example values
colors_feat = plt.cm.RdYlGn(np.array(importance))

bars = ax3.barh(features, importance, color=colors_feat, edgecolor='black', linewidth=2)
ax3.set_xlabel('Feature Importance', fontweight='bold', fontsize=11)
ax3.set_title('C) Feature Importance Analysis', fontweight='bold', fontsize=12, pad=10)
ax3.grid(axis='x', alpha=0.3)

for bar, val in zip(bars, importance):
    width = bar.get_width()
    ax3.text(width + 0.01, bar.get_y() + bar.get_height()/2.,
            f'{val:.1%}', ha='left', va='center', fontweight='bold', fontsize=11)

# D) Class Distribution - Before Balancing
ax4 = fig.add_subplot(gs[2, 0])
classes_before = ['No Cooling', 'Cooling']
counts_before = [5100, 2100]  # Example 70-30 split
colors_pie = ['#d73027', '#1a9850']
wedges, texts, autotexts = ax4.pie(counts_before, labels=classes_before, autopct='%1.0f%%',
                                    colors=colors_pie, startangle=90,
                                    textprops={'fontsize': 10, 'fontweight': 'bold'})
ax4.set_title('D) Before Balancing\n(Imbalanced)', fontweight='bold', fontsize=11)

# E) Class Distribution - After Balancing
ax5 = fig.add_subplot(gs[2, 1])
classes_after = ['No Cooling', 'Cooling']
counts_after = [5100, 5100]  # 50-50 after upsampling
wedges, texts, autotexts = ax5.pie(counts_after, labels=classes_after, autopct='%1.0f%%',
                                    colors=colors_pie, startangle=90,
                                    textprops={'fontsize': 10, 'fontweight': 'bold'})
ax5.set_title('E) After Upsampling\n(Balanced)', fontweight='bold', fontsize=11)

# F) Key Insights Box
ax6 = fig.add_subplot(gs[2, 2])
ax6.axis('off')

insights_text = """
KEY FINDINGS:

✓ Model Accuracy: 87-90%

✓ High Precision (both classes)
  → Minimizes false activations

✓ Panel Temp most important
  (45% contribution)

✓ Balanced dataset prevents
  bias toward majority class

✓ Noise injection ensures
  robustness to sensor errors

✓ Generalizes across 10
  diverse climate zones
"""

ax6.text(0.1, 0.95, insights_text, fontsize=10, va='top', fontweight='bold',
        bbox=dict(boxstyle='round,pad=1', facecolor='#FFE5B4', 
        edgecolor='black', linewidth=2))

plt.savefig('ML_02_Performance_Metrics.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ML_02_Performance_Metrics.png")
plt.close()


# ============================================================================
# FIGURE 3: DECISION TREE VISUALIZATION (SIMPLIFIED)
# ============================================================================
print("Creating Decision Tree Visualization...")

fig, ax = plt.subplots(figsize=(14, 10))
ax.axis('off')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

ax.text(5, 9.5, 'Random Forest: Ensemble of 100 Decision Trees', 
        fontsize=16, fontweight='bold', ha='center')

# Root node
root = FancyBboxPatch((3.5, 7.5), 3, 0.8, boxstyle="round,pad=0.1",
                      edgecolor='black', facecolor='#FFD700', linewidth=3)
ax.add_patch(root)
ax.text(5, 7.9, 'Panel Temp > 45°C?', ha='center', va='center', 
        fontsize=11, fontweight='bold')

# Left branch - NO
arrow_left = FancyArrowPatch((3.8, 7.5), (2, 6.5), arrowstyle='->', 
                            mutation_scale=25, linewidth=2.5, color='red')
ax.add_patch(arrow_left)
ax.text(2.5, 7, 'NO', fontsize=10, fontweight='bold', color='red')

node_left = FancyBboxPatch((0.5, 5.5), 3, 0.8, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor='#90EE90', linewidth=2)
ax.add_patch(node_left)
ax.text(2, 5.9, 'No Cooling\n(Class 0)', ha='center', va='center',
        fontsize=10, fontweight='bold')

# Right branch - YES
arrow_right = FancyArrowPatch((6.2, 7.5), (8, 6.5), arrowstyle='->', 
                             mutation_scale=25, linewidth=2.5, color='green')
ax.add_patch(arrow_right)
ax.text(7.3, 7, 'YES', fontsize=10, fontweight='bold', color='green')

node_right = FancyBboxPatch((6.5, 5.5), 3, 0.8, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='#FFE5B4', linewidth=2)
ax.add_patch(node_right)
ax.text(8, 5.9, 'Irradiance > 600 W/m²?', ha='center', va='center',
        fontsize=10, fontweight='bold')

# From second node - NO
arrow_r_left = FancyArrowPatch((7, 5.5), (6, 4.5), arrowstyle='->', 
                              mutation_scale=20, linewidth=2, color='red')
ax.add_patch(arrow_r_left)
ax.text(6.3, 5, 'NO', fontsize=9, fontweight='bold', color='red')

leaf_r_left = FancyBboxPatch((4.5, 3.5), 3, 0.8, boxstyle="round,pad=0.1",
                            edgecolor='black', facecolor='#90EE90', linewidth=2)
ax.add_patch(leaf_r_left)
ax.text(6, 3.9, 'No Cooling\n(Class 0)', ha='center', va='center',
        fontsize=10, fontweight='bold')

# From second node - YES
arrow_r_right = FancyArrowPatch((8.5, 5.5), (8.5, 4.5), arrowstyle='->', 
                               mutation_scale=20, linewidth=2, color='green')
ax.add_patch(arrow_r_right)
ax.text(8.8, 5, 'YES', fontsize=9, fontweight='bold', color='green')

leaf_r_right = FancyBboxPatch((7, 3.5), 3, 0.8, boxstyle="round,pad=0.1",
                             edgecolor='black', facecolor='#FF6B6B', linewidth=2)
ax.add_patch(leaf_r_right)
ax.text(8.5, 3.9, 'Energy Gain >\nCooling Cost?', ha='center', va='center',
        fontsize=10, fontweight='bold')

# Final leaves
arrow_final_no = FancyArrowPatch((7.5, 3.5), (7, 2.5), arrowstyle='->', 
                                mutation_scale=15, linewidth=1.5, color='red')
ax.add_patch(arrow_final_no)
ax.text(7.1, 3, 'NO', fontsize=8, fontweight='bold', color='red')

final_no = FancyBboxPatch((5.5, 1.5), 3, 0.8, boxstyle="round,pad=0.1",
                         edgecolor='black', facecolor='#90EE90', linewidth=2)
ax.add_patch(final_no)
ax.text(7, 1.9, 'No Cooling\n(Class 0)', ha='center', va='center',
        fontsize=10, fontweight='bold')

arrow_final_yes = FancyArrowPatch((8.5, 3.5), (9, 2.5), arrowstyle='->', 
                                 mutation_scale=15, linewidth=1.5, color='green')
ax.add_patch(arrow_final_yes)
ax.text(8.9, 3, 'YES', fontsize=8, fontweight='bold', color='green')

final_yes = FancyBboxPatch((8, 1.5), 2, 0.8, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor='#32CD32', linewidth=2)
ax.add_patch(final_yes)
ax.text(9, 1.9, 'COOL!\n(Class 1)', ha='center', va='center',
        fontsize=10, fontweight='bold', color='white')

# Legend box
legend_box = FancyBboxPatch((0.2, 0.2), 2.5, 1.8, boxstyle="round,pad=0.1",
                           edgecolor='black', facecolor='#F0F0F0', linewidth=2)
ax.add_patch(legend_box)

ax.text(1.45, 1.7, 'RANDOM FOREST:', fontsize=10, fontweight='bold', ha='center')
ax.text(0.3, 1.3, '• 100 trees vote', fontsize=9, fontweight='bold')
ax.text(0.3, 1.0, '• Majority wins', fontsize=9, fontweight='bold')
ax.text(0.3, 0.7, '• Reduces overfitting', fontsize=9, fontweight='bold')
ax.text(0.3, 0.4, '• Handles noise well', fontsize=9, fontweight='bold')

plt.savefig('ML_03_Decision_Tree_Example.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: ML_03_Decision_Tree_Example.png")
plt.close()


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✅ ML VISUALIZATION COMPLETE!".center(70))
print("="*70)
print("\nGenerated 3 poster-ready figures:")
print("  1. ML_01_Training_Pipeline.png - Complete training workflow")
print("  2. ML_02_Performance_Metrics.png - Accuracy & feature importance")
print("  3. ML_03_Decision_Tree_Example.png - Simplified decision tree")
print("\n💡 Perfect for research poster ML section!")
print("="*70)
