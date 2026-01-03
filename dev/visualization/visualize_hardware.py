"""
Hardware Implementation Visualization - Blair's Arduino Control System
Based on research paper Phase 3
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Wedge
import numpy as np

# Professional colors
BLUE = '#1f77b4'
ORANGE = '#ff7f0e'
GREEN = '#2ca02c'
RED = '#d62728'
PURPLE = '#9467bd'
GRAY = '#7f7f7f'
LIGHT_BLUE = '#aec7e8'
LIGHT_GREEN = '#98df8a'
LIGHT_RED = '#ff9896'
LIGHT_ORANGE = '#ffbb78'

plt.rcParams['font.size'] = 11

# ============================================================================
# FIGURE 1: HARDWARE SYSTEM ARCHITECTURE
# ============================================================================
print("Creating Hardware System Architecture...")

fig, ax = plt.subplots(figsize=(14, 16))
ax.set_xlim(0, 14)
ax.set_ylim(0, 16)
ax.axis('off')

# Title
ax.text(7, 15.5, 'Arduino-Based Solar Panel Cooling Control System', 
        fontsize=18, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.8', facecolor=LIGHT_BLUE, 
                 edgecolor='black', linewidth=3))

# ============================================================================
# SECTION 1: HARDWARE COMPONENTS (TOP)
# ============================================================================
ax.text(7, 14.5, 'HARDWARE COMPONENTS', fontsize=14, fontweight='bold', 
       ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_ORANGE,
       edgecolor='black', linewidth=2))

# Arduino Uno (Center)
arduino_box = Rectangle((5.5, 12.5), 3, 1.5, facecolor=BLUE, 
                        edgecolor='black', linewidth=2, alpha=0.3)
ax.add_patch(arduino_box)
ax.text(7, 13.6, 'ARDUINO UNO', fontsize=13, fontweight='bold', ha='center')
ax.text(7, 13.2, 'ATmega328P\n5V | 16MHz', fontsize=9, ha='center')

# Temperature Sensor (Left)
temp_box = Rectangle((1, 12.5), 2.5, 1.5, facecolor=ORANGE,
                     edgecolor='black', linewidth=2, alpha=0.3)
ax.add_patch(temp_box)
ax.text(2.25, 13.5, 'TEMP SENSOR', fontsize=11, fontweight='bold', ha='center')
ax.text(2.25, 13.1, 'LM35/DS18B20\n±2°C accuracy\nPin: A0', fontsize=9, ha='center')

# Relay Module (Right)
relay_box = Rectangle((10.5, 12.5), 2.5, 1.5, facecolor=GREEN,
                      edgecolor='black', linewidth=2, alpha=0.3)
ax.add_patch(relay_box)
ax.text(11.75, 13.5, 'RELAY MODULE', fontsize=11, fontweight='bold', ha='center')
ax.text(11.75, 13.1, '5V Control\nPump Switching\nPin: 7', fontsize=9, ha='center')

# LED Indicators
led_green_box = Rectangle((0.5, 10.5), 2, 1, facecolor=LIGHT_GREEN,
                          edgecolor='black', linewidth=2)
ax.add_patch(led_green_box)
ax.text(1.5, 11.2, 'GREEN LED', fontsize=10, fontweight='bold', ha='center')
ax.text(1.5, 10.8, 'Stage 1\nPin: 2', fontsize=8, ha='center')

led_red_box = Rectangle((3, 10.5), 2, 1, facecolor=LIGHT_RED,
                        edgecolor='black', linewidth=2)
ax.add_patch(led_red_box)
ax.text(4, 11.2, 'RED LED', fontsize=10, fontweight='bold', ha='center')
ax.text(4, 10.8, 'Stage 2\nPin: 3', fontsize=8, ha='center')

# Water Pump
pump_box = Rectangle((9, 10.5), 2.5, 1, facecolor=LIGHT_BLUE,
                     edgecolor='black', linewidth=2)
ax.add_patch(pump_box)
ax.text(10.25, 11.2, 'WATER PUMP', fontsize=10, fontweight='bold', ha='center')
ax.text(10.25, 10.8, '2W | 25L/min', fontsize=8, ha='center')

# Power Supply
power_box = Rectangle((12, 10.5), 1.5, 1, facecolor='#ffff99',
                      edgecolor='black', linewidth=2)
ax.add_patch(power_box)
ax.text(12.75, 11.2, 'POWER', fontsize=10, fontweight='bold', ha='center')
ax.text(12.75, 10.8, '5V DC', fontsize=8, ha='center')

# ============================================================================
# SECTION 2: CONTROL FLOW (MIDDLE)
# ============================================================================
ax.text(7, 9.8, 'CONTROL LOGIC FLOW', fontsize=14, fontweight='bold',
       ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_GREEN,
       edgecolor='black', linewidth=2))

# Step 1: Temperature Reading
step1_box = Rectangle((1, 8.3), 4, 1.2, facecolor='white',
                      edgecolor=ORANGE, linewidth=2)
ax.add_patch(step1_box)
ax.text(3, 9.2, '1. READ TEMPERATURE', fontsize=11, fontweight='bold', ha='center')
ax.text(3, 8.8, 'Analog Pin A0 → Voltage\nVoltage × 100 → °C', fontsize=8, ha='center')

arrow1 = FancyArrowPatch((5, 8.9), (5.5, 8.9), arrowstyle='->', 
                        mutation_scale=25, linewidth=3, color='black')
ax.add_patch(arrow1)

# Step 2: Compare to Thresholds
step2_box = Rectangle((5.5, 8.3), 3, 1.2, facecolor='white',
                      edgecolor=PURPLE, linewidth=2)
ax.add_patch(step2_box)
ax.text(7, 9.2, '2. COMPARE', fontsize=11, fontweight='bold', ha='center')
ax.text(7, 8.8, 'Check against\nstaged thresholds', fontsize=8, ha='center')

arrow2 = FancyArrowPatch((8.5, 8.9), (9, 8.9), arrowstyle='->', 
                        mutation_scale=25, linewidth=3, color='black')
ax.add_patch(arrow2)

# Step 3: Activate Outputs
step3_box = Rectangle((9, 8.3), 4, 1.2, facecolor='white',
                      edgecolor=GREEN, linewidth=2)
ax.add_patch(step3_box)
ax.text(11, 9.2, '3. ACTIVATE OUTPUT', fontsize=11, fontweight='bold', ha='center')
ax.text(11, 8.8, 'LEDs + Pump Relay\nSerial Monitor Log', fontsize=8, ha='center')

# ============================================================================
# SECTION 3: STAGED COOLING LOGIC (DETAILED)
# ============================================================================
ax.text(7, 7.5, 'STAGED COOLING THRESHOLDS', fontsize=14, fontweight='bold',
       ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#ffe5cc',
       edgecolor='black', linewidth=2))

# Stage boxes
stages_y = 6.5
stages_data = [
    ('<25°C', 'NORMAL', 'All OFF', 'white', 'System idle'),
    ('25-39°C', 'STAGE 1', 'Green LED\nPump ON', LIGHT_GREEN, 'Mild overheating'),
    ('40-59°C', 'STAGE 2', 'Red LED\nPump ON', LIGHT_RED, 'Warning level'),
    ('≥60°C', 'CRITICAL', 'Both LEDs\nPump ON', '#ff6666', 'Maximum cooling'),
]

x_positions = [0.5, 3.8, 7.1, 10.4]
for i, (temp_range, stage_name, action, color, description) in enumerate(stages_data):
    stage_box = Rectangle((x_positions[i], stages_y-1), 3.0, 1.5,
                          facecolor=color, edgecolor='black', linewidth=2)
    ax.add_patch(stage_box)
    
    ax.text(x_positions[i]+1.5, stages_y+0.2, temp_range, 
           fontsize=10, fontweight='bold', ha='center')
    ax.text(x_positions[i]+1.5, stages_y-0.1, stage_name,
           fontsize=11, fontweight='bold', ha='center', color='darkred' if i==3 else 'black')
    ax.text(x_positions[i]+1.5, stages_y-0.5, action,
           fontsize=8, ha='center')
    ax.text(x_positions[i]+1.5, stages_y-0.85, f'({description})',
           fontsize=7, ha='center', style='italic')

# ============================================================================
# SECTION 4: CIRCUIT DIAGRAM (SIMPLIFIED)
# ============================================================================
ax.text(7, 4.7, 'CIRCUIT CONNECTIONS', fontsize=14, fontweight='bold',
       ha='center', bbox=dict(boxstyle='round,pad=0.4', facecolor=LIGHT_BLUE,
       edgecolor='black', linewidth=2))

# Arduino representation (simplified)
arduino_circuit = Rectangle((5.5, 2), 3, 2, facecolor=BLUE,
                           edgecolor='black', linewidth=3, alpha=0.3)
ax.add_patch(arduino_circuit)
ax.text(7, 3.5, 'ARDUINO UNO', fontsize=12, fontweight='bold', ha='center')

# Pin labels
pins_left = [
    ('A0', 'Temp Sensor', 3.2),
    ('GND', 'Ground', 2.8),
    ('5V', 'Power', 2.4),
]

for pin, label, y_pos in pins_left:
    ax.text(5.3, y_pos, pin, fontsize=9, fontweight='bold', ha='right',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', edgecolor='black'))
    ax.plot([4, 5.3], [y_pos, y_pos], 'k-', linewidth=2)
    ax.text(3.5, y_pos, label, fontsize=8, ha='right', va='center')

pins_right = [
    ('Pin 2', 'Green LED', 3.6),
    ('Pin 3', 'Red LED', 3.2),
    ('Pin 7', 'Relay', 2.8),
]

for pin, label, y_pos in pins_right:
    ax.text(8.7, y_pos, pin, fontsize=9, fontweight='bold', ha='left',
           bbox=dict(boxstyle='round,pad=0.2', facecolor='yellow', edgecolor='black'))
    ax.plot([8.7, 10], [y_pos, y_pos], 'k-', linewidth=2)
    ax.text(10.5, y_pos, label, fontsize=8, ha='left', va='center')

# ============================================================================
# SECTION 5: KEY SPECIFICATIONS (BOTTOM)
# ============================================================================
spec_box = Rectangle((0.3, 0.2), 13.4, 1.5, facecolor='#f0f0f0',
                    edgecolor='black', linewidth=2)
ax.add_patch(spec_box)

ax.text(7, 1.5, 'SYSTEM SPECIFICATIONS', fontsize=12, fontweight='bold', ha='center')

specs_text = """
PERFORMANCE: ±2°C accuracy | <1 second response | 1Hz sampling | 100% relay reliability
HARDWARE: Arduino Uno (ATmega328P) | LM35 Temp Sensor | 5V Relay | 220Ω resistors
CONTROL: Staged thresholds (25°C, 40°C, 60°C) | Visual LED feedback | Serial Monitor logging
INTEGRATION: Aligns with MATLAB thermal model | Matches ML noise parameters | Validates physics predictions
"""

ax.text(0.5, 1.25, specs_text, fontsize=8, va='top', family='monospace')

plt.tight_layout()
plt.savefig('Hardware_1_System_Architecture.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: Hardware_1_System_Architecture.png")
plt.close()


# ============================================================================
# FIGURE 2: ARDUINO CODE FLOW
# ============================================================================
print("Creating Arduino Code Flow...")

fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

ax.text(5, 13.5, 'Arduino Control Software Flow', 
        fontsize=18, fontweight='bold', ha='center')

# Code flow boxes
flow_items = [
    (12.5, 'SETUP', 'Initialize pins\nSet pinMode()\nBegin Serial (9600)', BLUE),
    (11.2, 'LOOP START', 'Continuous monitoring\n1 Hz sampling rate', GREEN),
    (9.9, 'READ SENSOR', 'analogRead(A0)\nVoltage = value × (5.0/1023.0)\nTemp = voltage × 100', ORANGE),
    (8.3, 'SERIAL OUTPUT', 'Serial.print("Temperature: ")\nSerial.println(temperatureC)', PURPLE),
    (7.0, 'THRESHOLD CHECK', 'if (temp >= 60)\nelse if (temp >= 40)\nelse if (temp >= 25)\nelse', RED),
    (5.2, 'ACTIVATE STAGE', 'digitalWrite(LEDs)\ndigitalWrite(pumpRelay)\nSerial.println(status)', GREEN),
    (3.9, 'DELAY', 'delay(1000)\n// Wait 1 second', GRAY),
    (2.6, 'LOOP END', 'Return to start\nContinuous operation', BLUE),
]

for y_pos, title, content, color in flow_items:
    box = Rectangle((2, y_pos-0.3), 6, 0.9, facecolor=color,
                   edgecolor='black', linewidth=2, alpha=0.3)
    ax.add_patch(box)
    
    ax.text(5, y_pos+0.3, title, fontsize=11, fontweight='bold', ha='center')
    ax.text(5, y_pos-0.05, content, fontsize=8, ha='center', family='monospace')
    
    # Arrow to next (except last)
    if y_pos > 3:
        arrow = FancyArrowPatch((5, y_pos-0.3), (5, y_pos-0.7),
                               arrowstyle='->', mutation_scale=25,
                               linewidth=3, color='black')
        ax.add_patch(arrow)

# Return arrow
return_arrow = FancyArrowPatch((8, 2.6), (8, 11.2),
                              arrowstyle='->', mutation_scale=25,
                              linewidth=3, color='red', linestyle='--')
ax.add_patch(return_arrow)
ax.text(8.5, 7, 'REPEAT', fontsize=10, fontweight='bold', 
       rotation=90, va='center', color='red')

# Code example box
code_box = Rectangle((0.3, 0.3), 9.4, 2,
                    facecolor='#2b2b2b', edgecolor='black', linewidth=2)
ax.add_patch(code_box)

ax.text(5, 2.1, 'EXAMPLE CODE SNIPPET', fontsize=11, fontweight='bold',
       ha='center', color='white')

code_text = """
int sensorValue = analogRead(A0);
float voltage = sensorValue * (5.0 / 1023.0);
float temperatureC = voltage * 100.0;

if (temperatureC >= 60) {
  digitalWrite(greenLED, HIGH);
  digitalWrite(redLED, HIGH);
  digitalWrite(pumpRelay, HIGH);
  Serial.println("CRITICAL: Maximum cooling");
}
"""

ax.text(0.5, 1.85, code_text, fontsize=7, va='top', family='monospace',
       color='#00ff00')

plt.tight_layout()
plt.savefig('Hardware_2_Arduino_Flow.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: Hardware_2_Arduino_Flow.png")
plt.close()


# ============================================================================
# FIGURE 3: BREADBOARD LAYOUT
# ============================================================================
print("Creating Breadboard Layout...")

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_xlim(0, 12)
ax.set_ylim(0, 10)
ax.axis('off')

ax.text(6, 9.5, 'Breadboard Circuit Assembly', 
        fontsize=18, fontweight='bold', ha='center')

# Breadboard representation
breadboard = Rectangle((1, 2), 10, 6, facecolor='#f5e6d3',
                       edgecolor='black', linewidth=3)
ax.add_patch(breadboard)

# Arduino (simplified)
arduino = Rectangle((2, 4.5), 2.5, 2.5, facecolor=BLUE,
                   edgecolor='black', linewidth=2, alpha=0.4)
ax.add_patch(arduino)
ax.text(3.25, 5.7, 'ARDUINO\nUNO', fontsize=10, fontweight='bold',
       ha='center', color='white')

# Temperature Sensor
temp_sensor = Circle((6, 6.5), 0.3, facecolor=ORANGE,
                    edgecolor='black', linewidth=2)
ax.add_patch(temp_sensor)
ax.text(6, 6.5, 'LM35', fontsize=7, ha='center', fontweight='bold')
ax.plot([4.5, 5.7], [5.5, 6.5], 'k-', linewidth=2)
ax.text(6, 7, 'Temp Sensor', fontsize=8, ha='center')

# Green LED
green_led = Wedge((7.5, 5.5), 0.25, 0, 360, facecolor=GREEN,
                 edgecolor='black', linewidth=2)
ax.add_patch(green_led)
ax.plot([4.5, 7.3], [5, 5.5], 'g-', linewidth=2)
ax.text(7.5, 5, 'Green\nLED', fontsize=7, ha='center')

# Red LED
red_led = Wedge((8.5, 5.5), 0.25, 0, 360, facecolor=RED,
               edgecolor='black', linewidth=2)
ax.add_patch(red_led)
ax.plot([4.5, 8.3], [4.8, 5.5], 'r-', linewidth=2)
ax.text(8.5, 5, 'Red\nLED', fontsize=7, ha='center')

# Relay Module
relay = Rectangle((7, 3), 1.5, 1, facecolor=GREEN,
                 edgecolor='black', linewidth=2, alpha=0.4)
ax.add_patch(relay)
ax.text(7.75, 3.5, 'RELAY', fontsize=9, fontweight='bold', ha='center')
ax.plot([4.5, 7], [4.5, 3.5], 'k-', linewidth=2)

# Ground rail
ground_rail = Rectangle((1.2, 2.3), 9.6, 0.3, facecolor='black', alpha=0.3)
ax.add_patch(ground_rail)
ax.text(11, 2.45, 'GND', fontsize=8, fontweight='bold', color='black')

# Power rail
power_rail = Rectangle((1.2, 7.4), 9.6, 0.3, facecolor='red', alpha=0.3)
ax.add_patch(power_rail)
ax.text(11, 7.55, '5V', fontsize=8, fontweight='bold', color='red')

# Connection labels
connections = [
    (2, 3, 'Pin A0 → Temp'),
    (2, 3.5, 'Pin 2 → Green LED'),
    (2, 4, 'Pin 3 → Red LED'),  
    (2, 4.5, 'Pin 7 → Relay'),
]

for x, y, label in connections:
    ax.text(x-0.2, y, '•', fontsize=20, color='blue')
    ax.text(x+0.2, y, label, fontsize=7, va='center')

# Legend
legend_box = Rectangle((0.3, 0.3), 4, 1.4, facecolor='white',
                       edgecolor='black', linewidth=2)
ax.add_patch(legend_box)

ax.text(2.3, 1.5, 'COMPONENTS', fontsize=10, fontweight='bold', ha='center')

legend_items = [
    ('Arduino Uno', BLUE),
    ('Temp Sensor (LM35)', ORANGE),
    ('Green LED (Pin 2)', GREEN),
    ('Red LED (Pin 3)', RED),
    ('Relay Module (Pin 7)', GREEN),
]

y_legend = 1.2
for label, color in legend_items:
    circle = Circle((0.6, y_legend), 0.1, facecolor=color,
                   edgecolor='black', linewidth=1)
    ax.add_patch(circle)
    ax.text(0.85, y_legend, label, fontsize=7, va='center')
    y_legend -= 0.18

# Notes
notes_box = Rectangle((4.8, 0.3), 6.9, 1.4, facecolor='#ffffcc',
                      edgecolor='black', linewidth=2)
ax.add_patch(notes_box)

ax.text(8.25, 1.5, 'ASSEMBLY NOTES', fontsize=10, fontweight='bold', ha='center')

notes_text = """
• Use 220Ω resistors for LEDs (current limiting)
• Connect 4.7kΩ pull-up for DS18B20 if used
• Ensure proper grounding for all components
• Double-check pin assignments before power-on
• Test with multimeter before connecting Arduino
"""

ax.text(5, 1.3, notes_text, fontsize=7, va='top')

plt.tight_layout()
plt.savefig('Hardware_3_Breadboard_Layout.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✓ Saved: Hardware_3_Breadboard_Layout.png")
plt.close()


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("✅ HARDWARE VISUALIZATIONS COMPLETE!".center(70))
print("="*70)
print("\nGenerated 3 poster-ready figures:")
print("  1. Hardware_1_System_Architecture.png")
print("     - Complete hardware components")
print("     - Staged cooling logic")
print("     - Circuit connections")
print("     - System specifications")
print("")
print("  2. Hardware_2_Arduino_Flow.png")
print("     - Software control flow")
print("     - Code structure")
print("     - Example code snippet")
print("")
print("  3. Hardware_3_Breadboard_Layout.png")
print("     - Physical circuit layout")
print("     - Component connections")
print("     - Assembly notes")
print("\n💡 Perfect for poster hardware implementation section!")
print("="*70)
