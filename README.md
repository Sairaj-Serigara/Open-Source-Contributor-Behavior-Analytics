# 📊 Open Source Contributor Analytics

An end-to-end analytics platform that collects contributor data from GitHub repositories, performs feature engineering, and presents interactive insights through a Streamlit dashboard.

---

## 🚀 Project Overview

Open Source Contributor Analytics is designed to analyze contributor behavior across multiple open-source GitHub repositories. The project collects repository data using the GitHub REST API, processes contributor metrics, and visualizes repository and contributor performance through an interactive dashboard.

The dashboard provides repository comparisons, contributor rankings, activity analysis, and detailed contributor insights.

---

## ✨ Features

* GitHub REST API integration
* Repository-wise contributor collection
* Commit, Pull Request, and Issue analytics
* Contributor feature engineering
* Repository comparison dashboard
* Contributor activity ranking
* Interactive Plotly visualizations
* Streamlit-based analytics dashboard

---

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* Requests
* GitHub REST API

---

## 📊 Dashboard Pages

### 🏠 Home

* Project overview
* Dataset information
* Feature summary

### 📈 Overview

* Repository contribution distribution
* Repository summary
* Dataset statistics

### 🏆 Repository Comparison

* Compare repositories across contributor metrics
* Contribution statistics
* Repository performance

### 👤 Contributor Explorer

* Search contributors
* View contributor metrics
* Repository-specific insights

### 🥇 Top Contributors

* Activity score ranking
* Top contributor leaderboard

### 📉 Activity Analysis

* Contributor activity metrics
* Commit frequency analysis
* Pull request and issue insights

---

## 📦 Installation

Clone the repository

```bash
git clone https://github.com/Sairaj-Serigara/Open-Source-Contributor-Analytics.git
```

Navigate to the project

```bash
cd Open-Source-Contributor-Analytics
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Dashboard

```bash
streamlit run app.py
```

---

## 📁 Data Pipeline

1. Collect contributor data from GitHub repositories.
2. Extract commits, pull requests, and issues.
3. Perform feature engineering.
4. Generate repository summaries and contributor rankings.
5. Visualize insights using the Streamlit dashboard.

---


