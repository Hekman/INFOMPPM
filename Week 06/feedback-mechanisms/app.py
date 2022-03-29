import streamlit as st
import pandas as pd
import template as t
import authenticate as a
import json
from itertools import cycle
from random import random

st.set_page_config(layout="wide")

# the simpsons episodes
df = pd.read_json('episodes.json')

df_users = pd.read_json('users.json')

# open the activities json file
with open('activities.json') as json_file:
  users_activities = json.load(json_file)

# create a session state
if 'season' not in st.session_state:
  st.session_state['season'] = 1

if 'episode' not in st.session_state:
  st.session_state['episode'] = 'tt0348034'

if 'user' not in st.session_state:
  st.session_state['user'] = 0

if 'activities' not in st.session_state:
  st.session_state['activities'] = users_activities

#authenticate
a.authenticate()

# get seasons
seasons = pd.unique(df['season'].sort_values(ascending=True))

# retrieve season and episode from session state
df_season = df[df['season'] == st.session_state['season']]
df_episode = df[df['id'] == st.session_state['episode']]
df_episode = df_episode.iloc[0]

col1, col2 = st.columns(2)

with col1:
  st.image(df_episode['image'], use_column_width='always')

with col2:
  st.title(df_episode['title'])
  st.caption(df_episode['airdate'])
  st.markdown(df_episode['summary'])
  st.caption('Season ' + str(df_episode['season']) + ' | episode ' + str(df_episode['episode']) + ' | Rating ' + str(df_episode['rating']) + ' | ' + str(df_episode['votes']) + ' votes')

with st.expander('Implicit and Explicit feedback'):
  st.button('👍', key=random(), on_click=t.activity, args=(df_episode['id'], 'Like' ))  
  st.button('👎', key=random(), on_click=t.activity, args=(df_episode['id'], 'Dislike'))  

with st.expander("Seasons"):
  cols = cycle(st.columns(14))
  for season in seasons:
    next(cols).button(str(season), key=season, on_click=t.select_season, args=(season, ))

with st.expander("Random episodes in this season"):
  t.tiles(df_season.sample(6))