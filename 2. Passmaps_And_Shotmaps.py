
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:56:07 2020

@author: lindelwemoyo
"""

#Load in Statsbomb competition and match data
#This is a library for loading json files.
import json

#Import the function to draw pitch
import matplotlib.pyplot as plt
import numpy as np

#Load the competition file
#Got this by searching 'how do I open json in Python'
with open('/Users/lindelwemoyo/Data Projects/SoccermaticsForPython1/Statsbomb/data/competitions/competitions.json') as f:
    competitions = json.load(f)
    
#Mens World Cup 2019 has competition ID 43
competition_id=43

#Load the list of matches for this competition
with open('/Users/lindelwemoyo/Data Projects/SoccermaticsForPython1/Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)

#size of the pitch
pitchLengthX=120
pitchWidthY=80

#Findmatchid
home_team_required = "France"
away_team_required = "Argentina"
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==home_team_required) and (away_team_name==away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id:' + str(match_id_required))
    
#ID for Fra Argentina match
match_id_required = 7580
home_team_required = "France"
away_team_required = "Argentina"

#Load in the data
file_name = str(match_id_required)+'.json'

#Load in all match events
import json
with open ('/Users/lindelwemoyo/Data Projects/SoccermaticsForPython1/Statsbomb/data/events/'+file_name) as data_file:
    #print (mypath+'events/'+file)
    data = json.load(data_file)

#get nested structure into a dataframe
#store the dataframe in a dictionary with the match id as key (remove .json from string)
from pandas.io.json import json_normalize
df = json_normalize(data, sep = "_").assign(match_id=file_name[:-5])

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')

#Draw the pitch
from FCPython import createPitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')

#PlotTheShots
for i,shot in shots.iterrows():
    x = shot['location'][0]
    y = shot['location'][1]
    
    goal = shot['shot_outcome_name'] == 'Goal'
    team_name =shot['team_name']
    
    circleSize=2
    circleSize=np.sqrt(shot['shot_statsbomb_xg']*15)


    if (team_name==home_team_required):
        if goal:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")
            plt.text((x+1),pitchWidthY-y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
    elif (team_name==away_team_required):
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue") 
            plt.text((pitchLengthX-x+1),y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
            shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)

plt.text(5,75,away_team_required + ' shots')
plt.text(80,75,home_team_required + ' shots')

#passes
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')
#Draw pitch
(fig,ax) = createPitch(pitchLengthX,pitchWidthY,'yards','gray')
for i,thepass in passes.iterrows():
    if thepass['player_name']=='Paul Pogba':
        x=thepass['location'][0]
        y=thepass['location'][1]
        passCircle=plt.Circle((x,pitchWidthY-y),2,color='blue')
        passCircle.set_alpha(.2)
        ax.add_patch(passCircle)
        dx=thepass['pass_end_location'][0]-x
        dy=thepass['pass_end_location'][1]-y
        passArrow=plt.Arrow(x,pitchWidthY-y,dx,dy,width=3,color='blue')
        ax.add_patch(passArrow)
plt.text(5,75,'Pogba passes v Argentina                  2018 World Cup')
        
fig.set_size_inches(10,7)
fig.savefig('Output/passes.pdf', dpi=100)
plt.show()     




    

        
    
    
    
    
    
    