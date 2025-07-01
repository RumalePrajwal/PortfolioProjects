import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from ai_strategy_agent import ask_motogp_ai

# Load data
@st.cache_data
def load_data():
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "simulated", "all_sessions.parquet"))
    return pd.read_parquet(path)

df = load_data()

# Sidebar – Session Controls
st.sidebar.title("🏁 MotoGP Strategy Dashboard")
track = st.sidebar.selectbox("Select Track", sorted(df["track"].unique()))
session = st.sidebar.selectbox("Select Session", sorted(df["session"].unique()))
filtered_df = df[(df["track"] == track) & (df["session"] == session)]

riders = sorted(filtered_df["rider"].unique())
selected_riders = st.sidebar.multiselect("Select Riders", riders, default=riders[:3])

st.title(f"{track} – {session} Session")
st.write(f"🔍 Showing {len(filtered_df)} rows of data")

# Lap Time Trends
st.subheader("📉 Lap Time Trends")
plot_df = filtered_df[filtered_df["rider"].isin(selected_riders)]

fig, ax = plt.subplots(figsize=(10, 5))
for rider in selected_riders:
    rider_data = plot_df[plot_df["rider"] == rider]
    ax.plot(rider_data["lap"], rider_data["lap_time_sec"], label=rider)

ax.set_xlabel("Lap")
ax.set_ylabel("Lap Time (sec)")
ax.set_title("Lap Time Comparison")
ax.legend()
st.pyplot(fig)

# Tyre and Pit Stop Summary
st.subheader("🛞 Tyre Choice & 🛠 Pit Stops")
col1, col2 = st.columns(2)

with col1:
    tyre_counts = plot_df.groupby("rider")["tyre"].value_counts().unstack(fill_value=0)
    st.bar_chart(tyre_counts)

with col2:
    pit_summary = plot_df.groupby("rider")["pit_stop"].sum().sort_values(ascending=False)
    st.bar_chart(pit_summary)

# Sector Breakdown
st.subheader("⏱ Sector Times (Average)")
sector_means = plot_df.groupby("rider")[["sector1", "sector2", "sector3"]].mean().round(2)
st.dataframe(sector_means)

# Incident Summary
st.subheader("⚠️ Incidents")
incidents = plot_df[plot_df["incident"].notna()]
if not incidents.empty:
    st.dataframe(incidents[["rider", "lap", "incident"]])
else:
    st.info("No incidents in this session.")

# Ask AI
st.markdown("## 🤖 Ask MotoGP AI Strategist")
user_question = st.text_input("Ask a strategy question:")

if user_question:
    with st.spinner("Analyzing..."):
        response = ask_motogp_ai(user_question)
    st.success("Answer:")
    st.write(response)
