# Pokemon-Type-Combinations

This repository provides a visualization of different Pokemon types with a chord diagram using a locally hosted HTML page. A table is also featured that can be filtered by pokemon types and stats. The table is accompanied by a type effectiveness calculator, providing a useful team composition tool for players.

## Prerequisites
Ensure you have the following installed on your machine:
- [Python 3.6 or above](https://www.python.org/downloads/)
- [pip (Python package installer)](https://pip.pypa.io/en/stable/installation/)

## Example Video

Click the video below to see application in use.

[![Pokemon](http://img.youtube.com/vi/FIli4OFn-OM/0.jpg)](http://www.youtube.com/watch?v=FIli4OFn-OM "Pokemon Type Combinations")




## Installation
### 1. Download or Clone the Repository

If you want to download the repository, click on Code at the top of this page and select Download ZIP. Extract the zip file to a location of your choosing.

If you have git installed, you can clone the repository. Open a command prompt or terminal and navigate to where you want to clone the repository to (i.e., cd Desktop). Use the following command to clone:
```
git clone https://github.com/echestnut22/Pokemon-Type-Combinations
```


### 2. Setting Up a Virtual Environment (optional)

Before installing the project's dependencies, it's recommended to set up a Python virtual environment. This helps to avoid conflicts with other       installed Python packages that may exist on your system.

Use the following commands to create and activate a new virtual environment:

On Windows:

```
python -m venv venv
.\venv\Scripts\activate
```
On MacOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Python Packages
Install requirements and packages by running:
```
pip install .
```

### 4. Running the application 
To run application as localhost:
```
python main.py
```


## Downloading Pokemon Images
Images used for this project are the work of artist Ken Sugimori found here https://archives.bulbagarden.net/wiki/Category:Ken_Sugimori_Pok%C3%A9mon_artwork

This repository assigns images to Pokemon via a public google bucket. If one wishes to download the images used in this project, you can run the image_scraper.py file in the data folder. NOTE: This script will require the user to manually enter the directory they would like to download these images found at the top of the script. 

Python scripts have also been included for renaming images for better readability as well as scraping and organizing dataframe (although clean dataframe is included in repository as pokedex.csv)
