import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# --- Data Simulation (Replace with your actual data fetching logic) ---
def fetch_camera_data():
    """
    This function would connect to your cloud database/API
    to fetch real-time data from your cameras.
    For demonstration, we'll simulate some data.
    """
    num_cameras = 5
    data = {
        'Camera ID': [f'Camera {i+1}' for i in range(num_cameras)],
        'Location': [f'Forest Zone {chr(65+i)}' for i in range(num_cameras)],
        'Temperature (°C)': [25 + i * 2 + (datetime.datetime.now().second % 10) for i in range(num_cameras)],
        'Humidity (%)': [60 - i * 3 + (datetime.datetime.now().second % 5) for i in range(num_cameras)],
        'Smoke Level': [i * 0.1 + (datetime.datetime.now().second % 2) * 0.05 for i in range(num_cameras)],
        'Fire Detected': [True if (datetime.datetime.now().second % 15 == i) else False for i in range(num_cameras)],
        'Timestamp': [datetime.datetime.now() for _ in range(num_cameras)]
    }
    df = pd.DataFrame(data)
    return df

# --- Dashboard Layout ---
app.layout = html.Div(style={'backgroundColor': '#1A1A1A', 'color': '#E0E0E0', 'fontFamily': 'Inter, sans-serif'}, children=[
    html.H1("Data X Wildfire Monitoring Dashboard", 
            style={'textAlign': 'center', 'color': '#FF7043', 'paddingTop': '20px'}),
    
    html.Div(className="container mx-auto p-6", children=[
        html.Div(className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6", children=[
            # Card 1: Total Cameras
            html.Div(className="bg-datax-gray p-6 rounded-lg shadow-md", children=[
                html.H3("Total Cameras", className="text-xl font-semibold mb-2"),
                html.P(id='total-cameras', className="text-4xl font-bold text-datax-blue")
            ]),
            # Card 2: Active Fires
            html.Div(className="bg-datax-gray p-6 rounded-lg shadow-md", children=[
                html.H3("Active Fires Detected", className="text-xl font-semibold mb-2"),
                html.P(id='active-fires', className="text-4xl font-bold text-datax-orange")
            ]),
            # Card 3: Last Updated
            html.Div(className="bg-datax-gray p-6 rounded-lg shadow-md", children=[
                html.H3("Last Updated", className="text-xl font-semibold mb-2"),
                html.P(id='last-updated', className="text-xl text-datax-light-text")
            ]),
        ]),

        html.Div(className="mt-8 bg-datax-gray p-6 rounded-lg shadow-md", children=[
            html.H2("Camera Data Overview", className="text-2xl font-bold text-datax-green mb-4"),
            dcc.Graph(id='camera-data-table'), # Will display a table or detailed view
        ]),

        html.Div(className="mt-8 bg-datax-gray p-6 rounded-lg shadow-md", children=[
            html.H2("Smoke Levels by Location", className="text-2xl font-bold text-datax-green mb-4"),
            dcc.Graph(id='smoke-level-chart'),
        ]),

        html.Div(className="mt-8 bg-datax-gray p-6 rounded-lg shadow-md", children=[
            html.H2("Temperature & Humidity Trends", className="text-2xl font-bold text-datax-green mb-4"),
            dcc.Graph(id='temp-humidity-chart'),
        ]),
    ]),
    
    # Interval component to refresh data
    dcc.Interval(
        id='interval-component',
        interval=5*1000, # in milliseconds (5 seconds)
        n_intervals=0
    )
])

# --- Callbacks to update dashboard components ---
@app.callback(
    [Output('total-cameras', 'children'),
     Output('active-fires', 'children'),
     Output('last-updated', 'children'),
     Output('camera-data-table', 'figure'),
     Output('smoke-level-chart', 'figure'),
     Output('temp-humidity-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    df = fetch_camera_data()

    # Summary Stats
    total_cameras = len(df)
    active_fires = df['Fire Detected'].sum()
    last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Camera Data Table (using a Scatter plot for simplicity, but you'd use a Dash DataTable)
    # For a real table, you'd use dash_table.DataTable
    # For now, let's just show a simple bar chart of smoke levels for each camera
    camera_table_fig = px.bar(df, x='Camera ID', y='Smoke Level', 
                              title='Current Smoke Levels per Camera',
                              color='Fire Detected',
                              color_discrete_map={True: '#FF7043', False: '#2196F3'},
                              template="plotly_dark")
    camera_table_fig.update_layout(
        plot_bgcolor='#333333', paper_bgcolor='#333333', font_color='#E0E0E0',
        xaxis_title="Camera ID", yaxis_title="Smoke Level (Arbitrary Units)"
    )


    # Smoke Level Chart
    smoke_fig = px.bar(df, x='Location', y='Smoke Level', 
                       title='Average Smoke Level by Location',
                       color='Fire Detected',
                       color_discrete_map={True: '#FF7043', False: '#2196F3'},
                       template="plotly_dark")
    smoke_fig.update_layout(
        plot_bgcolor='#333333', paper_bgcolor='#333333', font_color='#E0E0E0',
        xaxis_title="Location", yaxis_title="Smoke Level"
    )

    # Temperature & Humidity Chart
    temp_humidity_fig = px.scatter(df, x='Temperature (°C)', y='Humidity (%)', 
                                   size='Smoke Level', color='Fire Detected',
                                   color_discrete_map={True: '#FF7043', False: '#2196F3'},
                                   hover_name='Camera ID',
                                   title='Temperature vs. Humidity by Camera (Size indicates Smoke Level)',
                                   template="plotly_dark")
    temp_humidity_fig.update_layout(
        plot_bgcolor='#333333', paper_bgcolor='#333333', font_color='#E0E0E0',
        xaxis_title="Temperature (°C)", yaxis_title="Humidity (%)"
    )


    return total_cameras, active_fires, last_updated, camera_table_fig, smoke_fig, temp_humidity_fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8050) # Dash apps typically run on port 8050 by default