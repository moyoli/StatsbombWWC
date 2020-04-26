#Load in Statsbomb competition and match data
#This is a library for loading json files.
import json

#Load the competition file
#Got this by searching 'how do I open json in Python'
with open('Statsbomb/data/competitions/competitions.json') as f:
    competitions = json.load(f)
    
#Mens World Cup 2019 has competition ID 43
competition_id=43

#Load the list of matches for this competition
with open('Statsbomb/data/matches/'+str(competition_id)+'/3.json') as f:
    matches = json.load(f)

#Look inside matches
matches[0]
matches[43]['home_team']
matches[27]['home_team']['home_team_name']
matches[51]['away_team']['away_team_name']

#Print all match results
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name=='Sweden' or away_team_name=='Sweden'):
        home_score=match['home_score']
        away_score=match['away_score']
        describe_text = 'The match between ' + home_team_name + ' and ' + away_team_name
        result_text = ' finished ' + str(home_score) +  ' : ' + str(away_score)
        print(describe_text + result_text)

#Now lets find a match we are interested in
home_team_required ="Nigeria"
away_team_required ="Argentina"

#Find ID for the match
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==home_team_required) and (away_team_name==away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id:' + str(match_id_required))
        
#Exercise: 
#1, Edit the code above to print out the result list for the Mens World cup
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    home_score=match['home_score']
    away_score=match['away_score']
    full_description = 'Match between ' + home_team_name + ' and ' + away_team_name + ' ended' + str(home_score) + " : " + str(away_score)
    print(full_description)


#2, Edit the code above to find the ID for England vs. Sweden
home_team_required = "Brazil"
away_team_required = "Mexico"
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==home_team_required) and (away_team_name==away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id:' + str(match_id_required))

#3, Write new code to write out a list of just Sweden's results in the tournament.
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name=='Sweden' or away_team_name=='Sweden'):
        home_score=match['home_score']
        away_score=match['away_score']
        full_description = 'Match between ' + home_team_name + ' and ' + away_team_name + ' ended' + str(home_score) + " : " + str(away_score)
        print(full_description)

#4 Find stadium name
home_team_required = "Brazil"
away_team_required = "Mexico"
for match in matches:
    home_team_name=match['home_team']['home_team_name']
    away_team_name=match['away_team']['away_team_name']
    if (home_team_name==home_team_required) and (away_team_name==away_team_required):
        match_date_required = match['match_date']
print(home_team_required + ' vs ' + away_team_required + ' was played on:' + str(match_date_required))

