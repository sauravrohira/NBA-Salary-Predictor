from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# NBA season we will be analyzing
years = list(range(2010, 2021))
# URL page we will scraping (see image above)
urlformats = ["per_game", "advanced", "play-by-play"]

for year in years:
    stats_reg, stats_adv, stats_pbp = None, None, None
    for u in urlformats:
        # this is the HTML from the given URL
        url = "https://www.basketball-reference.com/leagues/NBA_{}_{}.html".format(year, u)
        html = urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")

        # use findALL() to get the column headers
        soup.findAll('tr', limit=2)
        # use getText()to extract the text we need into a list
        if u == "play-by-play":
            headers = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th', )]
        else:
            headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th', )]
        # exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
        headers = headers[1:]
        # avoid the first header row
        rows = soup.findAll('tr', {"class" : "full_table"})[0:]
        player_stats = [[td.getText() for td in rows[i].find_all('td', class_=lambda x: x != 'right iz')] for i in range(len(rows))]

        if(u == "per_game"):
            stats_reg = pd.DataFrame(player_stats, columns=headers)
        elif u == "advanced":
            stats_adv = pd.DataFrame(player_stats, columns=headers)
        else:
            stats_pbp = pd.DataFrame([row[:11] for row in player_stats], columns=headers[:11])

    def drop_y(df):
        # list comprehension of the cols that end with '_y'
        to_drop = [x for x in df if x.endswith('_y')]
        df.drop(to_drop, axis=1, inplace=True)

    stats = pd.merge(stats_pbp, stats_reg, on='Player', suffixes=['', '_y'])
    drop_y(stats)
    stats = pd.merge(stats, stats_adv, on='Player', suffixes=['', '_y'])
    drop_y(stats)
    stats.drop([stats.columns[41],stats.columns[46]], axis=1, inplace=True)
    stats['PG%'] = stats['PG%'].apply(lambda x: x[:-1])
    stats['SG%'] = stats['SG%'].apply(lambda x: x[:-1])
    stats['SF%'] = stats['SF%'].apply(lambda x: x[:-1])
    stats['PF%'] = stats['PF%'].apply(lambda x: x[:-1])
    stats['C%'] = stats['C%'].apply(lambda x: x[:-1])
    stats.replace('', 0.0, inplace=True)
    stats.to_csv("./player_stats/{}-{}.csv".format(year-1,year))
    print("{} Done!".format(year))

