import streamlit as st
import pandas as pd
import plotly.express as px

# Full-Screen Layout
st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for Styling
st.markdown("""
    <style>
        .main .block-container {
            padding: 0px !important;
            margin: 0px !important;
            max-width: 100%;
        }
        .main-title {
            font-size: 30px;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            padding: 15px;
            background: #2C3E50;
            border-radius: 10px;
        }
        .refresh-btn {
            display: block;
            width: 200px;
            text-align: center;
            background: rgb(219, 52, 52);
            color: white;
            padding: 10px;
            font-size: 18px;
            border-radius: 5px;
            text-decoration: none;
            margin: 10px auto;
            cursor: pointer;
        }
        .refresh-btn:hover {
            background: #2980b9;
        }
    </style>
""", unsafe_allow_html=True)

# Load CSV Data
df = pd.read_csv("cyber_security_news_live.csv")

# Convert 'Published Date' to datetime format
df['Published Date'] = pd.to_datetime(df['Published Date'], errors='coerce', utc=True)

# Remove NaT values
df = df.dropna(subset=['Published Date'])

# Title
st.markdown('<div class="main-title">🔍 Real-Time Cyber Threat Intelligence Dashboard</div>', unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("🔎 Filter Options")

# Default Dates
if not df.empty:
    min_date = df['Published Date'].min().date()
    max_date = df['Published Date'].max().date()
else:
    min_date = max_date = pd.Timestamp.today().date()

# Date Range Picker
date_range = st.sidebar.date_input("📅 Select Date Range", [min_date, max_date])

# Ensure correct unpacking
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    st.sidebar.error("⚠️ Please select a valid date range!")
    start_date, end_date = min_date, max_date

# Keyword Search
keyword = st.sidebar.text_input("🔍 Search by Keyword")

# Source Filter
sources = df["Source"].unique().tolist()
selected_sources = st.sidebar.multiselect("📢 Select News Sources", sources, default=sources)

# Sort News
sort_by = st.sidebar.radio("🔀 Sort News By", ["Latest", "Oldest"])

# Filter Data
df_filtered = df[
    (df['Published Date'].dt.date >= start_date) &
    (df['Published Date'].dt.date <= end_date) &
    (df['Source'].isin(selected_sources))
]

if keyword:
    df_filtered = df_filtered[df_filtered["Title"].str.contains(keyword, case=False, na=False)]

df_filtered = df_filtered.sort_values("Published Date", ascending=(sort_by == "Oldest"))

# Display Filtered Data
st.write("## 📊 Latest Cyber Security News")
if not df_filtered.empty:
    st.data_editor(df_filtered, use_container_width=True, height=450)
else:
    st.warning("⚠️ No data available for the selected filters!")

# Most Critical Cyber Security News
st.write("## 🚨 Most Critical Cyber Security News")
critical_keywords = ["Breach", "Ransomware", "Zero-Day", "Hack", "Exploit", "Malware", "APT"]
df_critical = df_filtered[df_filtered['Title'].str.contains('|'.join(critical_keywords), case=False, na=False)]

if not df_critical.empty:
    st.data_editor(df_critical, use_container_width=True, height=300)
else:
    st.warning("⚠️ No critical news found!")

# Pie Chart for Source Distribution
st.write("## 🥧 News Source Distribution")
if not df_filtered.empty:
    fig_pie = px.pie(df_filtered, names='Source', title='Distribution of News Sources')
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.warning("⚠️ No data available!")

# Line Chart for News Over Time
st.write("## 📈 Cyber Threat Trends Over Time")
if not df_filtered.empty:
    df_sorted = df_filtered.sort_values('Published Date')
    df_count = df_sorted.groupby(df_sorted['Published Date'].dt.date).size().reset_index(name='Count')
    fig_line = px.line(df_count, x='Published Date', y='Count', title='Daily Cyber News Trend')
    st.plotly_chart(fig_line, use_container_width=True)
else:
    st.warning("⚠️ No data available!")

# Refresh Button
if st.button("🔄 Refresh Data", help="Click to reload the dashboard"):
    st.rerun()

# Contact Section with LinkedIn and GitHub Links
st.markdown("""
    <h2 style='font-size:28px; color:#1f77b4;'>📬 Get in Touch!</h2>
    <p style='font-size:20px; color:#ffffff;'>
        If you have any questions or just want to connect, feel free to reach out to me on LinkedIn or check out my GitHub!
    </p>
    <p style='font-size:22px; font-weight:bold; color:#ffffff; text-align: center;'>
        🔗 <span style="font-weight: bold;">Mangesh Ambekar</span>
    </p>
    <div style="display: flex; justify-content: center; gap: 20px; align-items: center;">
        <a href="https://www.linkedin.com/in/mangeshsanjayambekar/" target="_blank">
            <img src="https://www.svgrepo.com/show/448234/linkedin.svg" alt="LinkedIn"
                 style="width: 60px; height: 60px;">
        </a>
        <a href="https://github.com/Mangesh0101" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="GitHub"
                 style="width: 60px; height: 60px;">
        </a>
    </div>
""", unsafe_allow_html=True)
