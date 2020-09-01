from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

years = list(range(2010, 2021))
salary_caps = {2010: 57700000.0, 2011: 58044000.0, 2012: 58044000.0, 2013: 58044000.0, 2014: 58679000.0, 2015: 63065000.0, 2016: 70000000.0, 2017: 94143000.0, 2018: 99093000.0, 2019: 101869000.0, 2020: 109140000.0}

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
        if name[-2] == ' ':
            return name[:-3]
        else:
            return name[:-4]
    
    def format_salary(salary, year):
        s = float(salary[1:].replace(',', ''))
        return (s/salary_caps[year])*s

    df['Player'] = df['Player'].apply(lambda x: format_name(x))
    df['Salary'] = df['Salary'].apply(lambda x: format_salary(x, year))
    df.drop_duplicates(inplace=True)
    df.reset_index()
    df.to_csv("./player_salaries1/{}-{}.csv".format(year-1,year))
    print("{} Done!".format(year))

    