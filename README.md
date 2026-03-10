# Unified Global Cyber Threats Dashboard

A comprehensive, interactive Streamlit application that merges an exploratory **Historical ML Engine** (analyzing trends from 2015-2025) with a **Live Threat Radar** powered by the AlienVault Open Threat Exchange (OTX) API.

## Features
- **Historical Security Analytics:** Explore years of global breach data with interactive area charts, box plots, and heatmaps.
- **Predictive ML Modeling:** Utilizes Polynomial Regression curves to forecast cumulative financial liabilities and incident counts up to five years in the future.
- **Live Threat Telemetry:** Streams real-time `OTX Pulses` using the AlienVault API, displaying active global attacks on an interactive map.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd Cybersecurity_Dashboard_Project
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure AlienVault OTX Credentials:**
   You must create a `.streamlit/secrets.toml` file in the root directory to authenticate the live map:
   ```toml
   [otx]
   api_key = "YOUR_ALIENVAULT_OTX_API_KEY_HERE"
   ```

## Running the Dashboard
Execute the following command in your terminal:
```bash
streamlit run cyber_dashboard.py
```
This will launch the application in your default web browser (typically on `http://localhost:8501`).
