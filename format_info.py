import pandas as pd

df = pd.read_csv("1996-2019_player_info.csv", index_col=0)
df['season'] = df['season'].apply(lambda x: int(x[:4]) + 1)
df.rename(columns={"Country":"USA", "season":"Season"}, inplace=True)
df.drop(columns=["Team", "Age", "gp", "pts", "reb", "ast", "net_rating", "oreb_pct", "dreb_pct", "usg_pct", "ts_pct", "ast_pct"], inplace=True)
df = df[df.Season >= 2005]
df.sort_values(["Season","Player"], ascending=[True, True], inplace=True)

df['USA'] = df['USA'].apply(lambda x: 1 if x == "USA" else 0)
df['College'] = df['College'].apply(lambda x: 1 if x != "None" else 0)

for i, r in df.iterrows():
    if(r.loc['YearsPro'] == "Undrafted"):
        FindCond = (df['Player'] == r.loc['Player']) & (df['Season'] == (r.loc['Season'] - 1))
        tdf = df.loc[FindCond]
        if tdf.empty:
            df.at[i,'YearsPro'] = 1
        else:
             df.at[i, 'YearsPro'] = int(tdf.iloc[0].loc['YearsPro']) + 1
    else:
        df.at[i,'YearsPro'] = r['Season'] - int(r['YearsPro'])

for i in range(2010, 2021):
    tdf = df.loc[df['Season'] == i]
    tdf.reset_index(inplace=True, drop=True)
    tdf.to_csv('player_info/{}-{}.csv'.format(i-1,i))
