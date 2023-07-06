#SPECIFY DIRECTORY THAT CONTAINS IMAGES HERE

dir_path = r''

import os
import pandas as pd

#CHANGE NAMES OF IMAGES 
#Had to manually change Nidoran male and female names in files d/t using male and female signs 

# define dictionary mapping
name_mapping = {
    "Tauros Paldea Combat.png": "Tauros Combat Breed.png",
    "Tauros Paldea Blaze.png": "Tauros Blaze Breed.png",
    "Tauros Paldea Aqua.png": "Tauros Aqua Breed.png",
    
    "Ho Oh.png": "Ho-Oh.png",
    
    "Wooper Paldea.png": "Paladean Wooper.png",
    
    "Castform Sunny.png": "Castform Sunny Form.png",
    "Castform Rainy.png": "Castform Rainy Form.png",
    "Castform Snowy.png": "Castform Snowy Form.png",
    
    "Deoxys.png": "Deoxys Normal Forme.png",
    "Deoxys Attack.png": "Deoxys Attack Forme.png",
    "Deoxys Defense.png": "Deoxys Defense Forme.png",
    "Deoxys Speed.png": "Deoxys Speed Forme.png",
    
    "Burmy Plant.png": "Burmy Plant Cloak.png",
    "Burmy Sandy.png": "Burmy Sandy Cloak.png",
    "Burmy Trash.png": "Burmy Trash Cloak.png",
    
    "Wormadam Plant.png": "Wormadam Plant Cloak.png",
    "Wormadam Sandy.png": "Wormadam Sandy Cloak.png",
    "Wormadam Trash.png": "Wormadam Trash Cloak.png",
    
    "Mime Jr.png": "Mime Jr..png",
    
    "Porygon Z.png": "Porygon-Z.png",
    
    "Dialga Origin.png": "Dialga Origin Forme.png",
    "Palkia Origin.png": "Palkia Origin Forme.png",
    "Giratina Origin.png": "Giratina Origin Forme.png",
    
    "Shaymin.png": "Shaymin Land Forme.png",
    "Shaymin Sky.png": "Shaymin Sky Forme.png",
    
    "Basculin Red.png": "Basculin Red-Striped Form.png",
    "Basculin Blue.png": "Basculin Blue-Striped Form.png",
    "Basculin White.png": "Basculin White-Striped Form.png",
    
    "Darmanitan.png": "Darmanitan Standard Mode.png",
    "Darmanitan Zen.png": "Darmanitan Zen Mode.png",
    "Galarian Darmanitan.png": "Galarian Standard Mode.png",
    "Galarian Darmanitan Zen.png": "Galarian Zen Mode.png",
    
    "Tornadus.png": "Tornadus Incarnate Forme.png",
    "Tornadus Therian.png": "Tornadus Therian Forme.png",
    "Thundurus.png": "Thundurus Incarnate Forme.png",
    "Thundurus Therian.png": "Thundurus Therian Forme.png",
    "Landorus.png": "Landorus Incarnate Forme.png",
    "Landorus Therian.png": "Landorus Therian Forme.png",
    
    
    "Keldeo.png": "Keldeo Ordinary Form.png",
    "Keldeo Resolute.png": "Keldeo Resolute Form.png",
    
    "Meloetta.png": "Meloetta Aria Forme.png",
    "Meloetta Pirouette.png": "Meloetta Pirouette Forme.png",
    
    "Greninja Ash.png": "Ash Greninja.png",
    
    "Aegislash Shield.png": "Aegislash Shield Forme.png",
    "Aegislash Blade.png": "Aegislash Blade Forme.png",
    
    
    "Zygarde Core.png": "Zygarde 50% Forme.png",
    "Zygarde 10Percent.png": "Zygarde 10% Forme.png",
    "Zygarde Complete.png": "Zygarde Complete Forme.png",
    
    
    "Oricorio.png": "Oricorio Baile Style.png",
    "Oricorio Pom Pom.png": "Oricorio Pom-Pom Style.png",
    "Oricorio Pa'u.png": "Oricorio Pa'u Style.png",
    "Oricorio Sensu.png": "Oricorio Sensu Style.png",
    

    "Lycanroc.png": "Lycanroc Midday Form.png",
    "Lycanroc Midnight.png": "Lycanroc Midnight Form.png",
    "Lycanroc Dusk.png": "Lycanroc Dusk Form.png",
    
    "Wishiwashi.png": "Wishiwashi Solo Form.png",
    "Wishiwashi School.png": "Wishiwashi School Form.png",
    
    "Minior.png": "Minior Meteor Form.png",
    "Minior Core.png": "Minior Core Form.png",
    
    "Jangmo o.png": "Jangmo-o.png",
    "Hakamo o.png": "Hakamo-o.png",
    "Kommo o.png": "Kommo-o.png",
    
    "Necrozma Dusk Mane.png": "Necrozma Dusk Mane Necrozma.png",
    "Necrozma Dawn Wings.png": "Necrozma Dawn Wings Necrozma.png",
    "Necrozma Ultra.png": "Necrozma Ultra Necrozma.png",
    
    "Toxtricity Amped.png": "Toxtricity Amped Form.png",
    "Toxtricity Low Key.png": "Toxtricity Low Key Form.png",
    
    "Eiscue.png": "Eiscue Ice Face.png",
    "Eiscue Noice.png": "Eiscue Noice Face.png",
    
    "Morpeko Full.png": "Morpeko Full Belly Mode.png",
    "Morpeko Hangry.png": "Morpeko Hangry Mode.png",
    
    "Zacian Hero.png": "Zacian Hero of Many Battles.png",
    "Zacian 2.png": "Zacian Crowned Sword.png",
    "Zamazenta Hero.png": "Zamazenta Hero of Many Battles.png",
    "Zamazenta 2.png": "Zamazenta Crowned Shield.png",
    
    "Urshifu Single Strike.png": "Urshifu Single Strike Style.png",
    "Urshifu Rapid Strike.png": "Urshifu Rapid Strike Style.png",
    
    "Enamorus.png": "Enamorus Incarnate Forme.png",
    "Enamorus Therian.png": "Enamorus Therian Forme.png",

    
    "Squawkabilly.png": "Squawkabilly Green Plumage.png",
    "Squawkabilly Blue.png": "Squawkabilly Blue Plumage.png",
    "Squawkabilly Yellow.png": "Squawkabilly Yellow Plumage.png",
    "Squawkabilly White.png": "Squawkabilly White Plumage.png",
    
    
    "Palafin Hero.png": "Palafin Hero Form.png",
    
    "Tatsugiri.png": "Tatsugiri Curly Form.png",
    "Tatsugiri Droopy.png": "Tatsugiri Droopy Form.png",
    "Tatsugiri Stretchy.png": "Tatsugiri Stretchy Form.png",
    
    "Dudunsparce.png": "Dudunsparce Two-Segment Form.png",
    "Dudunsparce Three.png": "Dudunsparce Three-Segment Form.png",
    
    "Gimmighoul.png": "Gimmighoul Chest Form.png",
    "Gimmighoul Roaming.png": "Gimmighoul Roaming Form.png",
    
    "Wo Chien.png": "Wo-Chien.png",
    "Chien Pao.png": "Chien-Pao.png",
    "Ting Lu.png": "Ting-Lu.png",
    "Chi Yu.png": "Chi-Yu.png",
    "Hoopa.png": "Hoopa Confined.png",
    "Flab%C3%A9b%C3%A9.png": "Flabébé.png",
    "Galarian Darmanitan Zen": "Galarian Darmanitan Zen Mode",
    
    #Replace ' with _ for easier image assignment
    "Farfetch'd.png": "Farfetch_d.png",
    "Galarian Farfetch'd.png": "Galarian Farfetch_d.png",
    "Oricorio Pa'u Style.png": "Oricorio Pa_u Style.png",
    "Sirfetch'd.png": "Sirfetch_d.png",
    
}

# iterate through each file in directory
for filename in os.listdir(dir_path):
    # check if file is a PNG image
    if filename.endswith('.png'):
        # check if file's name exists in dictionary mapping
        if filename in name_mapping:
            # get the new name for the file
            new_filename = name_mapping[filename]
            # rename the file
            try:
                os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
            except FileExistsError:
                pass




