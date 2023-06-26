import pandas as pd
import re
import os

ALTERNATE_FORMS = ["Mega", "Alolan", "Partner", "Galarian", "Hisuian"]

REPLACEMENT_RULES = {
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

TYPE_COLORS = {
    'Fairy': '#EE99AC',
    'Bug': '#A8B820',
    'Dark': '#705848',
    'Dragon': '#7038F8',
    'Electric': '#F8D030',
    'Fighting': '#C03028',
    'Fire': '#F08030',
    'Flying': '#A890F0',
    'Ghost': '#705898',
    'Grass': '#78C850',
    'Ground': '#E0C068',
    'Ice': '#98D8D8',
    'Normal': '#A8A878',
    'Poison': '#A040A0',
    'Psychic': '#F85888',
    'Rock': '#B8A038',
    'Steel': '#B8B8D0',
    'Water': '#6890F0'
}

#Type effectiveness dicitonary for type calculator and image assignment 
TYPE_EFFECTIVENESS = {
    'Normal': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Normal.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 0, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1}
    },
    'Fire': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Fire.png',
        'effectiveness': {'Normal': 1, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 0.5, 'Ice': 0.5, 'Fighting': 1, 'Poison': 1, 'Ground': 2, 'Flying': 1, 'Psychic': 1, 'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 0.5}
    },
    'Water': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Water.png',
        'effectiveness': {'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 2, 'Grass': 2, 'Ice': 0.5, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1}
    },
    'Electric': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Electric.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 0.5, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 2, 'Flying': 0.5, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 0.5, 'Fairy': 1}
    },
    'Grass': {
    'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Grass.png',
    'effectiveness': {'Normal': 1, 'Fire': 2, 'Water': 0.5, 'Electric': 0.5, 'Grass': 0.5, 'Ice': 2, 'Fighting': 1, 'Poison': 2, 'Ground': 0.5, 'Flying': 2, 'Psychic': 1, 'Bug': 2, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1}
    },
    'Ice': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Ice.png',
        'effectiveness': {'Normal': 1, 'Fire': 2, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 2, 'Psychic': 2, 'Bug': .5, 'Rock': .5, 'Ghost': 1, 'Dragon': 1, 'Dark': .5, 'Steel': 2, 'Fairy': 2}
    },
    'Fighting': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Fighting.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 2, 'Psychic': 2, 'Bug': 0.5, 'Rock': .5, 'Ghost': 1, 'Dragon': 1, 'Dark': .5, 'Steel': 1, 'Fairy': 2}
    },
    'Poison': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Poison.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 0.5, 'Ice': 1, 'Fighting': 0.5, 'Poison': 0.5, 'Ground': 2, 'Flying': 1, 'Psychic': 2, 'Bug': 0.5, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 0.5}
    },
    'Ground': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Ground.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 2, 'Electric': 0, 'Grass': 2, 'Ice': 2, 'Fighting': 1, 'Poison': 0.5, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1}
    },
    'Flying': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Flying.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 2, 'Grass': 0.5, 'Ice': 2, 'Fighting': 0.5, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 0.5, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1}
    },
    'Psychic': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Psychic.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 0.5, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 0.5, 'Bug': 2, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 2, 'Steel': 1, 'Fairy': 1}
    },
    'Bug': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Bug.png',
        'effectiveness': {'Normal': 1, 'Fire': 2, 'Water': 1, 'Electric': 1, 'Grass': 0.5, 'Ice': 1, 'Fighting': 0.5, 'Poison': 1, 'Ground': 0.5, 'Flying': 2, 'Psychic': 1, 'Bug': 1, 'Rock': 2, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1}
    },
    'Rock': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Rock.png',
        'effectiveness': {'Normal': 0.5, 'Fire': 0.5, 'Water': 2, 'Electric': 1, 'Grass': 2, 'Ice': 1, 'Fighting': 2, 'Poison': 0.5, 'Ground': 2, 'Flying': 0.5, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 2, 'Fairy': 1}
    },
    'Ghost': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Ghost.png',
        'effectiveness': {'Normal': 0, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 0, 'Poison': 0.5, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 0.5, 'Rock': 1, 'Ghost': 2, 'Dragon': 1, 'Dark': 2, 'Steel': 1, 'Fairy': 1}
    },
    'Dragon': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Dragon.png',
        'effectiveness': {'Normal': 1, 'Fire': 0.5, 'Water': 0.5, 'Electric': 0.5, 'Grass': 0.5, 'Ice': 2, 'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 2, 'Dark': 1, 'Steel': 1, 'Fairy': 2}
    },
    'Dark': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Dark.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 2, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 0, 'Bug': 1, 'Rock': 1, 'Ghost': 0.5, 'Dragon': 1, 'Dark': 0.5, 'Steel': 1, 'Fairy': 2}
    },
    'Steel': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Steel.png',
        'effectiveness': {'Normal': 0.5, 'Fire': 2, 'Water': 1, 'Electric': 1, 'Grass': 0.5, 'Ice': 0.5, 'Fighting': 2, 'Poison': 0, 'Ground': 2, 'Flying': 0.5, 'Psychic': 0.5, 'Bug': 0.5, 'Rock': 0.5, 'Ghost': 1, 'Dragon': 0.5, 'Dark': 1, 'Steel': 0.5, 'Fairy': 0.5}
    },
    'Fairy': {
        'image_url': 'https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/Fairy.png',
        'effectiveness': {'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1, 'Fighting': 0.5, 'Poison': 2, 'Ground': 1, 'Flying': 1, 'Psychic': 1, 'Bug': 0.5, 'Rock': 1, 'Ghost': 1, 'Dragon': 0, 'Dark': 0.5, 'Steel': 2, 'Fairy': 1}
        },
    #Added None to dictionary to prevent KeyErrors. Just x1 for all types 
    'None': {
        'effectiveness': {
            'Normal': 1, 'Fire': 1, 'Water': 1, 'Electric': 1, 'Grass': 1, 'Ice': 1,
            'Fighting': 1, 'Poison': 1, 'Ground': 1, 'Flying': 1, 'Psychic': 1,
            'Bug': 1, 'Rock': 1, 'Ghost': 1, 'Dragon': 1, 'Dark': 1, 'Steel': 1, 'Fairy': 1
        }
    }

}


def create_dataframe():

    df = pd.read_csv('https://raw.githubusercontent.com/echestnut22/Pokemon-Type-Combinations/main/data/pokedex.csv')

    df = df.rename(columns={"Pokedex Number": "NDex"})

    df['NDex'] = df['NDex'].astype(str).str.zfill(4)

    # Create a regular expression pattern to match the preceding words
    pattern = r"\b\w+\b(?=\s+(?:" + "|".join(ALTERNATE_FORMS) + r"))"

    # Apply the lambda function to the "Name" column to remove preceding words
    df["Name"] = df["Name"].apply(lambda x: re.sub(pattern, "", x).strip())

    df["Name"] = df["Name"].replace(REPLACEMENT_RULES)

    #Remove Irrelevant pokemon from df 
    df = df[~df['Name'].isin(['Pumpkaboo Small Size', 'Pumpkaboo Large Size', 'Pumpkaboo Super Size', 'Gourgeist Small Size', 'Gourgeist Large Size', 'Gourgeist Super Size', 'Rockruff Own Tempo Rockruff', 'Eternatus Eternamax','Partner Eevee','Giratina Altered Forme'])]

    #Ensure pokemon of first form comes first in DataFrame. Important for hyperlinks
    def sort_group(group):
        return group.sort_values(by='Name', key=lambda x: x.str.len())
    df = df.groupby('NDex', group_keys=False).apply(sort_group)

    # Add a new column with image paths for every Pokemon using Google API(image rendering too slow with GitHub)
    #Replace ' with _ for Farfetch'd and other pokemon with apostrophe in name.
    df['Image'] = df['Name'].str.replace("'", "_").apply(lambda x: f"https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/{x}.png")


    return df

def sort_dataframe(df_filtered, sort_by):
    if sort_by == 'NDex':
        df_filtered = df_filtered.sort_values(by='NDex')
    elif sort_by == 'Name':
        df_filtered = df_filtered.sort_values(by='Name')
    elif sort_by == 'Attack':
        df_filtered = df_filtered.sort_values(by='Attack', ascending=False)
    elif sort_by == 'Defense':
        df_filtered = df_filtered.sort_values(by='Defense', ascending=False)
    elif sort_by == 'Total':
        df_filtered = df_filtered.sort_values(by='Total', ascending=False)
    elif sort_by == 'Sp. Atk':
        df_filtered = df_filtered.sort_values(by='Sp. Atk', ascending=False)
    elif sort_by == 'Sp. Def':
        df_filtered = df_filtered.sort_values(by='Sp. Def', ascending=False)
    elif sort_by == 'HP':
        df_filtered = df_filtered.sort_values(by='HP', ascending=False)
    elif sort_by == 'Speed':
        df_filtered = df_filtered.sort_values(by='Speed', ascending=False)
    return df_filtered