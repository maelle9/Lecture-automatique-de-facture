import base64
import os
from flask import Flask, send_from_directory
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import main_traitement
import atexit
import tempfile

#Dossier ou les photos upload vont être téléchargé
with tempfile.TemporaryDirectory() as tmpdirname:
    print('dossier temporaire:', tmpdirname)

    server = Flask(__name__)
    app = Dash(server=server, external_stylesheets=[dbc.themes.SUPERHERO], suppress_callback_exceptions=True)

    def download(path):
        """Serve a file from the upload directory."""
        return send_from_directory(tmpdirname, path, as_attachment=True)

    sidebar = html.Div([
        html.H5("Historique", className="display-6"),
        html.Hr(),
        html.H6("Historique des dernières images visualisées"),
        html.Ul(id="file-list"),
        dbc.Nav(vertical=True)],
        style={
            "position": "fixed",
            "top": "8%",
            "left": "0px",
            "bottom": "0px",
            "width": "15rem",
            "padding": "2rem 1rem",
            "color": "white",
            "background-color": "#233A4F"
        }
    )

    navbar = dbc.NavbarSimple(children=[
            dbc.DropdownMenu(direction="start",
                children=[
                    dbc.DropdownMenuItem("Trouver mon total", href="/"),
                    dbc.DropdownMenuItem("Informations", href="/Infos"),
                    dbc.DropdownMenuItem("Github", href="https://github.com/maaelle/Lecture-automatique-de-facture"),

                ],
                nav=True,
                in_navbar=True,
                label="Plus",
            ),
        ],
        brand="Github",
        brand_href="https://github.com/maaelle/Lecture-automatique-de-facture",
        color="dark",
        dark=True,
        fluid=True
    )

    contentIm = html.Div([
                    html.Div(
                        children=[dcc.Upload(
                            id='importer',
                            children=html.Div(
                                ['Deposer votre image dans cette partie',
                                html.Div(id='output-image-upload', style={'position': 'absolute'}),
                                html.A(id='Ima')
                                 ],
                                style={
                                    "width": "150%",
                                    'color': 'black',
                                    'height': '23rem',
                                    'lineHeight': '200%',
                                    'textAlign': 'center',
                                    "background-color": "#AAB6C1",
                                },
                            ),
                            multiple=True
                        )],
                        style={
                            'display': 'inline-block',
                            'margin-top': '11%',
                            'margin-left': '15%',
                            'vertical-align': 'top',
                        }
                    ),

                    html.Div(children=[
                        html.Div(children=[
                            html.A("Le total de cette facture est:")],
                            style={
                                'width': '150%',
                                'height': '3rem',
                                'lineHeight': '200%',
                                'textAlign': 'center',
                                "background-color": "#4A84BC"
                            }
                        ),

                        html.Div(children=[
                            html.A("")],
                            style={
                                'width': '65%',
                                'height': '8rem',
                                'lineHeight': '200%',
                                'textAlign': 'center',
                                'color': 'black',
                                'margin-top': '20%',
                                'margin-left': '45%',
                                'border-radius': '100px',
                                "background-color": "#E8A7B6"

                            }
                        )
                    ],
                            style={
                            'display': 'inline-block',
                            'margin-left': '25%',
                            'margin-top': '17%'
                            }
                    ),
                    sidebar,

    ], style={
            'margin-left': '15rem',
            'padding': '0rem 0rem'})

    contentInfos = html.Div([
        html.H5("Plus d'informations sur nous", className="display-4"),
        html.Hr(),
        html.P("Nous sommes 3 élèves de l'Esme Sudria de la majeure Intelligence Artificielle, nous avons réalisé ce projet dans le cadre de notre 2ème année."),
        html.P("BAYON DE NOYER Camille"),
        html.P("MARCELIN Maëlle"),
        html.P("MOGHRAOUI Sonia"),
        html.Br(),
        html.Br(),
        html.H5("Plus d'informations sur notre projet", className="display-4"),
        html.Hr(),
        html.P("On se place dans la perspective d’une boîte de conseil qui essaye de diversifier son offre d’extraction de texte à partir d’images. "
               "En particulier, le client cherche un système capable d’extraire les frais totaux à partir de factures. "),
        html.P("Le client ne veut pas nous donner de données de facture pour des raisons réglementaires. "
               "En conséquence, nous allons devoir construire un système d’extraction de texte à partir d’images à partir de photos de reçus de paiement."),
        html.P("Notre objectif est donc de pouvoir extraire le total de factures à partir de photos de reçus de paiement."),
        html.Br(),
        html.Br(),
        html.H5("Nous contacter", className="display-4"),
        html.Hr(),
        html.P("AutomatisationFacture.esme@outlook.fr")
    ], style={'textAlign': 'center', "padding": "2rem 10rem"})


    def save_file(name, content):
        """Decode and store a file uploaded with Plotly Dash."""
        data = content.encode("utf8").split(b";base64,")[1]
        with open(os.path.join(tmpdirname, name), "wb") as fp:
            fp.write(base64.decodebytes(data))


    def uploaded_files():
        """List the files in the upload directory."""
        files = []
        for filename in os.listdir(tmpdirname):
            path = os.path.join(tmpdirname, filename)
            if os.path.isfile(path):
                files.append(filename)
        return files


    def files_names(filename):
        """Create a Plotly Dash 'A' element that downloads a file from the app."""
        return html.A(filename)

    def DisplayImage(contents, filename):
        return html.Div([
            html.Div([
            html.Div([
                html.H4(main_traitement.main(tmpdirname + "/" + filename, False)),
            ], style={'margin-left': '265%', 'margin-top': '65%', 'position': 'absolute'}),
            html.Img(src=contents, style={'height': '90%', 'width': '90%', 'margin-left': '30%'})])
        ])

    @app.callback(Output("file-list", "children"),
                Input("importer", "contents"),
                State("importer", "filename"))

    def SavefilesandRegenerateList(list_of_contents, list_of_names):
        """Save uploaded files and regenerate the file list."""

        if list_of_names is not None and list_of_contents is not None:
            for data, name in zip(list_of_contents, list_of_names):
                save_file(name, data)

        files = uploaded_files()

        if len(files) == 0:
            return [html.Li("Pas d'image dans l'historique")]
        else:
            return [html.Li(files_names(filename)) for filename in files]

    @app.callback(Output("output-image-upload", "children"),
                Input("importer", "contents"),
                State("importer", "filename"))

    def AfficherIm(list_of_contents, list_of_names):
        if list_of_contents is not None:
            Ima = [
                DisplayImage(c, n)
                for c, n in
                    zip(list_of_contents, list_of_names)]
            return Ima

    app.layout = html.Div([
                    dcc.Location(id="url"),
                    navbar,
                    html.Div(id="page-content"),

                ])

    @app.callback(
        [Output("page-content", "children")],
        [Input("url", "pathname")],  # On va prendre le pathname du url dans app.layout
    )
    def Content(pathname):
        if pathname == "/":
            return [contentIm]
        elif pathname == "/Infos":
            return [contentInfos]
        else:
            return [html.H1("Malheureusement cette page n'est pas disponible", style={"margin-left": "5rem"})]


    if __name__ == "__main__":
        app.run_server(debug=True)

    def CloseRepertory():
        if os.path.exists(tmpdirname):
            os.removedirs(tmpdirname)
        print("Au revoir")

    atexit.register(CloseRepertory)