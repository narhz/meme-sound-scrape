from bs4 import BeautifulSoup as bs
import requests
import os

from pprint import pprint




BASE_URL = 'https://www.myinstants.com'


def get_page(num):
    page_url = f'/categories/memes/?page={str(num)}&name=memes'
    soup = bs(requests.get(BASE_URL + page_url).content, 'html.parser')
    return soup


def get_links(soup_obj):
    links = []
    forbid = ['*', '"', "'", '?', '/', '>', '<', '!', ':', '|']
    for a_tag in soup_obj.find_all('a', class_='instant-link'):
        req = requests.get(BASE_URL + a_tag['href']).content
        name = a_tag.text + '.mp3'

        for char in forbid:
            if char in name:
                name = name.replace(char, '')

        buttons = bs(req, 'html.parser').find_all('a', class_='waves-effect waves-light btn blue white-text')
        
        for button in buttons:
            if button.text == 'Download MP3':
                links.append({'name': name, 'link': BASE_URL + button['href']})

    return links


def dl_link(item):
    if not os.path.exists('sounds/' + item.get('name')):
        req = requests.get(item.get('link')).content
        with open('sounds/' + item.get('name'), 'wb') as sound_file:
            sound_file.write(req)



def create_dir():
    if not os.path.exists('sounds'):
        os.makedirs('sounds')


def run():
    create_dir()

    page_num = 1
    while True:
        page = get_page(page_num)
        links = get_links(page)

        if not links:
            break

        for link in links:
            dl_link(link)

        page_num += 1


if __name__ == "__main__":
    run()