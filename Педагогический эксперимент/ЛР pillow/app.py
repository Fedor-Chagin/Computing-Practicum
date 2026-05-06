from flask import Flask, request, render_template_string, make_response, jsonify
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

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
    
    font_size = max(20, min(width, height) // 10)
    font = ImageFont.truetype("ofont.ru_Ekaterina Velikaya Two.ttf", font_size)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    position = ((width - text_width) // 2, (height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)
    
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=90)
    img_io.seek(0)
    
    response = make_response(img_io.getvalue())
    response.headers.set('Content-Type', 'image/jpeg')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)


# cd /Users/fedorcagin/Desktop/pillow
# python3 -m venv venv
# source venv/bin/activate
# python app.py

# http://127.0.0.1:5000/makeimage
# http://127.0.0.1:5000/login