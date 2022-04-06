# John Zhu

# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
#import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# List of years 
site_list = spacex_df['Launch Site'].unique()

#siteList = [{'label': i, 'value': i} for i in spacex_df['Launch Site'].unique()]
#siteList.insert(0,{'label': 'All', 'value': 'All'})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                 options=[
                                     {'label':'All Sites','value':'ALL'},
                                     {'label':'CCAFS LC-40','value':'CCAFS LC-40'},
                                     {'label':'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                     {'label':'KSC LC-39A','value':'KSC LC-39A'},
                                     {'label':'VAFB SLC-4E','value':'VAFB SLC-4E'}
                                 ],                               
                                  #  options=[{'label': i, 'value': i} for i in site_list],
                                    placeholder="Select a Launch Site here",
                                    value='ALL',
                                    searchable=True,
                                    style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}
                                    ),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                            min=0, max=10000, step=1000,
                                            marks={0: '0', 2500: '2500', 5000 :'5000', 7500:'7500'},
                                            value=[min_payload, max_payload]),
                                #html.Div(id='debugging2'),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Add callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig=px.pie(spacex_df,values='class',
        names='Launch Site',
        title='Total Success Launches by All Sites')
    else:
        data =  spacex_df[spacex_df['Launch Site']==entered_site]
        df = data.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(df,values='class count',names='class',title=f"Total Success Launches for {entered_site}")
    return fig

# Debugging 
# @app.callback(
#     dash.dependencies.Output('debugging2', 'children'),
#     [dash.dependencies.Input('payload-slider', 'value')])
# def update_output(value):
#     return 'You have selected "{}"'.format(value)
    
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(site,payload):
    low, high = (payload[0],payload[1])
    mask=spacex_df[spacex_df['Payload Mass (kg)'].between(low,high)]
    if site=='ALL':
        fig=px.scatter(mask,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Payload vs. Launch Outcome for all sites')
        return fig
    else:
        mask_filtered=mask[mask['Launch Site']==site]
        fig=px.scatter(mask_filtered,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Payload vs. Launch Outcome for ' + site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
