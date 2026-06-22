from flask import Flask, request, render_template_string, make_response, jsonify, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import io
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Создаем папку для хранения изображений
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# HTML для формы создания изображения
FORM_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Генератор изображений</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .error { color: red; }
        input { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Создание изображения</h1>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    <form method="POST" enctype="application/x-www-form-urlencoded">
        <label>Ширина (10-2000): <input type="number" name="width" required></label><br>
        <label>Высота (10-2000): <input type="number" name="height" required></label><br>
        <label>Текст: <input type="text" name="text" required></label><br>
        <button type="submit">Создать</button>
    </form>
    <br>
    <a href="/images">Посмотреть все изображения</a>
</body>
</html>
'''

# HTML для загрузки изображения
UPLOAD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Загрузка изображения</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .error { color: red; }
        .success { color: green; }
        form { margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Загрузка изображения</h1>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    {% if success %}
        <p class="success">{{ success }}</p>
    {% endif %}
    <form method="POST" enctype="multipart/form-data">
        <label>Название изображения: <input type="text" name="image_name" value="{{ filename }}"></label><br>
        <label>Выберите изображение: <input type="file" name="image_file" accept="image/*" required></label><br>
        <button type="submit">Загрузить</button>
    </form>
    <br>
    <a href="/images">Посмотреть все изображения</a>
</body>
</html>
'''

# HTML для галереи изображений
GALLERY_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Галерея изображений</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .image-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            text-align: center;
        }
        .image-card img {
            max-width: 100%;
            height: auto;
            border-radius: 4px;
        }
        .image-name {
            margin-top: 10px;
            font-weight: bold;
        }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
        .nav { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Галерея изображений</h1>
    <div class="nav">
        <a href="/makeimage">Создать изображение</a> |
        <a href="/load_image">Загрузить изображение</a>
    </div>
    
    {% if images %}
        <div class="gallery">
            {% for image in images %}
                <div class="image-card">
                    <img src="{{ url_for('static', filename='images/' + image) }}" alt="{{ image }}">
                    <div class="image-name">{{ image }}</div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <p>Нет загруженных изображений.</p>
    {% endif %}
</body>
</html>
'''

@app.route('/login', methods=['GET'])
def login():
    return jsonify({"author": "1154212"})

@app.route('/makeimage', methods=['GET', 'POST'])
def makeimage():
    if request.method == 'GET':
        return render_template_string(FORM_HTML, error=None)
    
    try:
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        text = request.form.get('text', '').strip()
        
        if width < 10 or width > 2000 or height < 10 or height > 2000:
            raise ValueError("Invalid image size")
        if width <= 0 or height <= 0:
            raise ValueError("Invalid image size")
            
    except (TypeError, ValueError):
        return render_template_string(FORM_HTML, error="Invalid image size"), 400
    
    img = Image.new('RGB', (width, height), color=(230, 230, 230))
    draw = ImageDraw.Draw(img)
    
    # Пытаемся использовать шрифт, если файл существует
    try:
        font_size = max(20, min(width, height) // 10)
        font = ImageFont.truetype("ofont.ru_Ekaterina Velikaya Two.ttf", font_size)
    except:
        # Используем шрифт по умолчанию
        font = ImageFont.load_default()
        font_size = 20
    
    # Рисуем текст
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        # Для старых версий PIL
        text_width, text_height = draw.textsize(text, font=font)
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)
    
    # Сохраняем изображение в галерею
    filename = f"generated_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    img.save(filepath, 'JPEG', quality=90)
    
    # Возвращаем изображение
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    
    response = make_response(img_io.getvalue())
    response.headers.set('Content-Type', 'image/jpeg')
    return response

@app.route('/load_image', methods=['GET', 'POST'])
def load_image():
    if request.method == 'GET':
        return render_template_string(UPLOAD_HTML, error=None, success=None, filename='')
    
    # POST метод - загрузка изображения
    try:
        # Получаем название изображения
        image_name = request.form.get('image_name', '').strip()
        image_file = request.files.get('image_file')
        
        if not image_file or image_file.filename == '':
            return render_template_string(UPLOAD_HTML, 
                                        error="Пожалуйста, выберите изображение", 
                                        success=None, 
                                        filename=image_name)
        
        # Если название пустое, используем имя файла
        if not image_name:
            image_name = os.path.splitext(image_file.filename)[0]
        
        # Безопасное имя файла
        safe_name = secure_filename(image_name)
        if not safe_name:
            safe_name = f"image_{uuid.uuid4().hex[:8]}"
        
        # Проверяем расширение
        ext = os.path.splitext(image_file.filename)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return render_template_string(UPLOAD_HTML, 
                                        error="Поддерживаются только изображения (jpg, png, gif, bmp)", 
                                        success=None, 
                                        filename=image_name)
        
        # Формируем имя файла с расширением
        filename = f"{safe_name}{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Проверяем, существует ли файл
        if os.path.exists(filepath):
            return render_template_string(UPLOAD_HTML, 
                                        error=f"Изображение с именем '{image_name}' уже существует", 
                                        success=None, 
                                        filename=image_name)
        
        # Сохраняем файл
        image_file.save(filepath)
        
        return render_template_string(UPLOAD_HTML, 
                                    error=None, 
                                    success=f"Изображение '{image_name}' успешно загружено", 
                                    filename='')
        
    except Exception as e:
        return render_template_string(UPLOAD_HTML, 
                                    error=f"Ошибка при загрузке: {str(e)}", 
                                    success=None, 
                                    filename=request.form.get('image_name', ''))

@app.route('/images', methods=['GET'])
def show_images():
    # Получаем все изображения из папки
    images = []
    try:
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                images.append(file)
        images.sort()  # Сортируем по имени
    except:
        images = []
    
    return render_template_string(GALLERY_HTML, images=images)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)