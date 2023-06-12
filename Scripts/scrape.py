import json
import os

import requests

from bs4 import BeautifulSoup


JSON_FOLDER_PATH = os.path.join(os.path.dirname(os.getcwd()), 'Lib')
AUTHORS_JSON_PATH = os.path.join(JSON_FOLDER_PATH, 'authors.json')
QUOTES_JSON_PATH = os.path.join(JSON_FOLDER_PATH, 'quotes.json')


def save_authors_to_json(names, born_dates, born_locations, descriptions):

    authors_list = []
    for name, b_date, b_location, description in zip(names, born_dates, born_locations, descriptions):
        author_dict = {
            'fullname': name.text,
            'born_date': str(b_date),
            'born_location': str(b_location),
            'description': str(description).replace('\n', '').strip()
        }
        authors_list.append(author_dict)

    with open(AUTHORS_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(authors_list, file, indent=2, ensure_ascii=False)


def save_quotes_to_json(authors_list, quotes_list, tags_list):
    quotes_json_list = []

    for i in range(len(quotes)):
        tags_for_quote = tags_list[i].find_all('a', class_='tag')
        quote_dict = {
            'tags': [tag_for_quote.text for tag_for_quote in tags_for_quote],
            'author': authors_list[i].text,
            'quote': quotes_list[i].text
        }
        quotes_json_list.append(quote_dict)

    with open(QUOTES_JSON_PATH, 'w', encoding='utf-8') as file:
        json.dump(quotes_json_list, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    base_url = 'https://quotes.toscrape.com/'
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.select('span.text')
    authors = soup.select('small.author')
    tags = soup.find_all('div', class_='tags')
    links_to_authors = soup.select('span a:not(.tag)')

    authors_born_dates = []
    authors_born_locations = []
    authors_description = []
    # Get list with links to every author about page
    for link in links_to_authors:
        link.attrs['href'] = base_url + link.attrs['href']
        response = requests.get(link.attrs['href'])
        soup = BeautifulSoup(response.text, 'html.parser')
        authors_born_dates.append(soup.select('span.author-born-date')[0].text)
        authors_born_locations.append(soup.select('span.author-born-location')[0].text)
        authors_description.append(soup.select('div.author-description')[0].text)

    save_authors_to_json(authors, authors_born_dates, authors_born_locations, authors_description)
    save_quotes_to_json(authors, quotes, tags)
