from pathlib import Path
from bs4 import BeautifulSoup

html_path = Path('./html/')
song_path = Path('./songs/')

def parse_html_file(file_path):
    with open(file_path, 'r', encoding="utf8") as html_file:
        html_content = html_file.read()
        soup = BeautifulSoup(html_content, 'html5lib')
        return soup

def get_nice_song_name(soup):

    def get_title():
        h3s = soup.find_all('h3')
        for h3 in h3s:
             next_node = h3.find_next_sibling()
             if next_node.name == 'h1':
                 return next_node.string

    def get_artist():
        h3s = soup.find_all('h3')
        for h3 in h3s:
             prev_node = h3.find_next_sibling()
             if prev_node.name == 'h1':
                 return h3.string


    def find_secondary_prop_by_name(name):
        secondary_spans = soup.find_all('span', class_="ant-typography-secondary")
        for span in secondary_spans:
            if span.string == name:
                prev_node = span.previous_sibling
                return prev_node.string

    new_song_name = f"{get_title().lower()}; {find_secondary_prop_by_name('BPM')}; {find_secondary_prop_by_name('camelot')}; {get_artist().lower()};"
    print(f"generted name is {new_song_name}")
    
    return new_song_name


for html_file in html_path.iterdir():
    for song in song_path.iterdir():
        if html_file.stem == song.stem:
            if html_file.stem == ".gitkeep": 
                continue
            print(f"processing {html_file.stem}")
            html_full_name = html_path.joinpath(html_file.name)
            soup = parse_html_file(html_full_name)
            new_song_name = get_nice_song_name(soup) + song.suffix
            print(f"> > > new_song_name{new_song_name}")
            song_full_name = song_path.joinpath(song.name )
            print(f"> > > song_full_name{song_full_name}")
            song.rename(song_path.joinpath(new_song_name))



