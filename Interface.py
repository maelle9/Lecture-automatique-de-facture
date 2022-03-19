from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import part3

# Load data
app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])  # initialisation du dash app

#On ajoute un layout sur la page

app.layout = html.Div([
                html.Div(
                    children=[dcc.Upload(
                        id='importer',
                        children=html.Div(
                            ['Upload here your ',
                            html.A('picture'),
                            html.Div(id='output-image-upload'),
                            html.A(id='children')
                             ],
                            style = {
                                'width' : '400px',
                                'color': 'black',
                                'height': '370px',
                                'lineHeight': '70px',
                                'textAlign': 'center',
                                'margin': '260px',
                                'margin-top': '75px',
                                "background-color": "#C8C8C8"
                            },
                        ),
                        multiple=True
                    ),

                    ],

                    style = {
                        'display': 'inline-block',
                        'vertical-align': 'top'
                    }
                ),

                html.Div(children = [
                    html.Div(children=[
                        html.A("Le total de cette facture est:")],
                        style={
                            'width': '400px',
                            'height': '50px',
                            'lineHeight': '45px',
                            'textAlign': 'center',

                            "background-color": "#9B0024"
                        }
                    ),

                    html.Div(children=[
                        #html.A(part3.affiche_total('output-image-upload')),
                        html.A("€")],
                        style={
                            'width': '150px',
                            'height': '150px',
                            'lineHeight': '140px',
                            'textAlign': 'center',
                            'color': 'black',
                            'border-radius': '100px',
                            'margin': '130px',
                            'margin-top': '100px',
                            "background-color": "#E8A7B6"
                        }
                    )
                ],
                        style = {
                        'display': 'inline-block',
                        'margin-left': '-165px',
                        'margin-top': '100px'
                        }
                ),

                html.Div(children=[
                    html.A("<...........................................................................................................................................................>")],
                    style={
                        'width': '990px',
                        'height': '80px',
                        'lineHeight': '65px',
                        'font-size': '26px',
                        'textAlign': 'center',
                        'margin': '-170px',
                        'margin-left': '210px',
                        "background-color": "#9B0024"
                    }
                )
])

def Image(contents, filename):
    return html.Div([
        html.Img(src=contents, style={'height':'50%', 'width':'40%'}),
    ])

@app.callback(Output('output-image-upload', 'children'),
              Input('importer', 'contents'),
              State('importer', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            Image(c)
            for c, n in
                zip(list_of_contents, list_of_names)]
        return children

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)