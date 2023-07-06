#PUT DESIRED DIRECTORY FOR IMAGES HERE
folder_path = ''


import csv
import requests
from bs4 import BeautifulSoup
import re

#Only downloads pokemon with 4 NDex numbers, Rearranges names properly and renames different forms. 
#Manually had to put in URLs to loop through d/t forbidden error. 

import os
import requests
from bs4 import BeautifulSoup
import re

# URLs of the pages with the images
urls = [
    "https://archives.bulbagarden.net/wiki/Category:Ken_Sugimori_Pok%C3%A9mon_artwork",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A052%0A0052Meowth-Alola.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A105%0A105Marowak+RG.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A164%0A164Noctowl+GS.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A253%0A0253Grovyle.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A402%0A0402Kricketune.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A529%0A0529Drilbur.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A668%0A0668Pyroar.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A815%0A0815Cinderace-Gigantamax.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Ken_Sugimori_Pok%C3%A9mon_artwork&filefrom=%2A963%0A0963Finizen.png#mw-category-media"
]

# Headers for the GET request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

# Get the regex patterns to exclude pixel data and match 4 digits in filenames
pixel_pattern = re.compile(r"\d+px-")
digit_pattern = re.compile(r"\d{4}")

# Get the regex pattern to match the different forms
form_pattern = re.compile(r"-(Mega_x|Mega_y|Alola|Galar|Hisui|Mega|Partner|Paladea)")

# Get the URL of each image and download it to a folder

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
for url in urls:
    # Send a GET request to the URL with the headers
    response = requests.get(url, headers=headers)

    # Use Beautiful Soup to parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the URL of each image and download it to a folder
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        img_filename = img_url.split('/')[-1]

        # Remove pixel data from the filename
        img_filename = re.sub(pixel_pattern, "", img_filename)

        # Skip downloading the image if it doesn't contain 4 digits in its filename
        if not re.search(digit_pattern, img_filename):
            continue

        try:
            # Send a GET request to the URL of the image with the headers
            response = requests.get(img_url, headers=headers)

            # Check if 'Mega', 'Alola', 'Galar', or 'Hisui' is at the end of the filename
            if re.search(form_pattern, img_filename):
                # Extract the pokemon name and move the form name to the beginning of the filename
                form_name = re.search(form_pattern, img_filename).group(0)[1:]
                pokemon_name = re.sub(form_pattern, "", img_filename)
                img_filename = f"{form_name} {pokemon_name}"
                
            # Replace 'Hisui' with 'Hisuian', 'Galar' with 'Galarian', and 'Alola' with 'Alolan'
            img_filename = re.sub(r"\bHisui\b", "Hisuian", img_filename)
            img_filename = re.sub(r"\bGalar\b", "Galarian", img_filename)
            img_filename = re.sub(r"\bAlola\b", "Alolan", img_filename)
            
            # Replace URL-encoded apostrophe with an actual apostrophe. For Farfetch'd
            img_filename = img_filename.replace("%27", "'")

            # Remove the 4 digits from the filename
            img_filename = re.sub(digit_pattern, "", img_filename)

            # Replace "-" and "_" with a space
            img_filename = re.sub(r"[-_]", " ", img_filename)

            # Extract the form names from the filename using regex
            matches = re.findall(form_pattern, img_filename)
            if matches:
                form_names = [match.replace("_", " ").capitalize() for match in matches]
                img_filename = re.sub(form_pattern, "", img_filename).strip()
                new_filename = f"{form_names[-1]} {' '.join(form_names[:-1])} {img_filename}" if form_names[-1] != "Mega" else f"{form_names[-2]} Mega {img_filename}"
            else:
                new_filename = f"{img_filename}"
            
            
            # Save the image to a file in the specified folder
            with open(os.path.join(folder_path, new_filename), 'wb') as f:
                f.write(response.content)
                print(f"Downloaded {new_filename}")
        except:
            print(f"Failed to download {img_filename}")



#Downloading PNGs of type icons for display 

#Define the list of URLs to scrape
url_list = [
    "https://archives.bulbagarden.net/w/index.php?title=Category:Type_icons&fileuntil=FlyingIC+LA.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Type_icons&filefrom=FlyingIC+LA.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Type_icons&filefrom=PMD+DX+Dragon+type.png#mw-category-media",
    "https://archives.bulbagarden.net/w/index.php?title=Category:Type_icons&filefrom=WaterIC+RSE.png#mw-category-media"
]

# Define the regex pattern to extract the desired part of the filename
regex_pattern = r"(?<=-)[^-_]+(?=_)"

# Loop through each URL and download the images containing "BDSP"
for url in url_list:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for image in soup.find_all("img"):
        if "BDSP" in image["src"]:
            image_url = "https:" + image["src"].replace("https:", "")
            image_name = os.path.basename(image_url)
            match = re.search(regex_pattern, image_name)
            if match:
                new_image_name = match.group(0).replace("IC", "") + ".png"
                new_image_path = os.path.join(folder_path, new_image_name)
                with open(new_image_path, "wb") as f:
                    f.write(requests.get(image_url).content)