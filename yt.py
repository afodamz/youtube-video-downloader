from pytube import YouTube
from datetime import datetime
import sys
import ssl
import pyttsx3
import os
import argparse

ssl._create_default_https_context = ssl._create_stdlib_context

parser = argparse.ArgumentParser()
max_threads = 5
download_folder_path = "Downloads"


def say(msg="Great! Finally finished, please check the result!", voice="Victoria"):
    if os.name == 'nt':
        engine = pyttsx3.init()
        engine.say(f'{msg}')
        engine.runAndWait()
    else:
        os.system(f'say -- {msg}')

def create_folder():
    if not os.path.exists(download_folder_path):
        os.makedirs(download_folder_path)


download_start_time = datetime.now()


def downloadCallback(stream, chunk, bytes_remaining):
    global download_start_time
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    current = bytes_downloaded / total_size
    percentage_of_completion = bytes_downloaded / total_size * 100

    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percentage_of_completion))
    sys.stdout.flush()


def download(link):
    yt = YouTube(link)
    video = yt.streams.filter(progressive=True).last()
    yt.register_on_progress_callback(downloadCallback)
    print(f"Fetching \"{video.title}\"..")
    print(f"Fetching successful\n")
    print(f"Information: \n"
          f"File size: {round(video.filesize * 0.000001, 2)} MegaBytes\n"
          f"Highest Resolution: {video.resolution}\n"
          f"Author: {yt.author}")

    print(f"Downloading \"{video.title}\"..")

    try:
        video.download(output_path=download_folder_path)
    except:
        print("An error has occurred")
    print("Download is completed successfully")


if __name__ == "__main__":
    parser.add_argument('--links', nargs='+')
    parser.add_argument('--link', nargs='+')
    parser.add_argument('--file', help="please enter file name")
    args = parser.parse_args()

    create_folder()

    if args.links:
        for index, link in enumerate(args.links):
            download(link)
            say(msg=f"Done downloading {int(index) + 1} out of {len(args.links)}")
    elif args.link:
        download(args.link)
        say()
    if args.file:
        with open(args.file) as file:
            contents = file.readlines()
            for index, link in enumerate(contents):
                download(link)
                say(msg=f"Done downloading {int(index) + 1} out of {len(contents)}")
    else:
        link = input("Enter the YouTube video URL: ")
        while link is not 'q' or link is not 'quit':
            download(link)
            say()
            link = input("Enter the YouTube video URL: ")

