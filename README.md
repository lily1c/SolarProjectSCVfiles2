# 🌞 Solar Panel Cooling Optimizer

An interactive web application that optimizes solar panel performance by determining when active cooling is cost-effective using real-time weather data and machine learning.

**🚀 Live Demo:** [https://solarprojectscvfiles2-5k9mwrsrmm9a2m7da5kuba.streamlit.app](https://solarprojectscvfiles2-5k9mwrsrmm9a2m7da5kuba.streamlit.app)

---

## 🎯 Problem Statement

Solar panels lose efficiency as they heat up - approximately 0.5% per degree Celsius above 25°C. While active cooling systems can reduce panel temperature and increase power output, the cooling pump itself consumes energy. 

**The Challenge:** When does the energy gained from cooling outweigh the cost of running the cooling system?

This application solves that optimization problem in real-time for any location worldwide.

---

## ✨ Features

- **🌍 Real-Time Weather Data** - Fetches live temperature and solar irradiance from NASA POWER API
- **🔬 Physics-Based Calculations** - Computes panel temperature using NOCT equations and efficiency models
- **🤖 Machine Learning Validation** - Decision tree model trained on 131k+ samples validates recommendations
- **📊 Interactive Visualizations** - Dynamic gauge charts and energy breakdown graphs using Plotly
- **🌎 Global Coverage** - Works for any location via OpenStreetMap geocoding
- **⚡ Dual Input Modes** - Real-time API data or manual parameter entry

---

## 🛠️ Technology Stack

- **Backend:** Python 3.13
- **Web Framework:** Streamlit
- **Machine Learning:** Scikit-learn (Decision Tree Classifier)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly
- **APIs:** 
  - NASA POWER API (weather data)
  - OpenStreetMap Nominatim (geocoding)

---

## 📦 Installation & Local Setup

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone the repository**
```bash


cat > README.md << 'EOF'
# 🌞 Solar Panel Cooling Optimizer

An interactive web application that optimizes solar panel performance by determining when active cooling is cost-effective using real-time weather data and machine learning.

**🚀 Live Demo:** [https://solarprojectscvfiles2-5k9mwrsrmm9a2m7da5kuba.streamlit.app](https://solarprojectscvfiles2-5k9mwrsrmm9a2m7da5kuba.streamlit.app)

---

## 🎯 Problem Statement

Solar panels lose efficiency as they heat up - approximately 0.5% per degree Celsius above 25°C. While active cooling systems can reduce panel temperature and increase power output, the cooling pump itself consumes energy. 

**The Challenge:** When does the energy gained from cooling outweigh the cost of running the cooling system?

This application solves that optimization problem in real-time for any location worldwide.

---

## ✨ Features

- **🌍 Real-Time Weather Data** - Fetches live temperature and solar irradiance from NASA POWER API
- **🔬 Physics-Based Calculations** - Computes panel temperature using NOCT equations and efficiency models
- **🤖 Machine Learning Validation** - Decision tree model trained on 131k+ samples validates recommendations
- **📊 Interactive Visualizations** - Dynamic gauge charts and energy breakdown graphs using Plotly
- **🌎 Global Coverage** - Works for any location via OpenStreetMap geocoding
- **⚡ Dual Input Modes** - Real-time API data or manual parameter entry

---

## 🛠️ Technology Stack

- **Backend:** Python 3.13
- **Web Framework:** Streamlit
- **Machine Learning:** Scikit-learn (Decision Tree Classifier)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly
- **APIs:** 
  - NASA POWER API (weather data)
  - OpenStreetMap Nominatim (geocoding)

---

## 📦 Installation & Local Setup

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/lily1c/SolarProjectSCVfiles2.git
cd SolarProjectSCVfiles2
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 📁 Project Structure
```
SolarProjectSCVfiles2/
├── 🎯 PRODUCTION CODE
│   ├── app.py                          # Streamlit web interface
│   ├── src/
│   │   └── solar_cooling.py           # Core optimization logic
│   ├── models/
│   │   └── cooling_decision_model.pkl # Trained ML model
│   ├── requirements.txt                # Dependencies
│   └── .streamlit/
│       └── config.toml                # Streamlit configuration
│
└── 📁 DEVELOPMENT CODE
    ├── dev/
    │   ├── data_generation/           # NASA API data fetching scripts
    │   ├── training/                  # ML model training
    │   ├── visualization/             # Analysis and plotting scripts
    │   ├── data_raw/                  # Raw weather data (15 cities)
    │   └── analysis_outputs/          # Generated charts and diagrams
    └── data/
        └── processed/
            └── full_training_data.csv # Complete training dataset
```

---

## 🧮 How It Works

### 1. Panel Temperature Calculation
```python
T_panel = T_ambient + ((NOCT - 20) / 800) × Irradiance
```
- NOCT (Nominal Operating Cell Temperature) = 45°C
- Accounts for heat buildup from solar radiation

### 2. Efficiency Loss Model
```python
efficiency = η_ref × (1 - β × (T_panel - 25°C))
```
- η_ref = 18% (reference efficiency at 25°C)
- β = 0.5%/°C (temperature coefficient)

### 3. Power Output Comparison
- **Uncooled Power:** `P_uncooled = efficiency_uncooled × Irradiance × Panel_Area`
- **Cooled Power:** `P_cooled = efficiency_cooled × Irradiance × Panel_Area`
- **Net Gain:** `P_cooled - P_uncooled - Pump_Power`

### 4. Decision Logic
**Cooling is recommended when:**
```
Energy_Gain > Cooling_Cost
```

---

## 🤖 Machine Learning Model

### Training Data
- **15 geographic locations** (Phoenix, Riyadh, Seattle, Las Vegas, etc.)
- **131,400+ samples** (8,760 hours × 15 regions)
- **Realistic sensor noise** (±15 W/m² irradiance, ±2°C temperature)
- **Features:** Ambient temperature, solar irradiance, hour of day, panel temperature
- **Target:** Binary classification (cool or don't cool)

### Model Performance
- **Algorithm:** Decision Tree Classifier
- **Accuracy:** >95% on test set
- **Validation:** Cross-checked against physics-based calculations

### Best Regions for Cooling
1. **Phoenix, AZ** - High temperature + High irradiance
2. **Riyadh, Saudi Arabia** - Extreme desert heat
3. **Las Vegas, NV** - Consistent sun exposure
4. **Palm Springs, CA** - Hot, dry conditions

---

## 💻 Usage Guide

### Option 1: Real-Time Weather Data
1. Enter a location (e.g., "Phoenix, AZ")
2. Select date and time
3. Click "Fetch Weather Data"
4. View cooling recommendation and analysis

### Option 2: Manual Input
1. Select "Manual Input" mode
2. Adjust temperature and irradiance sliders
3. Results update in real-time

### Understanding Results
- **Green Alert:** Cooling recommended (net energy gain)
- **Orange Alert:** Cooling not recommended (net energy loss)
- **Gauge Charts:** Panel temperature, uncooled power, cooled power
- **Energy Breakdown:** Visual comparison of all energy factors
- **ML Prediction:** Model's recommendation and agreement with physics

---

## 🎓 What I Learned

Building this project taught me how to implement a complete machine learning pipeline and deploy it in a real application. I created a data generation script that fetches weather data from NASA POWER API for 15 geographic regions, generating 131,000+ training samples with realistic sensor noise to simulate real-world conditions. Training a decision tree classifier was straightforward, but I learned that deploying ML models requires careful attention to feature alignment - I had to use `model.feature_names_in_` to ensure my production inputs match the exact column order from training.

I built a modular architecture by extracting core logic into `solar_cooling.py` that both my CLI and web app import from, following DRY principles. Integrating the trained model into a Streamlit web interface taught me about state management, API integration with OpenStreetMap for geocoding, and creating responsive UIs with Plotly visualizations. The deployment process showed me how to structure projects with proper dependency management and relative paths for easy deployment to production environments.

---

## 🚀 Deployment

This app is deployed on **Streamlit Cloud** (free tier):

**Live URL:** [https://solarprojectscvfiles2-5k9mwrsrmm9a2m7da5kuba.streamlit.app](https://solarprojectscvfiles2-5k9mwrsrmm9a2m7da5kuba.streamlit.app)

### To Deploy Your Own Instance:
1. Fork this repository
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy with one click

---

## 🔮 Future Enhancements

- [ ] Wind speed integration for convective cooling effects
- [ ] Historical data analysis and trend visualization
- [ ] Cost-benefit analysis with electricity pricing
- [ ] Support for different panel types and specifications
- [ ] Mobile-responsive design improvements
- [ ] User accounts for saving favorite locations
- [ ] Email/SMS alerts for optimal cooling times

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Assolaba Sova**
- GitHub: [@lily1c](https://github.com/lily1c)

---

## 🙏 Acknowledgments

- **NASA POWER Project** - Free weather data API
- **OpenStreetMap** - Geocoding services
- **Streamlit** - Amazing web framework for Python
- **MLH Fellowship** - Inspiration for building production-ready applications

---

## 📧 Contact

For questions, feedback, or collaboration opportunities, please open an issue on GitHub.

---

**Built for MLH Fellowship 2025** | Demonstrating Python, ML, and Full-Stack Development Skills
