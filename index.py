import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from navbar import Navbar
from importClean import load_data_frame
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

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
    ]
)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/viewDataset':
        return table_layout
    elif pathname == '/viewGraph':
        return '404'
    else:
        return index_page


if __name__ == '__main__':
    app.title = "View Dataset"
    app.run_server(debug=False)
