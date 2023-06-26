import pandas as pd

def assign_hyperlink (df):
    # Create a dictionary to store the shortest name link for each NDex number
    shortest_name_links = {}

    # Create a new DataFrame with the Pokémon information and the image tag with different hyperlinks
    pokemon_data = []

    for _, row in df.iterrows():
        pokemon_name = row['Name']
        pokemon_name_link = pokemon_name.replace(" ", "_")  # Replace spaces with underscores for the hyperlink
        pokemon_link = ""

        if row['NDex'] not in shortest_name_links:
            shortest_name_links[row['NDex']] = pokemon_name
        else:
            if len(pokemon_name) < len(shortest_name_links[row['NDex']]):
                shortest_name_links[row['NDex']] = pokemon_name

        pokemon_link = f"https://bulbapedia.bulbagarden.net/wiki/{shortest_name_links[row['NDex']]}_(Pok%C3%A9mon)"

        type_1 = f"<a href='https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/{row['Type 1']}.png' target='_blank'><img src='https://storage.googleapis.com/pokemon_pngs/Pokemon%20PNG%202/{row['Type 1']}.png' width='70'></a>"
        type_2 = ""
        if pd.notnull(row['Type 2']):
            type_2_url = f"https://github.com/echestnut22/Pokemon-Type-Combinations/raw/main/data/Pokemon%20PNGs/{row['Type 2']}.png"
            type_2 = f"<a href='{type_2_url}' target='_blank'><img src='{type_2_url}' width='70'></a>" if type_2_url != 'https://github.com/echestnut22/Pokemon-Type-Combinations/raw/main/data/Pokemon%20PNGs/None.png' else ""
           

        pokemon_data.append({
            '': f"<a href='{pokemon_link}' target='_blank'><img src='{row['Image']}' width='100'></a>",
            'Dex #': row['NDex'],
            'Name': row['Name'],
            'Type(s)': type_1 + " " + type_2,
            'Total': row['Total'],
            'HP': row['HP'],
            'Atk': row['Attack'],
            'Def': row['Defense'],
            'Sp. Atk': row['Sp. Atk'],
            'Sp. Def': row['Sp. Def'],
            'Spd': row['Speed']
        })
        
    # Update the hyperlinks for each Pokémon in the DataFrame using the shortest name for their NDex number.
    # Should usually ensure the original form of pokemon always gets assigned HyperLink
    for data in pokemon_data:
        ndex = data['Dex #']
        shortest_name = shortest_name_links[ndex]

        # Words to remove from the name for proper HyperLinks when Table is updated 
        words_to_remove = ["Mega", "X", "Y", "Alolan", "Hisuian", "Galarian", "Sunny", "Rainy", "Snowy", "Form", "Forme",
                           "Ultra", "Dusk", "Mane", "Dawn", "Roaming", "Chest", "Two-Segment", "Curly", "White Plumage",
                           "Female", "Male", "Therian", "Incarnate", "Ice", "Shadow", "Ryder", "Rapid", "Strike", "Style",
                           "Single", "Crowned Sword", "Hero of Many Battles", "Crowned Shield", "Hangry", "Mode", "Face",
                           "Amped", "Meteor", "Solo", "Pa'u", "Baile", "Sensu", "Pom-Pom", "Unbound", "Complete",
                           "Blade", "Shield", "Ash", "Solo", "Aria", "Pirouette", "Ordinary", "Theria", "Standard",
                           "Solo", "White-Striped", "Sky", "Land", "Origin", "Fan", "Mow", "Heat", "Sandy", "Cloak",
                           "Trash", "Plant", "Attack", "Solo", "Solo", "Wash", "Frost", "Primal", "Combat", "Blaze",
                           "Aqua", "Breed", "Zen"]

        # Remove words from name for proper HyperLinks
        for word in words_to_remove:
            shortest_name = shortest_name.replace(word, "")
        pokemon_name_link = shortest_name.replace(" ", "_").replace("Type", "Type:")
        pokemon_link = f"https://bulbapedia.bulbagarden.net/wiki/{pokemon_name_link}_(Pok%C3%A9mon)"
        data[''] = f"<a href='{pokemon_link}' {data['']}"
    
    return pokemon_data
