import pandas as pd
from fuzzywuzzy import fuzz
import unicodedata

def clean_name(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")
    return str(text).replace('.', '').replace('\'','')

def non_intersect(l1, l2):
    answer = []
    for i in l1:
        if i not in l2:
            answer.append(i)
    return answer

def mismatch(l1, l2):
    return non_intersect(l1, l2) + non_intersect(l2, l1)

def find_typos(l):
    typo_list = []
    i1, i2 = 0, 1
    while i2 < len(l):
        score = fuzz.ratio(l[i1], l[i2])
        if score >= 75:
            typo_list.append((score, l[i1], l[i2]))
        i1 += 1
        i2 += 1
    return typo_list

def fix_typos(df1, df2):
    df1_players = df1['Player'].tolist()
    df2_players = df2['Player'].tolist()
    typos = find_typos(sorted(mismatch(df1_players, df2_players)))
    for t in typos:
        cond1 = (df1['Player'] == t[1]) | (df1['Player'] == t[2])
        cond2 = (df2['Player'] == t[1]) | (df2['Player'] == t[2])
        df1.loc[cond1, 'Player'] = t[1] if t[1] in df1_players else t[2]
        df2.loc[cond2, 'Player'] = t[1] if t[1] in df1_players else t[2]

years = list(range(2010,2021))
    
for year in years:
    stats = pd.read_csv('player_stats/{}-{}.csv'.format(year-1,year))
    stats.drop(stats.columns[0], axis=1, inplace=True)
    salaries = pd.read_csv('player_salaries2/{}-{}.csv'.format(year-1, year))
    salaries.drop(salaries.columns[0], axis=1, inplace=True)
    # salaries.drop('Team', axis=1, inplace=True)
    info = pd.read_csv('player_info/{}-{}.csv'.format(year-1, year))

    stats['Player'] = stats['Player'].apply(lambda x: clean_name(x))
    salaries['Player'] = salaries['Player'].apply(lambda x: clean_name(x))
    info['Player'] = info['Player'].apply(lambda x: clean_name(x))

    fix_typos(stats, salaries)
    fix_typos(stats, info)
    fix_typos(salaries, info)

    l1 = sorted(non_intersect(stats['Player'].tolist(), salaries['Player'].tolist()))

    salaries = pd.read_csv('player_salaries/{}-{}.csv'.format(year-1, year))
    salaries.drop(salaries.columns[0], axis=1, inplace=True)
    
    l1 = sorted(non_intersect(l1, salaries['Player'].tolist()))
    print('{}-missing-salaries: {}'.format(year, len(l1)))
    print(l1)
