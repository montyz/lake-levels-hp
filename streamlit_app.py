import streamlit as st
import pandas as pd
import datetime
import altair as alt
from pathlib import Path
import numpy as np

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Howard Prairie Lake Level at Ramp',
    page_icon=':sailboat:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data(ttl='8h')
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    last_month = today - datetime.timedelta(days=30)

    base_url = 'https://www.usbr.gov/pn-bin/daily.pl'
    station = 'hpd'
    format_type = 'csv'
    start_year = last_month.year
    start_month = last_month.month
    start_day = last_month.day
    end_year = yesterday.year
    end_month = yesterday.month
    end_day = yesterday.day
    param1 = 'fb'
    param2 = 'qj'
    url = f"{base_url}?station={station}&format={format_type}&year={start_year}&month={start_month}&day={start_day}&year={end_year}&month={end_month}&day={end_day}&pcode={param1}&pcode={param2}"

    raw_gdp_df = pd.read_csv(url)
    
    return raw_gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :sailboat: Howard Prairie Lake Levels at Ramp

by Monty Zukowski
'''

# Add some spacing
''
''

ramp = st.number_input('ramp elevation (adjustable)', value = 4501.0)
gdp_df['depth_at_ramp'] = gdp_df['hpd_fb'] - ramp

hover = alt.selection_point(
    fields=["DateTime"],
    nearest=True,
    on="mouseover",
    empty=False,
)

# The basic line
line = alt.Chart(gdp_df).mark_line().encode(
    x=alt.X("DateTime",title = "Date"),
    y=alt.Y("depth_at_ramp", title = "Depth at ramp")
)

points = line.transform_filter(hover).mark_circle(size=65)
tooltips = (
    alt.Chart(gdp_df)
    .mark_rule()
    .encode(
        x="DateTime",
        y="depth_at_ramp",
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("DateTime", title="Date"),
            alt.Tooltip("depth_at_ramp", title="Depth at ramp"),
        ],
    )
    .add_params(hover)
)
data_layer = line + points + tooltips
st.altair_chart(data_layer, use_container_width=True)

''
'### raw data from usbr.gov'
gdp_df
