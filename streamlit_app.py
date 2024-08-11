import streamlit as st
import pandas as pd
import datetime
import altair as alt
from pathlib import Path

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
    raw_gdp_df['x'] = pd.to_datetime(raw_gdp_df['DateTime'])
    raw_gdp_df['y'] = raw_gdp_df['hpd_fb'].astype(float)
    
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

ramp = st.number_input('ramp elevation', value = 4501.0)
gdp_df['y'] = gdp_df['y'] - ramp


# The basic line
line = alt.Chart(gdp_df).mark_line().encode(
    x='x',
    y='y'
)

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection_point(nearest=True, on="pointerover",
                              fields=["x"], empty=False)

# Interactive line chart with tooltips
line.interactive().properties(
    selection=nearest,
    # tooltip=[
    #     alt.Tooltip('hpd_fb:Q', title='Lake Level (feet)'),
    #     alt.Tooltip('DateTime:Q', title='Date', format='%Y-%m-%d %H:%M:%S'),
    # ]
)

# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
   # opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)

# Draw a rule at the location of the selection
rules = alt.Chart(gdp_df).mark_rule(color="gray").encode(
    x="x:Q",
    y='y:Q'

).transform_filter(
    nearest
)
selectors = alt.Chart(gdp_df).mark_point().encode(
    x="x:Q",
    opacity=alt.value(0),
).add_params(
    nearest
)
altair_chart = alt.layer(
    line, rules#, points, rules
)


st.altair_chart(altair_chart)


st.line_chart(
    gdp_df,
    x='x',
    x_label='date',
    y='y',
    y_label='feet'
)


''
'### raw data from usbr.gov'
gdp_df
