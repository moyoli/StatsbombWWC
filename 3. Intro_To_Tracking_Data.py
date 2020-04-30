#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:50:20 2020

@author: lindelwemoyo
"""

import Metrica_IO as mio
import Metrica_Viz as mviz

#set up path to data
DATADIR = '/Users/lindelwemoyo/Data Projects/SoccermaticsForPython2/sample-data-master/data'
game_id =2

#read in event data
events=mio.read_event_data(DATADIR,game_id)

#number of events of each event type
events['Type'].value_counts()

#housekeeping
events=mio.to_metric_coordinates(events)

#getting events by team
home_events=events[events['Team']=='Home']
away_events=events[events['Team']=='Away']

#frequency of events
home_events['Type'].value_counts()
away_events['Type'].value_counts()

#get all shots
shots = events[events['Type']=='SHOT']
home_shots = home_events[home_events.Type=='SHOT']
away_shots = away_events[away_events.Type=='SHOT']

#Frequency of shots or "SSTV stats"
home_shots['Subtype'].value_counts()
away_shots['Subtype'].value_counts()

#Count shots taken by each player
home_shots['From'].value_counts()
away_shots['From'].value_counts()

#select only goals
home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

#add minutes to df
home_goals['Minute'] = home_goals['Start Time [s]']/60
away_goals['Minute'] = away_goals['Start Time [s]']/60


#Plot the first goal
import numpy as np
import matplotlib as plt
fig,ax = mviz.plot_pitch()
ax.plot( events.loc[198]['Start X'], events.loc[198]['Start Y'], 'ro')
ax.annotate("", xy=events.loc[198][['End X','End Y']], xytext=events.loc[198][['Start X','Start Y']], alpha=0.6, arrowprops=dict(arrowstyle="->",color='r'))

#plot passing move leading up to goal
mviz.plot_events( events.loc[190:198], indicators= ['Marker','Arrow'], annotate=False)

#rEADING IN TRACKING DATA
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

#check out column names
tracking_home.colums

#convert positions from metrica units to meters
tracking_home=mio.to_metric_coordinates(tracking_home)
tracking_away=mio.to_metric_coordinates(tracking_away)

#Plot player trajectories over opening minute (Players 11,1,2,3,4) 
#60 seconds x 25 observations per seconds = 1500 frames
fig,ax = mviz.plot_pitch()
ax.plot( tracking_home['Home_11_x'].iloc[:1500], tracking_home['Home_11_y'].iloc[:1500], 'r.', MarkerSize=1)
ax.plot( tracking_home['Home_1_x'].iloc[:1500], tracking_home['Home_1_y'].iloc[:1500], 'b.', MarkerSize=1)
ax.plot( tracking_home['Home_2_x'].iloc[:1500], tracking_home['Home_2_y'].iloc[:1500], 'g.', MarkerSize=1)
ax.plot( tracking_home['Home_3_x'].iloc[:1500], tracking_home['Home_3_y'].iloc[:1500], 'y.', MarkerSize=1)
ax.plot( tracking_home['Home_4_x'].iloc[:1500], tracking_home['Home_4_y'].iloc[:1500], 'c.', MarkerSize=1)

#plot player positions at kickoff
KO_Frame = events.loc[0]['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[KO_Frame], tracking_away.loc[KO_Frame])

#alternatively
fig,ax = mviz.plot_frame( tracking_home.loc[51], tracking_away.loc[51])

#plotting player positions at first goal
fig,ax = mviz.plot_events( events.loc[198:198], indicators = ['Marker','Arrow'], annotate=True)
goal_frame = events.loc[198]['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[goal_frame], tracking_away.loc[goal_frame], figax=(fig,ax))

#Homework
#Q1. Plot passes and shots leading up to goal 2

#first gets all shots and goals
shots = events[events['Type']=='SHOT']
goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()
print(goals)

#Leading up to 2nd goal
mviz.plot_events( events.loc[818:823], indicators= ['Marker','Arrow'], annotate=True, color='b')

#Leading up to 3rd goal
mviz.plot_events( events.loc[1109:1118], indicators= ['Marker','Arrow'], annotate=True, color='r')

#filter out non pass and non shot events to make GOAL 3 clearer
passes_and_shots = events[events['Type'].isin(['SHOT','PASS'])]
mviz.plot_events( passes_and_shots.loc[1109:1118], indicators= ['Marker','Arrow'], annotate=True, color='r')

# All shots by player 9, goals differentiated by symbol&transparency

home_player9_shots = events[ (events['Type']=='SHOT') & (events.Team=='Home') & (events.From=='Player 9') ]

home_player9_shots_goal = home_player9_shots[home_player9_shots['Subtype'].str.contains('-GOAL')].copy()
home_player9_shots_nogoal = home_player9_shots[~home_player9_shots['Subtype'].str.contains('-GOAL')].copy()

fig,ax = mviz.plot_events( home_player9_shots_goal, indicators = ['Marker','Arrow'], annotate=False, color='g', alpha=1, marker_style='s' )
mviz.plot_events( home_player9_shots_nogoal, figax=(fig,ax), indicators = ['Marker','Arrow'], annotate=False, color='r', alpha=0.2, marker_style='o' )
fig.suptitle("Home team player 9 shots",y=0.92)

#Q3 Position of players at Number 9's goal
#read in tracking data
tracking_home = mio.tracking_data(DATADIR,game_id,'Home')
tracking_away = mio.tracking_data(DATADIR,game_id,'Away')

#convert positions from metrica units to meters
tracking_home=mio.to_metric_coordinates(tracking_home)
tracking_away=mio.to_metric_coordinates(tracking_away)

goal_rame = home_player9_shots_goal['Start Frame']
fig,ax = mviz.plot_frame( tracking_home.loc[goal_frame], tracking_away.loc[goal_frame],PlayerAlpha=0.3)
fig,ax = mviz.plot_events( home_player9_shots_goal, figax=(fig,ax), indicators = ['Marker','Arrow'], annotate=True )

#Q4 Calculating how far players ran
import pandas as pd
import Metrica_Velocities as mvel
tracking_home = mvel.calc_player_velocities(tracking_home,filter_= 'moving average')
tracking_away = mvel.calc_player_velocities(tracking_away,filter_= 'moving average')

#look through home and away teams separately
teams = ['Home','Away']
data = [tracking_home, tracking_away]
for name, data in zip(teams, data):
    team_players = np.unique( [c.split('_')[1] for c in data.columns if c[:4] == name] )
    team_summary = pd.DataFrame(index=team_players)

#calc total distance covered by each player
    distance=[]
    for player in team_summary.index:
        column = name + '_' + player + '_speed'
        player_distance = data[column].sum()/25./1000
        distance.append( player_distance)
        
    team_summary['Distance [km]'] = distance
    team_summary = team_summary.sort_values(['Distance [km]'],ascending=False)
    
    print("***** " + name + "team summary *****")
    print(team_summary)
    #make a simple bar chart of distance covered for each player
    fig,ax = plt.subplots()
    ax=team_summary['Distance [km]'].plot.bar(rot=0)
    ax.set_xlabel('Player')
    ax.set_ylabel('Distance covered [km]')
    fig.suptitle(name + ' Team',y=0.95)
