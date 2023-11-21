import requests
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ASCII art for the name TempoTrove
print(r"""
 
  _______                      _______                 
 |__   __|                    |__   __|                
    | | ___ _ __ ___  _ __   ___ | |_ __ _____   _____ 
    | |/ _ \ '_ ` _ \| '_ \ / _ \| | '__/ _ \ \ / / _ \
    | |  __/ | | | | | |_) | (_) | | | | (_) \ V /  __/
    |_|\___|_| |_| |_| .__/ \___/|_|_|  \___/ \_/ \___|
                     | |                               
                     |_|                               
 """ )

# The directory to save downloaded songs
download_dir = "DownloadedSongs"

# Create the download directory if it doesn't exist
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

def download_song(song_url, song_name):
    try:
        response = requests.get(song_url, stream=True)
        response.raise_for_status()

        # Set the path to save the downloaded song
        save_path = os.path.join(download_dir, f"{song_name}.mp3")

        # Download the song using urlretrieve
        urlretrieve(song_url, save_path)

        print(f"Downloaded {song_name} to {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {song_name}: {e}")

def search_and_download_mp3skull(song_name):
    search_url = f"http://mp3skull.com/mp3/{song_name.replace(' ', '_')}.html"
    try:
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        download_link = soup.find('a', {'rel': 'nofollow', 'class': 'download'})
        if download_link:
            song_url = download_link['href']
            download_song(song_url, song_name)
        else:
            print("No results found for the song on mp3skull.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def search_and_download_tubidy(song_name):
    search_url = f"https://tubidy.mobi/search/{song_name.replace(' ', '-')}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        download_link = soup.find('a', {'class': 'download'})
        if download_link:
            song_url = "https://tubidy.mobi" + download_link['href']
            download_song(song_url, song_name)
        else:
            print("No results found for the song on tubidy.mobi.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def search_and_download_mp3chief(song_name):
    search_url = f"http://mp3chief.com/mp3/{song_name.replace(' ', '_')}.html"
    try:
        response = requests.get(search_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        download_link = soup.find('a', {'title': 'Download'})
        if download_link:
            song_url = download_link['href']
            download_song(song_url, song_name)
        else:
            print("No results found for the song on mp3chief.com.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def display_menu():
    print("\n----- TempoTrove Menu -----")
    print("1. Search and Download a Song from mp3skull")
    print("2. Search and Download a Song from tubidy.mobi")
    print("3. Search and Download a Song from mp3chief.com")
    print("4. Exit")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            song_name = input("Enter the name of the song: ")
            search_and_download_mp3skull(song_name)
        elif choice == "2":
            song_name = input("Enter the name of the song: ")
            search_and_download_tubidy(song_name)
        elif choice == "3":
            song_name = input("Enter the name of the song: ")
            search_and_download_mp3chief(song_name)
        elif choice == "4":
            print("Exiting TempoTrove. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
