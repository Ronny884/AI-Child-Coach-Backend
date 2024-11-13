from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup

# # Вставьте URL видео с YouTube
# video_url = 'https://www.youtube.com/watch?v=rL8u4Y6holg'


def get_transcript(video_url):
    response = requests.get(video_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Извлечение названия видео
    video_title = soup.find('title').text

    # Определение языка субтитров
    if any(char in video_title for char in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'):
        language = 'ru'
    else:
        language = 'en'

    # Извлечение ID видео
    video_id = video_url.split('v=')[1]

    # Получение субтитров
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

    # Вывод субтитров
    for entry in transcript:
       return f"{entry['start']} - {entry['duration']}: {entry['text']}"