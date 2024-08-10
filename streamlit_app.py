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
gdp_df['hpd_fb'] = gdp_df['hpd_fb'] - ramp

st.line_chart(
    gdp_df,
    x='DateTime',
    x_label='date',
    y='hpd_fb',
    y_label='feet'
)

# The basic line
line = alt.Chart(gdp_df).mark_line().encode(
    x='DateTime',
    y='hpd_fb'
)

# Create a selection that chooses the nearest point & selects based on x-value
nearest = alt.selection_point(nearest=True, on="pointerover",
                              fields=["DateTime"], empty=False)

# # Interactive line chart with tooltips
# line.interactive().properties(
#     selection=nearest,
#     tooltip=[
#         alt.Tooltip('hpd_fb:Q', title='Lake Level (feet)'),
#         alt.Tooltip('DateTime:Q', title='Date', format='%Y-%m-%d %H:%M:%S'),
#     ]
# )



# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
)


altair_chart = alt.layer(
    line, points
)


st.altair_chart(altair_chart)

''
'### raw data from usbr.gov'
gdp_df
