# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


# First some MPG Data Exploration
@st.cache
def load_data(path):
    df = pd.read_csv(path)
    return df

clean_energy_ch_raw = load_data(path="../data/renewable_power_plants_CH.csv")
clean_energy_ch = deepcopy(clean_energy_ch_raw)

# Add title and header
st.title("Clean Energy Sources in Switzerland")
st.header("Overview in Switzerland")

with open('../data/georef-switzerland-kanton.geojson') as response:
    cantons = json.load(response)

# Need to find a way to match the canton code from the df with the canton name in the json

cantons_dict = {'TG':'Thurgau', 'GR':'Graubünden', 'LU':'Luzern', 'BE':'Bern', 'VS':'Valais',
                'BL':'Basel-Landschaft', 'SO':'Solothurn', 'VD':'Vaud', 'SH':'Schaffhausen', 'ZH':'Zürich',
                'AG':'Aargau', 'UR':'Uri', 'NE':'Neuchâtel', 'TI':'Ticino', 'SG':'St. Gallen', 'GE':'Genève',
                'GL':'Glarus', 'JU':'Jura', 'ZG':'Zug', 'OW':'Obwalden', 'FR':'Fribourg', 'SZ':'Schwyz',
                'AR':'Appenzell Ausserrhoden', 'AI':'Appenzell Innerrhoden', 'NW':'Nidwalden', 'BS':'Basel-Stadt'}

clean_energy_ch["canton_name"] = clean_energy_ch["canton"].map(cantons_dict)

source_per_canton = clean_energy_ch.groupby('canton_name').size().reset_index(name="count")

fig = px.choropleth_mapbox(source_per_canton,
                           geojson=cantons,
                           featureidkey="properties.kan_name",
                           locations='canton_name',
                           color="count",
                           opacity=0.8,
                           width=900,
                           height=500,
                           center={"lat": 46.8, "lon": 8.3},
                           mapbox_style="open-street-map",
                           zoom=6.5,
                           color_continuous_scale="Cividis",
                           title='<b>Number of Clean Energy Sources per Canton</b>',
                           labels={"canton_name": "Canton ",
                                   "count": "Number of Sources "},
                           )

fig.update_layout(margin={"r": 30, "t": 30, "l": 0, "b": 30},
                  font={"color": "midnight blue",
                        'family': 'verdana'},
                  title = {'x' : 0},

                  )

st.plotly_chart(fig)

capacity_per_source = clean_energy_ch.groupby('energy_source_level_2').agg('electrical_capacity').sum().reset_index(name="total_capacity")


fig1 = px.bar(capacity_per_source,
              x='energy_source_level_2',
              y='total_capacity',
              title='<b>Total capacity by source<b>',
              color="energy_source_level_2",
              color_discrete_map={'Bioenergy': 'rgb(29, 105, 150)',
                                  'Hydro': 'rgb(82, 106, 131)',
                                  'Solar': 'rgb(217, 175, 107)',
                                  'Wind': 'teal', },
              labels={"energy_source_level_2": "Source ",
                      "total_capacity": "Total capacity "},

              )

fig1.update_layout(
    xaxis_title="Source",
    yaxis_title="Total capacity",
    font={"color": "midnight blue",
          'family': 'verdana'},
    legend_title='Legend',
    plot_bgcolor='white',

)

st.plotly_chart(fig1)

contract_enddate = clean_energy_ch.groupby([ 'contract_period_end']).agg(
    count_contract = ('contract_period_end','count')).reset_index()

contract_enddate_sorted = contract_enddate.sort_values('contract_period_end', ascending = True)



fig2 = px.bar(contract_enddate_sorted,
              x='contract_period_end',
              y='count_contract',
              title='<b>Contract enddate<b>',
              color="count_contract",
              color_continuous_scale="Cividis",
              # color_discrete_map = 'rgb(82, 106, 131)',

              )

fig2.update_layout(
    xaxis_title="Contract enddate",
    yaxis_title="Count contract",
    font={"color": "midnight blue",
          'family': 'verdana'},
    legend_title='Legend',
    plot_bgcolor='white',

)

st.plotly_chart(fig2)