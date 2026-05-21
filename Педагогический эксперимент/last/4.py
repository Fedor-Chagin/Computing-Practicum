from flask import Flask, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route('/image')
def get_image():
    # Создаём изображение 300×100 с белым фоном
    width, height = 300, 100
    image = Image.new('RGB', (width, height), color='white')
    
    # Сохраняем в память
    img_io = io.BytesIO()
    image.save(img_io, format='PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

# Добавим маршрут для проверки
@app.route('/')
def home():
    return "Flask работает! Перейдите на /image"

if __name__ == '__main__':
    # ВАЖНО: host='0.0.0.0' - чтобы принимать запросы извне контейнера
    app.run(debug=True, host='0.0.0.0', port=5000)