from PIL import Image


def is_color_image(image_path):
    try:
        # Открываем изображение с помощью Pillow
        img = Image.open(image_path)

        # Получаем структуру пикселей
        pixels = img.getdata()

        # Проходим по всем пикселям и проверяем, есть ли различия в цвете
        for pixel in pixels:
            r, g, b = pixel[:3]
            print(abs(r - g),abs(g - b))
            if abs(r - g) > 20 or abs(g - b) > 20:
                return True

        # Если все пиксели имеют одинаковый цвет, то изображение черно-белое
        return False
    except Exception as e:
        # Если произошла ошибка при открытии изображения, считаем его некорректным
        return False

# Путь к изображению
image_path = 'img.png'

# Проверяем, является ли изображение цветным
if is_color_image(image_path):
    print('Изображение является цветным.')
else:
    print('Изображение является черно-белым или некорректным.')
