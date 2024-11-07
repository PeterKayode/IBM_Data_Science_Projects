import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [str(i) for i in range(1980, 2024)]

# Create the layout of the app
app.layout = html.Div([
    html.H1("Automobile Statistics Dashboard"),
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='select-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics'
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value='1980'
        )
    ]),
    html.Div(id='output-container')
])

# Callback for updating the output container based on selected statistics and year
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-statistics', component_property='value'), Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))
        
        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby(['Vehicle_Type'])['Automobile_Sales'].mean().reset_index()                           
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles Sold by Vehicle Type during Recession"))
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Expenditure Share by Vehicle Type during Recession'))
        
        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        R_chart4 = html.Div()
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1), html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3), html.Div(children=R_chart4)])
        ]
    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == int(input_year)]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales'))
        
        # Plot 2: Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph()
        
        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type in {}'.format(input_year)))
        
        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure by Vehicle Type in {}'.format(input_year)))
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)])
        ]
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
