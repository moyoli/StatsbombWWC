#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 13:56:00 2020

@author: lindelwemoyo
"""

from pandas.io.json import json_normalize
from utils import read_json

lineups_path = "/Users/lindelwemoyo/Data Projects/SoccermaticsForPython1/Statsbomb/data/lineups/{0}.json"
events_path = "/Users/lindelwemoyo/Data Projects/SoccermaticsForPython1/Statsbomb/data/events/{0}.json"

team_name = "Portugal"
match_id = 7576

#STEP 1: Read data
lineups = read_json(lineups_path.format(match_id))
names_dict = {player["player_name"]: player["player_nickname"]
              for team in lineups for player in team["lineup"]}
names_dict

events = read_json(events_path.format(match_id))
df_events = json_normalize(events, sep="_").assign(match_id=match_id)
df_events.head(5)

import pandas as pd
df_events = pd.json_normalize(events, sep="_").assign(match_id=match_id)
df_events.head(5)

#step 2: compute max minutes
first_red_card_minute = df_events[df_events.foul_committed_card_name.isin(["Second Yellow", "Red card"])].minute.min()
first_substitution_minute = df_events[df_events.type_name == "Substitution"].minute.min()
max_minute=df_events.minute.max()

num_minutes = min(first_substitution_minute, first_red_card_minute, max_minute)
num_minutes

#step 3: set text information
plot_name = "statsbomb_match{0}_{1}".format(match_id, team_name)

opponent_team = [x for x in df_events.team_name.unique() if x != team_name][0]
plot_title = "{0}'s passing network vs {1} (Statsbomb event data)".format(team_name, opponent_team)
plot_legend = "Location: pass origin\nSize: number of passes\nColor: number of passes"

#step4 prepare data
def _statsbomb_to_point(location, max_width=120, max_height=80):
    #convert a points coordinates from StatsBomb range to 0-1 range
    return location[0] / max_width, 1-(location[1] / max_height)

df_passes = df_events[(df_events.type_name == "Pass") &
                      (df_events.pass_outcome_name.isna()) &
                      (df_events.team_name ==  team_name) &
                      (df_events.minute < num_minutes)].copy()

df_passes["pass_recipient_name"] = df_passes.pass_recipient_name.apply(lambda x: names_dict[x] if names_dict[x] else x)
df_passes["player_name"] = df_passes.player_name.apply(lambda x: names_dict[x] if names_dict[x] else x)
df_passes.head()

df_passes["origin_pos_x"] = df_passes.location.apply(lambda x: _statsbomb_to_point(x)[0])
df_passes["origin_pos_y"] = df_passes.location.apply(lambda x: _statsbomb_to_point(x)[1])
player_position = df_passes.groupby("player_name").agg({"origin_pos_x": "median", "origin_pos_y": "median"})

player_position

player_pass_count = df_passes.groupby("player_name").size().to_frame("num_passes")
player_pass_count = df_passes.groupby("player_name").size().to_frame("pass_value")
player_pass_count

df_passes["pair_key"] = df_passes.apply(lambda x: "_".join(sorted([x["player_name"], x["pass_recipient_name"]])),axis=1)
pair_pass_count=df_passes.groupby("pair_key").size().to_frame("num_passes")
pair_pass_value = df_passes.groupby("pair_key").size().to_frame("pass_value")
pair_pass_count.head()

from visualization.passing_network import draw_pitch, draw_pass_map
import matplotlib.pyplot as plt

ax = draw_pitch()
ax = draw_pass_map(ax, player_position, player_pass_count, player_pass_value, )







