from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)

API_KEY = 'AIzaSyBJy4DH7F7EitQdj0B8JhUeVQCCjTz03Ls'
youtube = build('youtube', 'v3', developerKey=API_KEY)

def buscar_videos_virais_cc(palavra_chave, max_resultados=20):
    resultado = youtube.search().list(
        q=palavra_chave,
        part='snippet',
        type='video',
        videoLicense='creativeCommon',
        order='viewCount',
        maxResults=max_resultados
    ).execute()

    videos = []
    for item in resultado['items']:
        video_id = item['id']['videoId']
        titulo = item['snippet']['title']
        link = f'https://www.youtube.com/watch?v={video_id}'
        videos.append({'titulo': titulo, 'link': link})
    
    return videos

@app.route('/', methods=['GET', 'POST'])
def index():
    videos = []
    palavra_chave = ''
    if request.method == 'POST':
        palavra_chave = request.form.get('palavra_chave', '')
        if palavra_chave.strip():
            videos = buscar_videos_virais_cc(palavra_chave, max_resultados=20)
    return render_template('index.html', videos=videos, palavra_chave=palavra_chave)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # pega a porta usada no Railway
    app.run(host='0.0.0.0', port=port)
