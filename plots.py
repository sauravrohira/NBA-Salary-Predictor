import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

years = list(range(2010,2021))
final_df = pd.DataFrame()
for year in years:
    stats = pd.read_csv('player_stats/{}-{}.csv'.format(year-1,year))
    stats.drop(stats.columns[0], axis=1, inplace=True)
    salaries = pd.read_csv('player_salaries/{}-{}.csv'.format(year-1, year))
    salaries.drop(salaries.columns[0], axis=1, inplace=True)
    info = pd.read_csv('player_info/{}-{}.csv'.format(year-1, year))
    df = pd.merge(stats, salaries, on='Player')
    df = pd.merge(df, info, on='Player')
    final_df = final_df.append(df, ignore_index=True)

final_df.reset_index(inplace=True)
print(final_df)

fig = go.Figure(data=go.Scatter(x=final_df['PTS'],
                                y=final_df['Salary(%)'],
                                mode='markers',
                                marker_color=final_df['Age'],
                                hovertext=(final_df['Player'])))  # hover text goes here

fig.update_layout(title='PTS vs Salary(%)')
fig.show()

# fig = px.histogram(final_df, x='Salary(%)')
# fig.show()
