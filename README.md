# MSBA325-streamlit-app
# MSBA325-streamlit-app

Interactive Streamlit app for MSBA 325, exploring life expectancy and the gender gap in
Lebanon (World Bank Social Development Indicators).

**Live app:** https://amalalrajab15-ai-msba325-streamlit-app-app-fskgpm.streamlit.app

## What it shows

Two linked charts built from the same life-expectancy data (1960–2021):
- A line chart of female/male life expectancy over time
- A scatter plot comparing female vs male life expectancy directly

## Interactivity

- A period dropdown (full history / pre-war / civil war / post-war) sets the range of a
  year-range slider next to it — narrowing the era narrows what years the slider can select.

## Running locally

pip install -r requirements.txt
streamlit run app.py
