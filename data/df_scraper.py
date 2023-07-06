import csv
import requests
from bs4 import BeautifulSoup


#Get CSV of all pokemon with pokedex number, name, type(s), stats. Has megas and alterantive forms. No gigantimax 
#Uncleaned version of dataframe. Cleaned version provided in repository as pokedex.csv 
#Code for cleaning dataframe provided below in docstring 

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




"""

#Cleaning DataFrame
#Removing name redundance for alternative forms

df = pd.read_csv('C:/Users/ericc/.vscode/Jupyter/Pokemon/pokedex.csv')
# rename the 'Pokedex Number' column to 'NDex'
df = df.rename(columns={"Pokedex Number": "NDex"})
#Have all NDex numbers have four digits (will be easier for matching PNGs later)
df['NDex'] = df['NDex'].astype(str).str.zfill(4)

alternative_forms = ["Mega", "Alolan", "Partner", "Galarian", "Hisuian"]

# Create a regular expression pattern to match the preceding words
pattern = r"\b\w+\b(?=\s+(?:" + "|".join(alternative_forms) + r"))"

# Apply the lambda function to the "Name" column to remove preceding words
df["Name"] = df["Name"].apply(lambda x: re.sub(pattern, "", x).strip())

# Create a list of replacement rules
replacement_rules = {
    "Farfetch' Galarian Farfetch'd": "Galarian Farfetch'd",
    "Mr.  Galarian Mr. Mime": "Galarian Mr. Mime",
    "Kyogre Primal Kyogre":"Kyogre Primal",
    "Groudon Primal Groudon": "Groudon Primal",
    "Wooper Paldean Wooper":"Paladean Wooper",
    "Rotom Heat Rotom": "Rotom Heat",
    "Rotom Wash Rotom": "Rotom Wash",
    "Rotom Frost Rotom": "Rotom Frost",
    "Rotom Fan Rotom": "Rotom Fan",
    "Rotom Mow Rotom": "Rotom Mow",
    
    "Kyurem White Kyurem": "Kyurem White",
    "Kyurem Black Kyurem": "Kyurem Black",
    "Greninja Ash-Greninja": "Ash Greninja",
    
    "Pumpkaboo Average Size": "Pumpkaboo",
    
    "Gourgeist Average Size": "Gourgeist",
    
    "Hoopa Hoopa Confined": "Hoopa Confined",
    "Hoopa Hoopa Unbound": "Hoopa Unbound",
    
    "Type: Null": "Type Null",
    
    "Maushold Family of Four": "Maushold",
    "Maushold Family of Three": "Maushold Three",
    
    "Palafin Zero Form": "Palafin",
    
    "Zygarde 50% Forme": "Zygarde",
    
    "Necrozma Ultra Necrozma": "Necrozma Ultra",
    "Necrozma Dusk Mane Necrozma": "Necrozma Dusk Mane",
    "Necrozma Dawn Wings Necrozma": "Necrozma Dawn Wings",
    
    "Ho-oh": "Ho-Oh",
    
    "Darmanitan Standard Mode": "Darmanitan",
    "Galarian Standard Mode": "Galarian Darmanitan",
    "Galarian Zen Mode": "Galarian Darmanitan Zen Mode",
    
} 

# Apply the replacement rules to the "Name" column
df["Name"] = df["Name"].replace(replacement_rules)

#Remove Some pokemon from df 
df = df[~df['Name'].isin(['Pumpkaboo Small Size', 'Pumpkaboo Large Size', 'Pumpkaboo Super Size', 'Gourgeist Small Size', 'Gourgeist Large Size', 'Gourgeist Super Size', 'Rockruff Own Tempo Rockruff', 'Eternatus Eternamax','Partner Eevee','Giratina Altered Forme'])]

#Ensure pokemon of first form comes first in DataFrame. Important for hyperlinks
def sort_group(group):
    return group.sort_values(by='Name', key=lambda x: x.str.len())
df = df.groupby('NDex', group_keys=False).apply(sort_group)

#Make all NDex numbers have 4 digits.
df['NDex'] = df['NDex'].astype(str).str.zfill(4)


"""