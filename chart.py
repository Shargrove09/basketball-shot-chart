from nba_api.stats.endpoints import shotchartdetail
import json
import requests
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

# Load teams file
teams = json.loads(requests.get(
  'https://raw.githubusercontent.com/bttmly/nba/master/data/teams.json').text)

# Load players file
players = json.loads(requests.get(
  'https://raw.githubusercontent.com/bttmly/nba/master/data/players.json').text)

#Get user input 
user_input_first_name = input("Type the player's first name that you're looking: ")#'Stephen'
user_input_last_name = input("Type the player's last name that you're looking: ") #'Curry'
user_input_team_name = input("Type the team's name that you are looking for: ") #'Golden State Warriors'
user_input_season = input("Enter the season you are looking for: ") #'2015-16'

# Get team ID based on team name
def get_team_id(teamName): 
	for team in teams: 
		if team['teamName'] == teamName: 
			return team['teamId']
		elif team['simpleName'] == teamName: 
			return team['teamId']
	return -1


# Get player ID based on player name
# May need to account for case-sensitive errors
def get_player_id(first, last):
  for player in players:
    if player['firstName'] == first and player['lastName'] == last:
      return player['playerId']
  return -1

#JSON request
'''
shot_json = shotchartdetail.ShotChartDetail(team_id=get_team_id('Golden State Warriors'), player_id= get_player_id('Stephen', 'Curry' ), context_measure_simple='PTS',
season_nullable='2021-22',season_type_all_star='Regular Season') '''


shot_json = shotchartdetail.ShotChartDetail(team_id=get_team_id(user_input_team_name), player_id= get_player_id(user_input_first_name, user_input_last_name ), context_measure_simple='PTS',
season_nullable=user_input_season,season_type_all_star='Regular Season') 

#Load data into dictionary
shot_data = json.loads(shot_json.get_json())

#get data from dictionary
relevant_data = shot_data['resultSets'][0]

#get headers and row data 
headers = relevant_data['headers']
rows = relevant_data['rowSet']

#Create pandas DataFrame 
curry_data = pd.DataFrame(rows)
curry_data.columns = headers

#Creating a Basketball Court 

def create_court(ax, color):
    
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)
    
    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))
    
    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))
    
    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))
    
    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    
    return ax



#General plot parameters
mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 18
mpl.rcParams['axes.linewidth'] = 2

#Draw basketball court 
fig = plt.figure(figsize=(4,3.76)) 
#Set window name to player name and season
fig.canvas.manager.set_window_title(f'{user_input_first_name} {user_input_last_name} {user_input_season} Season Shooting')
ax = fig.add_axes([0,0,1,1])
ax = create_court(ax, 'black')

# Plot hexbin of shots with logarithmic binning
ax.hexbin(curry_data['LOC_X'], curry_data['LOC_Y'] + 60, gridsize=(30, 30), extent=(-300, 300, 0, 940), bins='log', cmap='Blues',zorder=-1)

#Annotate player name and season 
#ax.text(0, 0.5, 'Stephen Curry\n2015-16 Regular Season', transform=ax.transAxes, ha='left', va='baseline')


plt.savefig('ShotChart.png', dpi=300, bbox_inches='tight')
plt.show()






