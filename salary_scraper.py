from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

years = list(range(2010, 2021))

for year in years:
    url = "http://www.espn.com/nba/salaries/_/year/{}/seasontype/3".format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html.parser")
    salaries = []
    headers = ['Player', 'Team', 'Salary']

    pnum = int(soup.find('div', {"class": "page-numbers"}).getText()[-2:])
    rows = soup.findAll('tr', class_=lambda x: x != "colhead")
    salaries += [[td.getText() for td in rows[i].find_all('td')[1:]] for i in range(len(rows))]

    for page in range(0, pnum + 1):
        url = "http://www.espn.com/nba/salaries/_/year/{}/page/{}/seasontype/3".format(year, page)
        html = urlopen(url)
        soup = BeautifulSoup(html, features="html.parser")
        rows = soup.findAll('tr', class_=lambda x: x != "colhead")
        salaries += [[td.getText() for td in rows[i].find_all('td')[1:]] for i in range(len(rows))]
    df = pd.DataFrame(salaries, columns=headers)

    def format_name(name):
        if name[-1] == 'C':
            return name[:-3]
        else:
            return name[:-4]
    
    def format_salary(salary):
        return int(salary[1:].replace(',',''))

    df['Player'] = df['Player'].apply(lambda x: format_name(x))
    df['Salary'] = df['Salary'].apply(lambda x: format_salary(x))
    df.drop_duplicates(inplace=True)
    df.reset_index()
    df.to_csv("./player_salaries/{}-{}.csv".format(year-1,year))
    print("{} Done!".format(year))
