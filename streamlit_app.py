import streamlit as st
import pandas as pd
import math
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

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    base_url = 'https://www.usbr.gov/pn-bin/daily.pl'
    station = 'hpd'
    format_type = 'csv'
    start_year = '2024'
    start_month = '6'
    start_day = '30'
    end_year = '2024'
    end_month = '8'
    end_day = '31'
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

''
'### raw data from usbr.gov'
gdp_df
