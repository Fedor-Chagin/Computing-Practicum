const express = require('express');
const multer = require('multer');
const sizeOf = require('image-size');
const fs = require('fs');
const path = require('path');
const app = express();

// Создаём папки, если их нет
if (!fs.existsSync('uploads')) {
    fs.mkdirSync('uploads');
}
if (!fs.existsSync('public')) {
    fs.mkdirSync('public');
}

// Хранилище состояния последнего изображения
let lastImageState = null;

// Настройка multer для сохранения файлов с нормализацией имён
const storage = multer.diskStorage({
    destination: 'uploads/',
    filename: (req, file, cb) => {
        // Получаем оригинальное имя и заменяем все проблемные символы
        let originalName = file.originalname;
        // Убираем расширение .png
        const baseName = originalName.replace(/\.png$/i, '');
        // Заменяем все символы, кроме букв, цифр, точки и дефиса, на подчёркивание
        const safeName = baseName.replace(/[^a-zA-Z0-9а-яА-Я.-]/g, '_');
        cb(null, Date.now() + '_' + safeName + '.png');
    }
});

const upload = multer({ storage: storage });

// Раздача статических файлов
app.use(express.static('public'));
app.use('/uploads', express.static('uploads'));

// Маршрут /login
app.get('/login', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.json({ author: "25565" });
});

// Маршрут для получения последнего состояния
app.get('/last-image', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    if (lastImageState) {
        res.json(lastImageState);
    } else {
        res.json({});
    }
});

// Маршрут для отдачи React-фронтэнда
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Основной маршрут /size2json
app.post('/size2json', upload.single('image'), (req, res) => {
    res.setHeader('Content-Type', 'application/json');

    console.log('=== New request ===');
    console.log('File received:', req.file ? req.file.filename : 'No file');
    console.log('MIME type:', req.file ? req.file.mimetype : 'No');

    if (!req.file) {
        return res.json({ result: "invalid filetype" });
    }

    const isPng = req.file.mimetype === 'image/png' || req.file.originalname.toLowerCase().endsWith('.png');

    if (!isPng) {
        console.log('Not a PNG file');
        if (fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path);
        }
        return res.json({ result: "invalid filetype" });
    }

    try {
        const imageBuffer = fs.readFileSync(req.file.path);
        const dimensions = sizeOf(imageBuffer);
        console.log('Dimensions:', dimensions.width, 'x', dimensions.height);

        lastImageState = {
        width: dimensions.width,
        height: dimensions.height,
        thumbnail: `/uploads/${req.file.filename}`,
        filename: Buffer.from(req.file.originalname, 'latin1').toString('utf8'),
        timestamp: Date.now()
        };

        res.json({ width: dimensions.width, height: dimensions.height });

    } catch (err) {
        console.error('Processing error:', err.message);
        if (req.file && fs.existsSync(req.file.path)) {
            fs.unlinkSync(req.file.path);
        }
        res.json({ result: "error processing image" });
    }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Local: http://localhost:${PORT}`);
    console.log(`Production: https://lr4.fedorchagin.ru`);
});
