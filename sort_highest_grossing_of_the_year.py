import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_highest-grossing_films'

content = requests.get(url)
#print(content.content)
soup = BeautifulSoup(content.content, 'html.parser')
gross_table = soup.find_all('table', class_ = "wikitable plainrowheaders")
gross_table_by_year = list(gross_table)[1]
gross_table = gross_table[0]
#print(gross_table_by_year.find_all('tr'))
count = 0
with open('highest_gross.txt', 'w') as r:
    for row in gross_table_by_year.find_all('tr'):
        for cell in row.find_all('td'):

            if len(cell.find_all('span')) > 0:
                span_list = list()
                for span in cell.find_all('span'):
                    span_list.append(span)
                r.write(span_list[0].text.replace('$','').replace(',','') + "::")

            else:
                r.write(cell.text.strip("\n").replace('$','').replace(',','') + "::")

        r.write("\n")

gross_dict = dict()
with open('highest_gross.txt', 'r') as data:
    for line in data:
        if line and line[0].isalpha():
            line = line.strip()
            columns = line.split("::")
            title, gross = columns[0], columns[1].split(" ")[0]
            if title in gross_dict:
                gross_dict[title] = float(gross)
            else:
                gross_dict[title] = float(gross)

#print(gross_dict)

for title, income in sorted(list(gross_dict.items()), key=lambda x:x[1], reverse=True)[:5]:
    print(title , income)
