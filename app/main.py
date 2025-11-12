import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# === PAGE CONFIG ===
st.set_page_config(page_title="Solar Potential Dashboard", layout="wide")

# === HEADER ===
st.title("☀️ Cross-Country Solar Potential Dashboard")
st.markdown("""
Explore and compare solar resource metrics (GHI, DNI, DHI) across Benin, Sierra Leone, and Togo.
Use the sidebar to select countries and metrics for analysis.
""")

# === LOAD DATA ===
@st.cache_data
def load_data():
    data_dir = "data"
    dfs = {}
    for country in ["benin", "sierra_leone", "togo"]:
        path = os.path.join(data_dir, f"{country}_clean.csv")
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["Timestamp"])
            df["Country"] = country.replace("_", " ").title()
            dfs[country] = df
    return dfs

dfs = load_data()

if not dfs:
    st.error("No data found. Please ensure cleaned CSVs are in the `data/` folder.")
    st.stop()

# === SIDEBAR FILTERS ===
st.sidebar.header("Filters")

countries_selected = st.sidebar.multiselect(
    "Select countries to compare:",
    options=list(dfs.keys()),
    default=list(dfs.keys())
)

metrics = ["GHI", "DNI", "DHI"]
metric_selected = st.sidebar.selectbox("Select metric:", metrics)

# === PREPARE DATA ===
df_all = pd.concat([dfs[c] for c in countries_selected])

# === LAYOUT ===
st.markdown(f"### 📊 Comparison by {metric_selected}")

# Plotting
fig, ax = plt.subplots(figsize=(6, 4))
sns.set_context("talk", font_scale=0.8)
sns.boxplot(
    x="Country",
    y=metric_selected,
    data=df_all,
    ax=ax,
    hue="Country",
    palette="viridis",
    legend=False
)
ax.set_title(f"{metric_selected} Distribution by Country")
ax.set_xlabel("")
ax.set_ylabel(metric_selected)
st.pyplot(fig)

# === SUMMARY TABLE ===
st.markdown("### 📈 Summary Statistics")

summary = df_all.groupby("Country")[metrics].agg(["mean", "median", "std"]).round(2)
st.dataframe(summary)

# === OPTIONAL STATISTICAL TEST ===
from scipy.stats import f_oneway

if len(countries_selected) > 1:
    data_groups = [dfs[c][metric_selected].dropna() for c in countries_selected]
    stat, p_val = f_oneway(*data_groups)
    st.markdown(f"**ANOVA p-value:** {p_val:.4f}")
    if p_val < 0.05:
        st.success("✅ Significant difference detected between countries.")
    else:
        st.info("ℹ️ No statistically significant difference detected.")

# === VISUAL RANKING ===
st.markdown("### 🏆 Average GHI by Country")

avg_ghi = (
    df_all.groupby("Country")["GHI"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig2, ax2 = plt.subplots(figsize=(6, 3))
sns.barplot(x="Country", y="GHI", data=avg_ghi, ax=ax2, palette="magma")
ax2.set_title("Average GHI Comparison")
ax2.set_ylabel("Mean GHI")
ax2.set_xlabel("")
st.pyplot(fig2)

# === INSIGHTS ===
st.markdown("### 💡 Key Insights")
st.markdown("""
- **Benin** tends to show the highest median GHI, indicating the strongest solar potential.
- **Togo** follows closely, with slightly higher variability in solar radiation.
- **Sierra Leone** exhibits lower GHI values and higher humidity levels, potentially impacting efficiency.

Overall, **Benin (Malanville)** appears most favorable for solar generation among the three.
""")

st.markdown("---")
st.caption("Developed for KAIM Week 0 – Solar Challenge 🌍")
