import pandas as pd
from sklearn.model_selection import train_test_split


years = list(range(2010, 2021))
final_df = pd.DataFrame()
for year in years:
    stats = pd.read_csv('player_stats/{}-{}.csv'.format(year-1, year))
    stats.drop(stats.columns[0], axis=1, inplace=True)
    salaries = pd.read_csv('player_salaries/{}-{}.csv'.format(year-1, year))
    salaries.drop(salaries.columns[0], axis=1, inplace=True)
    info = pd.read_csv('player_info/{}-{}.csv'.format(year-1, year))
    info.drop(info.columns[0], axis=1, inplace=True)
    df = pd.merge(stats, info, on='Player')
    df = pd.merge(df, salaries, on='Player')
    final_df = final_df.append(df, ignore_index=True)

final_df.drop(columns=['Pos','Tm','College','USA','DraftRound','DraftNum', 'Salary', 'Salary(*)'],inplace=True)
train_test_X = final_df[final_df.Season != 2020].drop(columns=['Player','Salary(%)'])

train_test_y = final_df[final_df.Season != 2020].drop(columns=final_df.columns[:len(final_df.columns)-1])
names_final = final_df[final_df.Season == 2020].drop(columns=final_df.columns[1:len(final_df.columns)])
X_final = final_df[final_df.Season == 2020].drop(columns=['Player','Salary(%)'])
y_final = final_df[final_df.Season == 2020].drop(columns=(final_df.columns[:len(final_df.columns)-1]))

X_train, X_test, y_train, y_test = train_test_split(train_test_X, train_test_y, test_size=0.25, random_state=42)

X_train.to_csv('data/train/X.csv', index=False)
y_train.to_csv('data/train/y.csv', index=False)
X_test.to_csv('data/test/X.csv', index=False)
y_test.to_csv('data/test/y.csv', index=False)

names_final.to_csv('data/final/names.csv', index=False)
X_final.to_csv('data/final/X.csv', index=False)
y_final.to_csv('data/final/y.csv', index=False)


