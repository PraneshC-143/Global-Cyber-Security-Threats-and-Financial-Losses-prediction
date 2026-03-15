# 🛡️ Global Cybersecurity Threats & Financial Losses Dashboard
### Project Summary Report

---

## 📌 1. About the Project

The **Global Cybersecurity Threats & Financial Losses Dashboard** is an interactive, AI-powered web application built using **Python and Streamlit**. It combines historical cybersecurity data analysis with real-time live threat intelligence into a single unified platform.

The dashboard enables users to **explore, analyze, visualize, and predict** cyber attack trends — both from a 10-year historical dataset (2015–2025) and from live global threat feeds updated every few seconds.

---

## ❓ 2. Why This Project Exists (Problem Statement)

Cybersecurity threats are growing at an unprecedented rate. In 2024 alone, global cybercrime cost businesses over **$8 trillion**, and that figure is projected to cross **$10.5 trillion by 2025**.

However, most organizations and students face a critical gap:

- **Security analysts** have no single tool that combines historical trend analysis with live attack intelligence
- **Students and researchers** rely on static reports that go out of date quickly
- **Decision makers** cannot easily understand technical security data — it's too complex and jargon-heavy
- **Existing tools are expensive, siloed, and inaccessible** to small organizations and academic institutions

This dashboard was built to **bridge that gap** — providing a free, open, beautiful, and understandable tool for anyone who needs to understand the global cyber threat landscape.

---

## 🔄 3. Existing System & Its Limitations

| Existing Tool | Limitation |
|---|---|
| **Splunk / IBM QRadar** | Extremely expensive (enterprise licensing), requires deep technical expertise |
| **Static CSV / Excel reports** | No visualization, no live updates, no predictions |
| **AlienVault OTX (raw API)** | Requires programming knowledge to query; no visual interface |
| **Generic security dashboards** | Not customized for financial loss analysis or ML-based forecasting |
| **Academic research papers** | Static, text-heavy, no interactive exploration |

**Key problems solved by this project:**
- ✅ Real-time + historical data in one place (no tool did both)
- ✅ Plain-English explanations of attack types (no jargon)
- ✅ ML-based financial and attack forecasting (no free tool offered this)
- ✅ Beautiful, accessible UI for non-technical users

---

## ⭐ 4. Unique Features of This Dashboard

| Feature | Why It's Unique |
|---|---|
| **Dual-Mode Intelligence** | ONLY tool combining a historical ML engine + live OTX threat radar in one app |
| **3D Interactive Globe** 🌍 | Real Earth-like globe (orthographic) with country name labels on attack dots |
| **Plain-English Attack Explanations** | Every attack type has a tooltip explaining it in simple, jargon-free language |
| **Friendly Filter Labels** | Sidebar filters show `🦠 Malware (Harmful Software)` instead of plain `Malware` |
| **ML Financial Forecasting** | Predicts financial losses for 2025–2030 based on real historical data |
| **User-Friendly Geo Map Tooltips** | Clicking a map dot shows: Origin Country, Danger Level, Threats Found, Attack Type — all in plain English |
| **Live Pulse Stream** | Real-time color-coded security feed showing threats as they happen globally |
| **Polynomial Trend Predictor** | Live regression model forecasting next 15 attack ticks based on real-time data |
| **Fully Dark Theme UI** | Premium glassmorphism design with colored metric cards — looks like a real SOC dashboard |

---

## 👥 5. Who Is This Useful For?

| User Type | How They Benefit |
|---|---|
| 🎓 **Students & Researchers** | Learn cybersecurity concepts through visualizations and plain-English explanations |
| 🔒 **Security Analysts (SOC Teams)** | Monitor live threats from AlienVault OTX in a visual, filterable interface |
| 📊 **Data Scientists** | Study the ML/forecasting models and adapt them for research |
| 💼 **Business Decision Makers** | Understand financial impact of cyber threats without reading technical papers |
| 🏫 **Academic Institutions** | Use as a teaching tool in cybersecurity or data science courses |
| 🏛️ **Government & Policy Makers** | Understand which sectors and countries are most at risk |
| 📰 **Journalists & Analysts** | Quickly access statistics on current global cyber threat trends |

---

## 📊 6. Dashboard Features & Workflow

### 🔀 Two Intelligence Modes

```
 ┌────────────────────────────────────────────────────────────────┐
 │             CYBERSECURITY DASHBOARD                            │
 │                                                                │
 │   SIDEBAR ──► Select Mode                                      │
 │               ┌───────────────────┐   ┌──────────────────────┐│
 │               │ Historical ML     │   │ Live Threat Radar    ││
 │               │ Engine            │   │ (OTX)                ││
 │               └───────────────────┘   └──────────────────────┘│
 └────────────────────────────────────────────────────────────────┘
```

---

### 📘 Mode 1 — Historical ML Engine

**Data Flow:**
```
CSV Dataset (3,300 records, 2015–2025)
      ↓ Load & Clean (remove nulls, normalize columns)
      ↓ Apply Sidebar Filters (Year / Country / Industry)
      ↓ Render Charts + Run ML Models
      ↓ Display Forecasts & Insights
```

**Tabs & Features:**

| Tab | Feature | Chart Type |
|---|---|---|
| **Dashboard Overview** | Quick Summary (4 metric cards) | — |
| | Financial Impact Over Time | Area chart |
| | Most Common Attack Types | Horizontal bar + plain-English hovers |
| | Industry Risk Breakdown | Pie chart |
| | Global Attack Heatmap | Matrix heatmap |
| | Resolution Time Distribution | Histogram |
| **Detailed Stats** | Country-wise rankings, loss by sector | Bar charts |
| **Future Predictions** | ML attack severity classifier | Random Forest model |
| | Financial forecast 2025–2030 | Line + polynomial regression |
| | Model accuracy & confusion matrix | Plotly table |
| **Data Details** | Raw cleaned dataset viewer | Interactive table |

---

### 🔴 Mode 2 — Live Threat Radar (OTX)

**Data Flow:**
```
AlienVault OTX API (global sensor network)
      ↓ Authenticated request every 5 seconds
      ↓ Parse: extract TLP level, IOC types, coordinates, author
      ↓ Apply Sidebar Filters (TLP / Attack Type)
      ↓ Update charts in real-time
      ↓ Auto-rerun Streamlit loop
```

**Tabs & Features:**

| Tab | Feature | Description |
|---|---|---|
| **Live Threat Map** | 4 Live Metric Cards | Attacks tracked / IOC volume / Countries / Agency |
| | 3D Globe Map | Real Earth with country labels, rotatable, colored attack dots |
| | Alert Severity Donut | 🔴🟡🟢🔵 color-coded threat level breakdown |
| | Threat Types Donut | Malicious IPs / Bad sites / Files / Links |
| | Top Attack Origins | Which countries send the most attacks |
| | Attack Volume Timeline | Live rolling chart of threat frequency |
| **Threat Intelligence** | Correlation Heatmap | Attack type × IOC type relationship matrix |
| | Current Attack Stats | Detailed counts per threat category |
| **Predictive Analytics** | Live Regression Model | Forecasts next 15 time periods of attack volume |
| **Raw Data Logs** | Live Pulse Stream | Color-coded real-time threat feed |
| | System Logs | Backend API status and data ingestion logs |

---

## 🛠️ 7. Technology Stack

| Component | Technology |
|---|---|
| **Web Framework** | Streamlit (Python) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly Express, Plotly Graph Objects |
| **Machine Learning** | Scikit-learn (Random Forest, Polynomial Regression) |
| **Live Threat Feed** | AlienVault OTX API (OTXv2 Python SDK) |
| **Geolocation** | IP geolocation via OTX pulse metadata |
| **Styling** | Custom CSS (glassmorphism, dark theme) |
| **Version Control** | Git + GitHub |

---

## 📈 8. Project Impact & Value

- **3,300+ real attack records** analyzed across 10 years
- **10+ chart types** covering financial, geographic, temporal, and categorical data
- **Real-time global intelligence** from AlienVault's community of thousands of security researchers
- **Free and open source** — accessible to anyone
- **No cybersecurity background required** — all technical terms explained in plain English

---

*Generated: March 2026 | Author: PraneshC-143 | GitHub: github.com/PraneshC-143/Global-Cyber-Security-Threats-and-Financial-Losses-prediction*
