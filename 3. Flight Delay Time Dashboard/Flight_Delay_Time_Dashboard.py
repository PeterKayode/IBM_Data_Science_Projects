# This interactive dashboard provides insights into the average delay times 
# experienced by airlines, categorized by different types of delays. Explore the visualizations below to understand how various factors 
# such as carrier delays, weather conditions, NAS delays, security-related issues, and late aircraft arrivals impact flight schedules.
# Simply input a specific year using the field below, and the dashboard will dynamically update to display the delay statistics for 
# that year. Gain valuable insights into airline performance trends and factors influencing flight delays.



# Import required libraries
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into a pandas dataframe
airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                           encoding="ISO-8859-1",
                           dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                  'Div2Airport': str, 'Div2TailNum': str})

# Create a Dash application
app = dash.Dash(__name__)

# Description of the dashboard
description_text = '''
                    Welcome to the Flight Delay Time Statistics Dashboard! This interactive dashboard provides insights into the average delay times 
                    experienced by airlines, categorized by different types of delays. Explore the visualizations below to understand how various factors 
                    such as carrier delays, weather conditions, NAS delays, security-related issues, and late aircraft arrivals impact flight schedules.
                    Simply input a specific year using the field below, and the dashboard will dynamically update to display the delay statistics for 
                    that year. Gain valuable insights into airline performance trends and factors influencing flight delays.
                    '''

# Build the Dash app layout
app.layout = html.Div(children=[
    # Description section
    html.Div([
        html.H1('Flight Delay Time Statistics', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),
        html.P(description_text, style={'textAlign': 'center', 'font-size': 18, 'margin': 'auto', 'width': '80%'}),
        html.Br(),
        html.Br(),
        html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', style={'height':'35px', 'font-size': 30})], style={'textAlign': 'center', 'font-size': 30}),
        html.Br(),
        html.Br()
    ]),
    # Delay statistics visualization section
    html.Div([
        html.Div([
            html.Div(dcc.Graph(id='carrier-plot')),
            html.Div(dcc.Graph(id='weather-plot'))
        ], style={'display': 'flex'}),
        html.Div([
            html.Div(dcc.Graph(id='nas-plot')),
            html.Div(dcc.Graph(id='security-plot'))
        ], style={'display': 'flex'}),
        html.Div(dcc.Graph(id='late-plot'), style={'width':'65%'})
    ])
])

# Function to compute delay statistics
def compute_info(airline_data, entered_year):
    # Select data for the entered year
    df =  airline_data[airline_data['Year'] == int(entered_year)]
    # Compute average delay times for different types of delays
    avg_carrier_delay = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather_delay = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_nas_delay = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_security_delay = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late_aircraft_delay = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_carrier_delay, avg_weather_delay, avg_nas_delay, avg_security_delay, avg_late_aircraft_delay

# Callback decorator to update plots based on user input
@app.callback([
    Output(component_id='carrier-plot', component_property='figure'),
    Output(component_id='weather-plot', component_property='figure'),
    Output(component_id='nas-plot', component_property='figure'),
    Output(component_id='security-plot', component_property='figure'),
    Output(component_id='late-plot', component_property='figure')
], [Input(component_id='input-year', component_property='value')])
def update_graph(entered_year):
    # Compute delay statistics for the entered year
    avg_carrier_delay, avg_weather_delay, avg_nas_delay, avg_security_delay, avg_late_aircraft_delay = compute_info(airline_data, entered_year)
    
    # Line plot for carrier delay
    carrier_fig = px.line(avg_carrier_delay, x='Month', y='CarrierDelay', color='Reporting_Airline', title='Average Carrier Delay Time (minutes) by Airline')
    # Line plot for weather delay
    weather_fig = px.line(avg_weather_delay, x='Month', y='WeatherDelay', color='Reporting_Airline', title='Average Weather Delay Time (minutes) by Airline')
    # Line plot for NAS delay
    nas_fig = px.line(avg_nas_delay, x='Month', y='NASDelay', color='Reporting_Airline', title='Average NAS Delay Time (minutes) by Airline')
    # Line plot for security delay
    security_fig = px.line(avg_security_delay, x='Month', y='SecurityDelay', color='Reporting_Airline', title='Average Security Delay Time (minutes) by Airline')
    # Line plot for late aircraft delay
    late_aircraft_fig = px.line(avg_late_aircraft_delay, x='Month', y='LateAircraftDelay', color='Reporting_Airline', title='Average Late Aircraft Delay Time (minutes) by Airline')
    
    return carrier_fig, weather_fig, nas_fig, security_fig, late_aircraft_fig

# Run the app
if __name__ == '__main__':
    app.run_server()
