from PIL import Image, ImageDraw

width, height = 300, 100
image = Image.new('RGB', (width, height), color='white')

image.save('white_image.png')

print(f" Изображение размером {width}×{height} пикселей создано и сохранено как 'white_image.png'")