import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from navbar import Navbar
from importClean import load_data_frame
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from tommy import *

#  Bootstrap CSS, the Navbar requires it
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

#  Call the Navbar
nav = Navbar()
#  Specify csv file
df = load_data_frame("heart_failure_clinical_records_dataset.csv")
features = df.columns  # This is required for Graphs

app.layout = html.Div([
    nav,
    # Represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    html.Div([
        dcc.Dropdown(id='xaxis',
                     options=[{'label': i, 'value': i} for i in features],
                     value='age')
    ], style={"width": '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(id='yaxis',
                     options=[{'label': i, 'value': i} for i in features],
                     value="smoking")
    ], style={"width": '48%', 'display': 'inline-block'}),
    dcc.Graph(id="feature-graphic"),
    html.A(html.Button('Download Data', id='download-button'), id='download-link-filtered-data')
], style={'padding': 10})


@app.callback(Output('feature-graphic', 'figure'),
              # Output('download-link-filtered-data','href')],
              [Input('xaxis', 'value'),
               Input('yaxis', 'value')])
def update_graph(xaxis_name, yaxis_name):
    return {'data': [go.Scatter(x=df[xaxis_name],
                                y=df[yaxis_name],
                                text=df[xaxis_name],
                                mode='markers',
                                marker={'size': 15,
                                        'opacity': 0.5,
                                        'line': {'width': 0.5, 'color': 'white'}
                                        }
                                )],
            'layout': go.Layout(title="My Dashboard",
                                xaxis={'title': xaxis_name},
                                yaxis={'title': yaxis_name},
                                hovermode='closest'
                                )
            }


#  View all data from CSV
table_layout = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("records"),
    page_action="none",  # Allow all data in one page
    style_cell={'textAlign': 'center'},
    style_cell_conditional=[
        {
            "if": {"column_id": "Region"},
            "textAlign": "center"
        },
        {
            "if": {
                "state": "active"  # "active" selected data
            },
            "backgroundColor": "rgba(0,116,217, 0.3)"
        }
    ],
    css=[{'selector': '.row', 'rule': 'margin: 0'}],
)

#  Form for HF predictor
form_layout = dbc.FormGroup(
    [
        dbc.Jumbotron(
            html.H1("Heart Failure Predictor", className="display-3"),
        ),

        dbc.Label("Enter Your Age", html_for="age", width=3, className="pl-5"),
        dbc.Col(
            dbc.Input(
                type="number",
                id="age",
                placeholder="Enter Your Age",
            ),
            width=3, className="pl-5",
        ),

        dbc.Label("Are You an Anaemic Patient?", html_for="anemia", width=3, className="pl-5"),
        dbc.Col(
            dcc.Dropdown(
                id="anemia",
                options=[
                    {"label": "Yes", "value": "Yes"},
                    {"label": "No", "value": "No"}
                ], placeholder="Are You an Anaemic Patient?", searchable=False
            ),
            width=3, className="pl-5",
        ),

        dbc.Label("Are You a Diabetic Patient?", html_for="diabetes", width=3, className="pl-5"),
        dbc.Col(
            dcc.Dropdown(
                id="diabetes",
                options=[
                    {"label": "Yes", "value": "Yes"},
                    {"label": "No", "value": "No"}
                ], placeholder="Are You a Diabetic Patient?", searchable=False
            ),
            width=3, className="pl-5",
        ),

        dbc.Label("Do You have High Blood Pressure? (BP130/80 and above)", html_for="highblood", width=3,
                  className="pl-5"),
        dbc.Col(
            dcc.Dropdown(
                id="highblood",
                options=[
                    {"label": "High Blood Pressure Patient", "value": "Yes"},
                    {"label": "No", "value": "No"}
                ], placeholder="Are You a High Blood Pressure Patient?", searchable=False
            ),
            width=3, className="pl-5",
        ),

        dbc.Label("Are You a Smoker?", html_for="smoker", width=3, className="pl-5"),
        dbc.Col(
            dcc.Dropdown(
                id="smoker",
                options=[
                    {"label": "Smoker", "value": "Yes"},
                    {"label": "Non-smoker", "value": "No"}
                ], placeholder="Do You Smoke?", searchable=False
            ),
            width=3, className="pl-5",
        ),

        dbc.Label("Enter Your Gender", html_for="gender", width=3, className="pl-5"),
        dbc.Col(
            dcc.Dropdown(
                id="gender",
                options=[
                    {"label": "Male", "value": "Male"},
                    {"label": "Female", "value": "Female"}
                ], placeholder="What is Your Gender?", searchable=False
            ),
            width=3, className="pb-3 pl-5",
        ),

        dbc.Col(
            dbc.Button('Submit', id='submit-val', n_clicks=0, color="primary"),
            className="pl-5",
        ),
        html.Hr(className="my-4"),
        html.Div(id="testers", className="pl-5")
    ],
)


@app.callback(
    Output('testers', 'children'),
    [Input('submit-val', 'n_clicks')],
    [State('age', 'value'), State('anemia', 'value'),
     State('diabetes', 'value'), State('highblood', 'value'),
     State('smoker', 'value'), State('gender', 'value')],
    prevent_initial_call=True
)
def update_output(n_clicks, input1, input2, input3, input4, input5, input6):
    print(df)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/viewDataset':
        return table_layout
    elif pathname == '/predictor':
        return form_layout
    else:
        return index_page


if __name__ == '__main__':
    app.title = "View Dataset"
    app.run_server(debug=False)
