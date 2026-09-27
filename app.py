import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Lebanon Life Expectancy", layout="wide")

# ---------------------------------------------------------------
# Load and prepare the data
# ---------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Social-Development.csv")

    fe = df[df["Indicator Code"] == "SP.DYN.LE00.FE.IN"][["refPeriod", "Value"]]
    fe = fe.rename(columns={"Value": "Female"})

    ma = df[df["Indicator Code"] == "SP.DYN.LE00.MA.IN"][["refPeriod", "Value"]]
    ma = ma.rename(columns={"Value": "Male"})

    merged = pd.merge(fe, ma, on="refPeriod").sort_values("refPeriod")
    merged["refPeriod"] = merged["refPeriod"].astype(int)
    merged["Gap"] = merged["Female"] - merged["Male"]
    return merged.reset_index(drop=True)

data = load_data()

# ---------------------------------------------------------------
# Title and context
# ---------------------------------------------------------------
st.title("Lebanon: Life Expectancy and the Gender Gap (1960–2021)")

st.markdown("""
This page explores life expectancy at birth for women and men in Lebanon, using World Bank
Social Development Indicators. Two linked charts below use the same data:
a **time trend** of life expectancy, and a **correlation scatter plot** comparing female vs male
life expectancy directly.
""")

with st.expander("Two key insights (click to expand)"):
    st.markdown(f"""
1. Female and male life expectancy are strongly correlated (r ≈ **{data['Female'].corr(data['Male']):.2f}**)
   across the full period — they rise and fall together.
2. The gender gap roughly **tripled during the civil war** (1975–1990), averaging about
   **{data[(data.refPeriod>=1975)&(data.refPeriod<=1990)]['Gap'].mean():.1f} years**, compared to
   about **{data[data.refPeriod<1975]['Gap'].mean():.1f} years** before the war.
""")

st.divider()

# ---------------------------------------------------------------
# Interactive widget 1: period dropdown
# ---------------------------------------------------------------
PERIODS = {
    "Full history (1960–2021)": (1960, 2021),
    "Pre-Civil War (1960–1974)": (1960, 1974),
    "Civil War era (1975–1990)": (1975, 1990),
    "Post-war (1991–2021)": (1991, 2021),
}

col1, col2 = st.columns([1, 2])

with col1:
    period_label = st.selectbox("Step 1 — Choose a historical period", list(PERIODS.keys()))
    period_min, period_max = PERIODS[period_label]

# ---------------------------------------------------------------
# Interactive widget 2: year slider, LINKED to widget 1
# (its min/max come from the period chosen above — this is the link)
# ---------------------------------------------------------------
with col2:
    year_range = st.slider(
        "Step 2 — Fine-tune the exact years shown",
        min_value=period_min,
        max_value=period_max,
        value=(period_min, period_max),
    )

# Filter the data using both selections combined
filtered = data[(data["refPeriod"] >= year_range[0]) & (data["refPeriod"] <= year_range[1])]
st.caption(f"Showing {len(filtered)} years, from {year_range[0]} to {year_range[1]}.")

# ---------------------------------------------------------------
# Charts
# ---------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=filtered["refPeriod"], y=filtered["Female"],
                                    mode="lines+markers", name="Female", line=dict(color="#d1495b")))
    fig_line.add_trace(go.Scatter(x=filtered["refPeriod"], y=filtered["Male"],
                                    mode="lines+markers", name="Male", line=dict(color="#2e86ab")))
    fig_line.update_layout(title="Life expectancy over time",
                             xaxis_title="Year", yaxis_title="Life expectancy (years)")
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    fig_scatter = px.scatter(filtered, x="Male", y="Female", hover_data={"refPeriod": True})
    fig_scatter.update_traces(marker=dict(size=9, color="#2e86ab"))
    fig_scatter.update_layout(title="Female vs. male life expectancy (correlation)",
                                xaxis_title="Male life expectancy (years)",
                                yaxis_title="Female life expectancy (years)")
    st.plotly_chart(fig_scatter, use_container_width=True)

if len(filtered) >= 2:
    st.markdown(f"For this range: correlation **r = {filtered['Female'].corr(filtered['Male']):.2f}**, "
                f"average gap **{filtered['Gap'].mean():.1f} years**.")

st.divider()

# ---------------------------------------------------------------
# Design justifications
# ---------------------------------------------------------------
st.header("Design justifications")

with st.expander("Feature 1 — Period selector (dropdown)"):
    st.markdown("""
**User question:** Was Lebanon's conflict history visible in health outcomes, and how do the
pre-war, war-time, and post-war periods differ?

**Why this widget:** A dropdown was used instead of checkboxes/multiselect because the periods
are mutually exclusive, ordered eras — not categories a reader would want to combine.

**Course concept:** Providing context before detail — the dropdown gives the reader a
pre-labelled, meaningful starting point instead of a raw 62-year chart with no orientation.
""")

with st.expander("Feature 2 — Year-range slider (linked to the period selector)"):
    st.markdown("""
**User question:** Within the chosen era, exactly which years drove the pattern?

**Why this widget:** A slider was used instead of two separate number boxes because it makes
the relationship between start/end visually clear and can't produce an invalid range.

**Course concept:** Drill-down / focusing attention — the slider's own min/max come from the
period chosen in Feature 1, so picking "Civil War era" narrows the slider itself to 1975–1990.
This link is what makes the two widgets work together rather than as two separate filters.
""")