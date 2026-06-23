import os
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Open Source Contributor Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Open Source Contributor Behavior Analytics")
st.write("""
This dashboard analyzes contributor activity across
multiple open-source repositories using GitHub data.

Use the sidebar to navigate through the analytics.
""")

# Dataset Information

modified = os.path.getmtime("outputs/contributor_activity.csv")

last_updated = datetime.fromtimestamp(
    modified
).strftime("%d %b %Y %I:%M %p")

st.sidebar.markdown("### 📂 Dataset")
st.sidebar.caption(f"📅 Last Updated: {last_updated}")

# Project Highlights

st.markdown("### 🚀 Features")

st.markdown("""
- 📥 GitHub API Integration
- 📊 Contributor Activity Analytics
- ⚙️ Feature Engineering
- 🏆 Repository Comparison
- 👤 Contributor Explorer
- 📈 Interactive Visualizations
""")
