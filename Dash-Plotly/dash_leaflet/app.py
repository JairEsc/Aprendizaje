import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output
import awsS3Connection
import awsS3CityflowTrips
# Get the list of route files from S3
lista_de_opciones = awsS3CityflowTrips.getListRoutesFiles()

# Initialize the app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout for the app
app.layout = html.Div([
    html.H1("Dashboard de visualización de datos"),
    html.H2("Seleccione el archivo que desea visualizar"),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in lista_de_opciones],
        value='None'  # Default value
    ),
    html.Div(id='display-value')  # Area where the table will be displayed
])

# Callback to update the display-value based on the selected dropdown value
@app.callback(
    Output('display-value', 'children'),
    [Input('dropdown', 'value')]
)
def update_output(value):
    # If no file is selected, return a message
    if value == 'None':
        return "Por favor, seleccione un archivo."
    
    # Get the dataframe based on the selected file
    dataframe = awsS3Connection.get_data_given_index(value)
    
    # Check if dataframe is returned
    if dataframe is not None:
        # Create a DataTable from the dataframe
        return dash_table.DataTable(
            data=dataframe.to_dict('records'),  # Convert dataframe to a list of dicts
            columns=[{'name': col, 'id': col} for col in dataframe.columns]  # Define columns for the table
        )
    else:
        return "No se pudo cargar el archivo seleccionado."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# %%
