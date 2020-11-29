import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

import mysql.connector
from collections import Counter

miConexion = mysql.connector.connect( host='db', user= 'root', passwd='example', db='datos' )
cur = miConexion.cursor()
cur.execute( "SELECT type, rating, duration FROM NETFLIX" )
datos = cur.fetchall()
miConexion.close()

tipo, rating, duracion = zip(*datos)
label_tipo, value_tipo = zip(*Counter(tipo).most_common())
label_rating, value_rating = zip(*Counter(rating).most_common())
duracionMovies = [duracion[i] for i in range(len(datos)) if tipo[i]=="Movie"]
duracionMovies = [int(dur[0:-4]) for dur in duracionMovies]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
  html.H1(children='Estadísticas de Netflix'),
  html.H3(children='Películas v. Series'),
  dcc.Graph(
    figure=go.Figure(go.Pie(labels=label_tipo, values=value_tipo))
  ),
  html.H3(children='Clasificaciones de Edad'),
  dcc.Graph(
    figure=go.Figure(go.Pie(labels=label_rating, values=value_rating))
  ),
  html.H3(children='Duración de las películas, en minutos'),
  dcc.Graph(
    figure=go.Figure(data=[go.Histogram(x=duracionMovies)])
  )
])

if __name__ == '__main__':
  app.run_server(host='0.0.0.0', port=8080, debug=True)