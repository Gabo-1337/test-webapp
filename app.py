from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import validator

# -------------------------------------------------------------------------------------------------------
# * Initializations

# * dataset initalization
data = pd.read_csv("https://raw.githubusercontent.com/Lolimipsu/thesis-repository/main/HR_comma_sep.csv")

# * variable initializations
left_company = data[data["left"] == 1]
stay_company = data[data["left"] == 0]

salary_left_total = left_company.groupby("salary")["left"].count()
salary_stay_total = stay_company.groupby("salary")["left"].count()

department_left_total = left_company.groupby("Department")["left"].count()
department_stay_total = stay_company.groupby("Department")["left"].count()

# * css / ui design
external_stylesheets = [
    {
        "href": ("https://fonts.googleapis.com/css2?" "family=Lato:wght@400;700&display=swap"),
        "rel": "stylesheet",
    },
]

# -------------------------------------------------------------------------------------------------------
# * Salary and Department bar charts

bar_chart_container = dbc.Container(
    [
        html.Hr(),
        html.H3("Salary and Department Bar Charts"),
        html.Div(
            children=[
                dcc.Graph(
                    figure={
                        "data": [
                            {
                                "x": salary_stay_total.index,
                                "y": salary_stay_total.values,
                                "type": "bar",
                                "name": "Retained",
                            },
                            {
                                "x": salary_left_total.index,
                                "y": salary_left_total.values,
                                "type": "bar",
                                "name": "Left",
                            },
                        ],
                        "layout": {
                            "title": "Salary",
                            "width": 600,
                            "height": 449,
                        },
                    },
                    style={"border": "1px solid black", "margin": "10px"},
                ),
                dcc.Graph(
                    figure={
                        "data": [
                            {
                                "x": department_stay_total.index,
                                "y": department_stay_total.values,
                                "type": "bar",
                                "name": "Retained",
                            },
                            {
                                "x": department_left_total.index,
                                "y": department_left_total.values,
                                "type": "bar",
                                "name": "Left",
                            },
                        ],
                        "layout": {
                            "title": "Department",
                            "width": 600,
                            "height": 449,
                        },
                    },
                    style={"border": "1px solid black", "margin": "10px"},
                ),
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
    ]
)

# -------------------------------------------------------------------------------------------------------
# * Correlation heatmap

inputs = data[["satisfaction_level", "number_project", "average_montly_hours", "time_spend_company", "Department", "salary"]]
target = data.left

inputs.replace({"salary": {"low": 1, "medium": 2, "high": 3}}, inplace=True)

dep_dummies = pd.get_dummies(data["Department"])
df_with_dummies = pd.concat([inputs, dep_dummies], axis="columns")
df_with_dummies.drop("Department", axis="columns", inplace=True)

x = df_with_dummies
y = target

corr_df = pd.concat([x, y], axis="columns").corr()

# Create a mask that covers the upper half of the heatmap
mask = np.triu(np.ones_like(corr_df, dtype=bool))

# Create a new correlation matrix with the upper half set to np.nan
corr_df_masked = corr_df.where(~mask, np.nan)

# where it starts
corr_heatmap_fig = px.imshow(
    corr_df_masked,
    labels=dict(x="Variable", y="Variable", color="Correlation"),
    x=corr_df.columns,
    y=corr_df.columns,
    color_continuous_scale="RdBu",
)

corr_heatmap_fig.update_layout(height=900)

corr_heatmap_container = dbc.Container(
    [html.Hr(), html.H3("Correlation Heatmap"), dcc.Graph(figure=corr_heatmap_fig)]
)

# -------------------------------------------------------------------------------------------------------
# * KDE Plot

kde_df = data[
    [
        "satisfaction_level",
        "last_evaluation",
        "number_project",
        "average_montly_hours",
        "time_spend_company",
    ]
]

# Create the distplots
kde_plot_figures = []
for col in kde_df.columns:
    kde_fig = ff.create_distplot([kde_df[col]], [col])
    kde_fig.update_layout(width=600, height=449, title=f"{col} Distribution")
    kde_plot_figures.append(
        dcc.Graph(figure=kde_fig, style={"border": "1px solid black", "margin": "10px"})
    )

# this is the one we'll use to print out the charts
kde_plot_container = dbc.Container(
    [
        html.Hr(),
        html.H3("Univariate Analysis - Numerical Variables - KDE Plot"),
        html.Div(
            children=[
                kde_plot_figures[0],
                kde_plot_figures[1]
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
        html.Div(
            children=[
                kde_plot_figures[2],
                kde_plot_figures[3]
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
        html.Div(
            children=[
                kde_plot_figures[4],
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
    ]
)

# -------------------------------------------------------------------------------------------------------
# * Box Plot

# list of the columns to plot
box_plot_x_values = [
    "satisfaction_level",
    "last_evaluation",
    "number_project",
    "average_montly_hours",
    "time_spend_company",
]

# Create DataFrames for employees who left and Retained in the company
box_plot_left_df = data[data["left"] == 1]
box_plot_stay_df = data[data["left"] == 0]

# Create a list to store the box plot figures
box_plot_figures = []

# Create a box plot for each column in the box_plot_x_values list
for col in box_plot_x_values:
    # Create a box plot figure for the current column
    box_fig = dcc.Graph(
        figure={
            "data": [
                {"x": box_plot_stay_df[col], "type": "box", "name": "Retained"},
                {"x": box_plot_left_df[col], "type": "box", "name": "Left"},
            ],
            "layout": {
                "title": col,
                "width": 600,
                "height": 449,
            },
        },
        style={"border": "1px solid black", "margin": "10px"},
    )

    # Add the box plot figure to the list of figures
    box_plot_figures.append(box_fig)

# this is the one we'll use to print out the charts
box_plot_container = dbc.Container(
    [
        html.Hr(),
        html.H3("Bivariate Analysis - Numerical Variables - Box Plot"),
        html.Div(
            children=[
                box_plot_figures[0],
                box_plot_figures[1],
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
        html.Div(
            children=[
                box_plot_figures[2],
                box_plot_figures[3],
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
        html.Div(
            children=[
                box_plot_figures[4],
            ],
            style={
                "display": "flex",
                "flex-direction": "row",
            },
        ),
    ]
)

# -------------------------------------------------------------------------------------------------------
# * Custom Prediction Forms
# * cpf means Custom Prediction forms

satisfaction_level_cpf_input = dbc.Row(
    [
        dbc.Label("Satisfaction Level", html_for="satisfaction_level_cpf", width=2),
        dbc.Col(
            dbc.Input(
                type="number",
                id="satisfaction_level_cpf",
                placeholder="Please toggle or input a floating point number between 0.01 and 1.00",
                debounce=True,
                min=0.01,
                max=1.00,
                step=0.01,
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

satisfaction_level_cpf_input.validate = validator.validate_float
satisfaction_level_cpf_input.invalid_feedback = "Please toggle a float number between 0.01 and 0.99."

# -------------------------------------------------------------------------------------------------------
# * number_project_cpf_input

number_project_cpf_input = dbc.Row(
    [
        dbc.Label("Number of Projects", html_for="number_project_cpf", width=2),
        dbc.Col(
            dbc.Input(
                type="number",
                id="number_project_cpf",
                placeholder="Please toggle an integer between 1 and 10",
                debounce=True,
                min=1,
                max=10,
                step=1,
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

number_project_cpf_input.validate = validator.validate_integer
number_project_cpf_input.invalid_feedback = "Please toggle or input an integer between 1 and 10."

# -------------------------------------------------------------------------------------------------------
# * average_monthly_hours_cpf_input

average_monthly_hours_cpf_input = dbc.Row(
    [
        dbc.Label("Average Monthly Hours", html_for="average_monthly_hours_cpf", width=2),
        dbc.Col(
            dbc.Input(
                type="number",
                id="average_monthly_hours_cpf",
                placeholder="Please toggle an integer number between 1 and 310",
                debounce=True,
                min=1,
                max=310,
                step=1,
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

average_monthly_hours_cpf_input.validate = validator.validate_float_range
average_monthly_hours_cpf_input.invalid_feedback = "Please toggle an integer number between 1 and 310."

# -------------------------------------------------------------------------------------------------------
# * time_spend_company_cpf_input

time_spend_company_cpf_input = dbc.Row(
    [
        dbc.Label("Time Spent in Company", html_for="time_spend_company_cpf", width=2),
        dbc.Col(
            dbc.Input(
                type="number",
                id="time_spend_company_cpf",
                placeholder="Please toggle or input an integer number between 1 and 10",
                debounce=True,
                min=1,
                max=10,
                step=1,
            ),
            width=10,
        ),
    ],
    className="mb-3",
)

time_spend_company_cpf_input.validate = validator.validate_integer_range
time_spend_company_cpf_input.invalid_feedback = "Please toggle or input an integer number between 1 and 10."


# -------------------------------------------------------------------------------------------------------
# * salary_cpf_input

salary_cpf_input = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Salary", html_for="salary_cpf", width=2),
                dbc.Col(
                    dbc.Select(
                        id="salary_cpf",
                        options=[
                            {"label": "Low", "value": "1"},
                            {"label": "Medium", "value": "2"},
                            {"label": "High", "value": "3"},
                        ],
                    ),
                    width=10,
                ),
            ],
            className="mb-3",
        )
    ]
)

# -------------------------------------------------------------------------------------------------------
# * department_cpf_input

department_cpf_input = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Label("Department", html_for="department_cpf", width=2),
                dbc.Col(
                    dbc.Select(
                        id="department_cpf",
                        options=[
                            {"label": "IT", "value": "IT"},
                            {"label": "Random Department", "value": "RandD"},
                            {"label": "Accounting", "value": "accounting"},
                            {"label": "HR", "value": "hr"},
                            {"label": "Management", "value": "management"},
                            {"label": "Marketing", "value": "marketing"},
                            {"label": "Product Management", "value": "product_mng"},
                            {"label": "Sales", "value": "sales"},
                            {"label": "Support", "value": "support"},
                            {"label": "Technical", "value": "technical"},
                        ],
                    ),
                    width=10,
                ),
            ],
            className="mb-3",
        )
    ]
)

# -------------------------------------------------------------------------------------------------------
# * prints out the prediction
cpf_output = dbc.Row(
    [
        dbc.Label("Output", html_for="cpf_output", width=2),
        dbc.Col(
            dbc.Input(
                id="cpf_output",
                disabled=True
            ),
            width=10,
        ),
    ],
    className="mb-3",
)


custom_prediction_form = dbc.Form(
    [
        satisfaction_level_cpf_input,
        number_project_cpf_input,
        average_monthly_hours_cpf_input,
        time_spend_company_cpf_input,
        salary_cpf_input,
        department_cpf_input,
        cpf_output,
        html.Div(dbc.Button("Submit", id="submit-button-id", color="primary"), style={"textAlign": "center"}, n_clicks=0)
    ]
)

# -------------------------------------------------------------------------------------------------------
# * program starts here

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server
app.title = "Employee Retention Prediction Model"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="📊", className="header-emoji"),
                html.H1(
                    children="Employee Retention Prediction Model",
                    className="header-title",
                ),
                html.P(
                    children=("A Machine learning approach using random forest classifier"),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        # * Salary and Department bar charts
        dbc.Container([
            bar_chart_container
            ],
        ),
        # * Correlation heatmap
        dbc.Container([
            corr_heatmap_container
            ],
        ),
        # * KDE Plot
        dbc.Container([
            kde_plot_container
            ],
        ),
        # * Box Plot
        dbc.Container([
            box_plot_container
            ],
        ),
        # * Custom Prediction Form
        dbc.Container([
            html.Hr(),
            html.H3("Custom Prediction Input Form"),
            custom_prediction_form
            ],
        ),
    ]
)
# Define a callback function that updates the value of the disabled input field when the Submit button is clicked
@app.callback(
    Output("cpf_output", "value"),
    Input("submit-button-id", "n_clicks"),
    [State('satisfaction_level_cpf', 'value')], 
    [State('number_project_cpf', 'value')], 
    [State('average_monthly_hours_cpf', 'value')], 
    [State('time_spend_company_cpf', 'value')], 
    [State('salary_cpf', 'value')], 
    [State('department_cpf', 'value')])
def update_output(n_clicks, s_l, n_p, amh, tsc, sal, dep):
    if n_clicks:
        import bpred
        pred_output = bpred.make_prediction(s_l, n_p, amh, tsc, sal, dep)
        return (pred_output)

if __name__ == "__main__":
    app.run_server(debug=True)
