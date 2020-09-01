from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

years = list(range(2010, 2021))
salary_caps = {2010: 57700000.0, 2011: 58044000.0, 2012: 58044000.0, 2013: 58044000.0, 2014: 58679000.0, 2015: 63065000.0, 2016: 70000000.0, 2017: 94143000.0, 2018: 99093000.0, 2019: 101869000.0, 2020: 109140000.0}

for year in years:
    if year != 2020:
        url = "https://hoopshype.com/salaries/players/{}-{}/".format(year-1,year)
    else: 
        url = "https://hoopshype.com/salaries/players/"
    html = urlopen(url)
    soup = BeautifulSoup(html, features="html.parser")
    
    rows = soup.findAll('tr')
    headers = ['Player', 'Salary', 'Salary(*)']
    
    salaries = [[td.getText().replace("\n","").replace("\t","") for td in rows[i].findAll('td')[1:4]] for i in range(1,len(rows))]
    
    def format_salary(salary):
        s = int(salary[1:].replace(',', ''))
        return s
    
    def calc_salary_pct(salary, cap):
        return salary/cap *100

    df = pd.DataFrame(salaries, columns=headers)
    df['Salary'] = df['Salary'].apply(lambda x: format_salary(x))
    df['Salary(*)'] = df['Salary(*)'].apply(lambda x: format_salary(x))
    df['Salary(%)'] = df['Salary'].apply(lambda x: calc_salary_pct(x, salary_caps[year]))
    df.to_csv("./player_salaries/{}-{}.csv".format(year-1, year))
    print("{} Done!".format(year))
    
