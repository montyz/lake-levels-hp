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
    raw_gdp_df['x'] = pd.to_datetime(raw_gdp_df['DateTime'])
    raw_gdp_df['y'] = raw_gdp_df['hpd_fb'].astype(float)
    
    return raw_gdp_df

def demo():
    np.random.seed(42)
    columns = ["A", "B", "C"]
    source = pd.DataFrame(
        np.cumsum(np.random.randn(100, 3), 0).round(2),
        columns=columns, index=pd.RangeIndex(100, name="x"),
    )
    source = source.reset_index().melt("x", var_name="category", value_name="y")

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection_point(nearest=True, on="pointerover",
                                fields=["x"], empty=False)

    # The basic line
    line = alt.Chart(source).mark_line(interpolate="basis").encode(
        x="x:Q",
        y="y:Q",
        color="category:N"
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart(source).transform_pivot(
        "category",
        value="y",
        groupby=["x"]
    ).mark_rule(color="gray").encode(
        x="x:Q",
        opacity=alt.condition(nearest, alt.value(0.3), alt.value(0)),
        tooltip=[alt.Tooltip(c, type="quantitative") for c in columns],
    ).add_params(nearest)


    # Put the five layers into a chart and bind the data
    demo = alt.layer(
        line, points, rules
    ).properties(
    width=600, height=300
    )
    st.altair_chart(demo)

gdp_df = get_gdp_data()
st.altair_theme(theme=None)
demo()
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


# Draw points on the line, and highlight based on selection
points = line.mark_point().encode(
   opacity=alt.condition(nearest, alt.value(1), alt.value(0))
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
    line, points, rules
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
