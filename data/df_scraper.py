import csv
import requests
from bs4 import BeautifulSoup


#Get CSV of all pokemon with pokedex number, name, type(s), stats. Has megas and alterantive forms. No gigantimax 

url = 'https://pokemondb.net/pokedex/all'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'data-table'})

with open('pokedex.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Pokedex Number', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'])
    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        pokedex_number = columns[0].text.strip().zfill(4)
        name = columns[1].text.strip()
        types = columns[2].text.strip().split(' ')
        type_1 = types[0]
        type_2 = types[1] if len(types) == 2 else None
        total = columns[3].text.strip()
        hp = columns[4].text.strip()
        attack = columns[5].text.strip()
        defense = columns[6].text.strip()
        sp_atk = columns[7].text.strip()
        sp_def = columns[8].text.strip()
        speed = columns[9].text.strip()
        writer.writerow([pokedex_number, name, type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed])



