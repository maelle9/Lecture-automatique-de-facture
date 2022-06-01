import base64
import os
from flask import Flask, send_from_directory
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import main
import atexit

#Dossier ou les photos upload vont être téléchargé
UPLOAD_DIRECTORY = "C:/Temp"

#Si pas déjà existant, on le crée
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = Dash(server=server, external_stylesheets=[dbc.themes.SUPERHERO])

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


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
                        html.A("")],
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
                    html.A("<..............................................................................................................................................>")],
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
                ),
                html.H2("File List"),
                html.Ul(id="file-list")
])


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    return html.A(filename)

def Image(contents, filename):
    return html.Div([
        html.Div([
        html.Img(src=contents, style={'height': '50%', 'width': '40%'})]),
        html.Div([
            html.H6(main.main("C:/Temp/" + filename, False)),
        ], style={
            'margin-top': '-40px',
            'margin-left': '680px'})
    ])

@app.callback(Output("file-list", "children"),
            Input("importer", "contents"),
            State("importer", "filename"))

def update_output(list_of_contents, list_of_names):
    """Save uploaded files and regenerate the file list."""

    if list_of_names is not None and list_of_contents is not None:
        for data, name in zip(list_of_contents, list_of_names):
            save_file(name, data)

    files = uploaded_files()

    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]

@app.callback(Output("output-image-upload", "children"),
            Input("importer", "contents"),
            State("importer", "filename"))

def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            Image(c, n)
            for c, n in
                zip(list_of_contents, list_of_names)]
        return children


if __name__ == "__main__":
    app.run_server(debug=True)

def CloseRepertory():
    if os.path.exists(UPLOAD_DIRECTORY):
        os.rmdir(UPLOAD_DIRECTORY)
    print("Au revoir")

atexit.register(CloseRepertory)
app.run()