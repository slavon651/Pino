from flask import Flask, render_template, request, jsonify, send_file
import requests
import re
import os
from urllib.parse import urlparse
import tempfile
import json
from datetime import datetime

app = Flask(__name__)

# Конфигурация
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
TEMP_DIR = tempfile.gettempdir()

def extract_video_url(pinterest_url):
    """
    Извлекает прямую ссылку на видео из Pinterest URL
    """
    try:
        # Очищаем URL
        pinterest_url = pinterest_url.strip()
        
        # Проверяем что это Pinterest URL
        if 'pinterest' not in pinterest_url.lower():
            return None, "Invalid Pinterest URL"
        
        # Получаем HTML страницы
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.pinterest.com/',
        }
        
        response = requests.get(pinterest_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        html = response.text
        
        # Ищем JSON данные в HTML
        # Pinterest хранит данные в __PWS_DATA__
        patterns = [
            r'"video_list":\s*{[^}]*"V_720P":\s*{[^}]*"url":\s*"([^"]+)"',
            r'"video_list":\s*{[^}]*"V_HLSV4":\s*{[^}]*"url":\s*"([^"]+)"',
            r'"videos":\s*{[^}]*"video_list":\s*{[^}]*"V_720P":\s*{[^}]*"url":\s*"([^"]+)"',
            r'<video[^>]*src="([^"]+)"',
            r'"url":\s*"(https://[^"]*\.mp4[^"]*)"',
        ]
        
        video_url = None
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                video_url = matches[0]
                # Декодируем escaped символы
                video_url = video_url.replace('\\u002F', '/')
                break
        
        if not video_url:
            # Альтернативный метод - поиск через API
            pin_id_match = re.search(r'/pin/(\d+)', pinterest_url)
            if pin_id_match:
                pin_id = pin_id_match.group(1)
                api_url = f'https://www.pinterest.com/resource/PinResource/get/?source_url=/pin/{pin_id}/&data={{"options":{{"field_set_key":"detailed","id":"{pin_id}"}},"context":{{}}}}&_={datetime.now().timestamp()}'
                
                api_response = requests.get(api_url, headers=headers, timeout=30)
                if api_response.status_code == 200:
                    data = api_response.json()
                    try:
                        video_data = data['resource_response']['data']['videos']['video_list']
                        if 'V_720P' in video_data:
                            video_url = video_data['V_720P']['url']
                        elif 'V_HLSV4' in video_data:
                            video_url = video_data['V_HLSV4']['url']
                    except (KeyError, TypeError):
                        pass
        
        if not video_url:
            return None, "Video not found. This might be an image pin or private content."
        
        return video_url, None
        
    except requests.RequestException as e:
        return None, f"Network error: {str(e)}"
    except Exception as e:
        return None, f"Error: {str(e)}"

def download_video(video_url):
    """
    Скачивает видео и возвращает путь к временному файлу
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(video_url, headers=headers, stream=True, timeout=60)
        response.raise_for_status()
        
        # Создаем временный файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4', dir=TEMP_DIR)
        
        # Скачиваем видео по частям
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                temp_file.write(chunk)
        
        temp_file.close()
        return temp_file.name, None
        
    except Exception as e:
        return None, f"Download error: {str(e)}"

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def api_download():
    """API endpoint для скачивания видео"""
    try:
        data = request.get_json()
        pinterest_url = data.get('url', '').strip()
        
        if not pinterest_url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Извлекаем URL видео
        video_url, error = extract_video_url(pinterest_url)
        if error:
            return jsonify({'error': error}), 400
        
        # Возвращаем прямую ссылку на видео
        return jsonify({
            'success': True,
            'video_url': video_url,
            'message': 'Video found successfully!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/info', methods=['POST'])
def api_info():
    """Получение информации о видео"""
    try:
        data = request.get_json()
        pinterest_url = data.get('url', '').strip()
        
        if not pinterest_url:
            return jsonify({'error': 'URL is required'}), 400
        
        video_url, error = extract_video_url(pinterest_url)
        if error:
            return jsonify({'error': error}), 400
        
        # Получаем размер видео
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.head(video_url, headers=headers, timeout=10)
            file_size = int(response.headers.get('content-length', 0))
            file_size_mb = round(file_size / (1024 * 1024), 2)
        except:
            file_size_mb = 'Unknown'
        
        return jsonify({
            'success': True,
            'video_url': video_url,
            'file_size_mb': file_size_mb
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Создаем папку для шаблонов если её нет
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Запускаем сервер
    app.run(host='0.0.0.0', port=5000, debug=True)
