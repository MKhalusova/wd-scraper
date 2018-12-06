from bs4 import BeautifulSoup
import requests
from time import sleep
import csv

url = "https://walkingdead.fandom.com/wiki/TV_Series_Characters"

def get_links_to_characters(link):
    wd_characters = []
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html5lib')
    a_tags = soup.findAll('a', "image image-thumbnail link-internal", href=True)
    for tg in a_tags:
        if "TV_Series" in tg["href"]:
            wd_characters.append("https://walkingdead.fandom.com" + tg["href"])
    wd_characters = ["https://walkingdead.fandom.com/wiki/Jeffery_(TV_Series)" if x=="https://walkingdead.fandom.com/wiki/Jeffrey_(TV_Series)" else x for x in wd_characters]
    return wd_characters

def get_character_info(link_to_character_page):
    html = requests.get(link_to_character_page).text
    soup = BeautifulSoup(html, 'html5lib')
    character = {}
    try:
        character_info = soup.find('aside')
        character["name"] = character_info.h2.text.strip()
        items = character_info.findAll('div', "pi-item pi-data pi-item-spacing pi-border-color")
        for item in items:
            key = item.find('h3').text
            character[key] = item.find('div', "pi-data-value pi-font").text
    except:
        print("couldn't scrape: ", link_to_character_page)
    return character


if __name__ == "__main__":
    links_to_characters = get_links_to_characters(url)
    with open('wd_char.csv', 'w', newline='') as csvfile:
        fieldnames = ["name", "Actor", "Gender","Hair","Age","Occupation","Family","First Appearance", "Last Appearance",
                      "Death Episode", "Cause of Death", "Status", "Series Lifespan", "Ethnicity"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for link in links_to_characters:
            char_data = get_character_info(link)
            if not char_data: continue
            else:
                writer.writerow(char_data)
                sleep(10)





