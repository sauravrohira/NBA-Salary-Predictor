import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

stats = pd.read_csv('player_stats/2019-2020.csv')
stats.drop(stats.columns[0], axis=1, inplace=True)
salaries = pd.read_csv('player_salaries/2019-2020.csv')
salaries.drop(salaries.columns[0], axis=1, inplace=True)
salaries.drop('Team', axis=1, inplace=True)
df = pd.merge(stats, salaries, on='Player')

fig = go.Figure(data=go.Scatter(x=df['PTS'],
                                y=df['Salary'],
                                mode='markers',
                                marker_color=df['Salary'],
                                text=df['Player']))  # hover text goes here

fig.update_layout(title='Points vs Salary')
fig.show()
