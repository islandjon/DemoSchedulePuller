# this script will pull the schedule of the soccer games from the website
"""
This script pulls the schedule of soccer games from a website and places it into a pandas DataFrame. The data is then filtered and a PDF is produced for each age group.
Functions:
- extract_group_schedule_links(response_text): Extracts the group schedule links from the response text.
- check_links(base_url, links): Checks each link to see if the page exists.
- extract_game_schedule(response_text): Extracts the game schedule data from the response text.
- parse_team_info(team_string): Parses the team information from a team string.
- update_table(selected_teams, selected_age_groups): Updates the table based on selected teams and age groups.
- export_to_calendar(n_clicks, table_data): Exports the filtered schedule to a calendar.
Variables:
- url: The URL of the website to pull the schedule from.
- response: The response from the website.
- response_text: The text content of the response.
- base_url: The base URL of the website.
- group_schedule_links: The links to the group schedules.
- valid_links: The valid links to the group schedules.
- all_games_data: The extracted game schedule data from each valid link.
- df: The DataFrame containing the game schedule data.
- display_columns: The columns to display in the table.
- app.layout: The layout of the Dash app.
"""
# and place into a pandas dataframe. The data will then be filtered and a PDF will be produced with each age groups

# Import the necessary libraries
import datetime
import flask
import requests
from bs4 import BeautifulSoup
import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import re
from ics import Calendar, Event

# initialize the Dash app using Flask
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

def extract_group_schedule_links(response_text):
    """
    Extracts the links to group schedules from the given response text.

    Parameters:
    response_text (str): The HTML response text.

    Returns:
    list: A list of group schedule links.
    """
    soup = BeautifulSoup(response_text, 'html.parser')
    group_links = []
    for link in soup.find_all('a', href=True):
        if 'Group Schedules' in link.text:
            group_links.append(link['href'])
    return group_links


def check_links(base_url, links):
    """
    Check the validity of links by sending HTTP requests to each link.

    Args:
        base_url (str): The base URL to construct the full URL.
        links (list): A list of links to check.

    Returns:
        list: A list of valid links.

    Raises:
        requests.exceptions.RequestException: If there is an error while sending the HTTP request.

    """
    # Rest of the code...
    valid_links = []
    for link in links:
        for page in ['1','2']:
            full_url = base_url + link + f'?page={page}'  # Construct the full URL
            try:
                response = requests.get(full_url)
                if response.status_code == 200:
                    # print(f"Page exists: {full_url}")
                    valid_links.append(full_url)
                else:
                    # print(f"Page does not exist or returned a non-200 status: {full_url}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to reach {full_url}: {e}")
    return valid_links


def extract_game_schedule(response_text):
    """
    Extracts game schedule data from the given HTML response text.
    Args:
        response_text (str): The HTML response text containing the game schedule.
    Returns:
        list: A list of dictionaries, where each dictionary represents a game and contains the following keys:
            - 'GAME': The game reference.
            - 'DATE/TIME': The date and time of the game.
            - 'HOME': The home team.
            - 'AWAY': The away team.
            - 'LOCATION': The location of the game.
            - 'SURFACE': The surface of the game.
    """
    # Code implementation goes here
    pass
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response_text, 'html.parser')
    # Find all the rows in the schedule table
    games_rows = soup.find_all('div', class_='games-row')
    # Initialize a list to store the extracted data
    games_data = []
    # Iterate over each row to extract relevant details
    for row in games_rows:
        if row.find('div', class_='game-ref') is None:
            continue
        game_ref = row.find('div', class_='game-ref').text.strip()
        # Clean up and format the date and time
        month = row.find('div', class_='month').text.strip()
        day = row.find('div', class_='day').text.strip()
        time = row.find('div', class_='time').text.strip()
        date_time_str = f"{month} {day} {time} 2024"  # Assuming year is 2024
        date_time_obj = pd.to_datetime(date_time_str, format='%b %d %I:%M %p %Y')

        home_team = row.find('div', class_='game-home').text.strip()
        away_team = row.find('div', class_='game-away').text.strip()
        location = row.find(
            'div', class_='game-location').text.strip().replace('MAP', '').strip()
        surface = row.find(
            'div', class_='game-surface').text.strip().replace('OPEN', '').strip()

        # Append extracted data to the list
        games_data.append({
            'GAME': game_ref,
            'DATE/TIME': date_time_obj,
            'HOME': home_team,
            'AWAY': away_team,
            'LOCATION': location,
            'SURFACE': surface
        })
    return games_data
    

# Define the URL
url = 'https://app.demosphere.com/_widgets/v1/seasonal_schedule/66c33ac190249400089a06e3/groupings'

# Send a request to the website
response = requests.get(url)

# Check the status code
if response.status_code == 200:
    # print('The request was successful')
    response_text = response.text
else:
    print('The request was unsuccessful')

base_url = "https://app.demosphere.com"  # Replace with the correct base URL

# Step 1: Extract the group schedule links
group_schedule_links = extract_group_schedule_links(response_text)

# Step 2: Check each link to see if the page exists
valid_links = check_links(base_url, group_schedule_links)

# Step 3: Extract the game schedule data from each valid link
all_games_data = []
for link in valid_links:
    response = requests.get(link)
    if response.status_code == 200:
        games_data = extract_game_schedule(response.text)
        all_games_data.extend(games_data)

# Step 4: Create a DataFrame from the extracted data
df = pd.DataFrame(all_games_data)

df = df.sort_values(by='DATE/TIME')

# Function to parse team info
def parse_team_info(team_string):
    match = re.match(r'^(?P<League>\w+)\s(?P<Gender>[BG])-(?P<AgeGroup>U\d+|\d+U)-(?P<TeamName>.+)$', team_string)
    if match:
        info = match.groupdict()
        info['AgeGroup'] = f"{info['Gender']}-{info['AgeGroup'].replace('U', '')}U"
        return info
    return {"League": "", "Gender": "", "AgeGroup": "", "TeamName": ""}

# Apply parsing to HOME and AWAY teams
home_team_info = df['HOME'].apply(parse_team_info)
away_team_info = df['AWAY'].apply(parse_team_info)

# Convert to DataFrame and merge with the main DataFrame
home_team_df = pd.DataFrame(home_team_info.tolist(), index=df.index)
away_team_df = pd.DataFrame(away_team_info.tolist(), index=df.index)

df = df.join(home_team_df.add_prefix('HOME_')).join(away_team_df.add_prefix('AWAY_'))
# Sort the DataFrame by 'DATE/TIME'
df = df.sort_values(by='DATE/TIME')

# Only keep the original columns for display
display_columns = ["GAME", "DATE/TIME", "HOME", "AWAY", "LOCATION", "SURFACE"]

# App layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(html.H1("Soccer Schedule", className="text-center my-4"))
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="team-filter",
                    options=[{"label": team, "value": team} for team in sorted(list(set(df["HOME"].unique().tolist() + df["AWAY"].unique().tolist())))],
                    placeholder="Filter by Team (Home or Away)",
                    multi=True,
                ),
                width=6,
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="age-group-filter",
                    options=[{"label": age_group, "value": age_group} for age_group in sorted(df["HOME_AgeGroup"].unique())],
                    placeholder="Filter by Age Group",
                    multi=True,
                ),
                width=6,
            )
        ),
        dbc.Row(
            dbc.Col(
                dash_table.DataTable(
                    id="schedule-table",
                    columns=[{"name": col, "id": col} for col in display_columns],
                    data=df[display_columns].to_dict("records"),
                    sort_action="native",
                    page_action="none",  # Remove paging
                    style_table={'overflowY': 'auto', 'height': '600px'},  # Optional: Add vertical scrolling
                    style_cell={
                        'textAlign': 'left', 
                        'minWidth': '100px', 
                        'maxWidth': '200px', 
                        'whiteSpace': 'normal'
                    },
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    style_as_list_view=True,
                ),
                width=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Export to Calendar", id="export-button", color="primary", className="mt-4")
            )
        ),
        dcc.Download(id="download-calendar"),
    ],
    fluid=True,
)

# Callback to update table based on filters
@app.callback(
    Output("schedule-table", "data"),
    [Input("team-filter", "value"), Input("age-group-filter", "value")]
)
def update_table(selected_teams, selected_age_groups):
    filtered_df = df

    if selected_teams:
        filtered_df = filtered_df[
            filtered_df["HOME"].isin(selected_teams) | filtered_df["AWAY"].isin(selected_teams)
        ]

    if selected_age_groups:
        filtered_df = filtered_df[
            filtered_df["HOME_AgeGroup"].isin(selected_age_groups) | filtered_df["AWAY_AgeGroup"].isin(selected_age_groups)
        ]

    return filtered_df[display_columns].to_dict("records")

# Callback to export the filtered schedule to a calendar
@app.callback(
    Output("download-calendar", "data"),
    [Input("export-button", "n_clicks")],
    State("schedule-table", "data")
)
def export_to_calendar(n_clicks, table_data):
    if n_clicks is None:
        return dash.no_update
     
    calendar = Calendar()
    
    for row in table_data:
        event = Event()
        event.name = f"{row['HOME']} vs {row['AWAY']}"
        event.begin =  datetime.datetime.strptime(row['DATE/TIME'], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(hours=4)

        if "U6" in row['HOME'] or "6U" in row['HOME']:
            # convert to datetime object and add 50 minutes
            event.end = event.begin + datetime.timedelta(minutes=50)
        elif "U8" in row['HOME'] or "8U" in row['HOME']:
            event.end = event.begin + pd.Timedelta(minutes=50)
        elif "U10" in row['HOME'] or "U12" in row['HOME'] or "10U" in row['HOME'] or "12U" in row['HOME']:
            event.end = event.begin + pd.Timedelta(hours=1)
        elif "U15" in row['HOME'] or "15U" in row['HOME']:
            event.end = event.begin + pd.Timedelta(hours=1, minutes=10)
        elif "U19" in row['HOME'] or "19U" in row['HOME']:
            event.end = event.begin + pd.Timedelta(hours=1, minutes=20)
        event.location = row['LOCATION']
        event.description = (
            f"Game ID: {row['GAME']}\n"
            f"Date/Time: {row['DATE/TIME']}\n"
            f"Home Team: {row['HOME']}\n"
            f"Away Team: {row['AWAY']}\n"
            f"Location: {row['LOCATION']}\n"
            f"Surface: {row['SURFACE']}"
        )
        calendar.events.add(event)
    
    # Convert the calendar to a string and encode it as bytes
    calendar_str = str(calendar.serialize())
    calendar_bytes = calendar_str.encode("utf-8")
    
    return dcc.send_bytes(calendar_bytes, "soccer_schedule.ics")

if __name__ == '__main__':
    app.run_server(debug=False)
