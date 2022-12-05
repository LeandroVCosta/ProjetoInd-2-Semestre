import dash
import dash_bootstrap_components as dbc
import dash_auth
import sqlalchemy

VALID_USERNAME_PASSWORD_PAIRS = {
}

server = 'trackvisiondb.database.windows.net'
database = 'trackvisiondb'
username = 'CloudSA49c766d4'
password = 'Urubu1004'
driver = 'ODBC+DRIVER+17+for+SQL+Server'
engine_stmt = ("mssql+pyodbc://%s:%s@%s/%s?driver=%s" % (username, password, server, database, driver ))
conn = sqlalchemy.create_engine(engine_stmt)
valido = conn.execute("select * from Usuario")
for row in valido:
    VALID_USERNAME_PASSWORD_PAIRS[row[3]] = row[4]

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"


app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
app._favicon = ("../assets/energy.png")
app.title = "TrackVision"
server = app.server

