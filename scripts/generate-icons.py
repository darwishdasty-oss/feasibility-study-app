from PIL import Image, ImageDraw
import os

os.makedirs('/home/z/my-project/public/icons', exist_ok=True)

def make_icon(size, path):
    img = Image.new('RGBA', (size, size), (13, 148, 136, 255))
    draw = ImageDraw.Draw(img)
    margin = size // 6
    bar_w = (size - 2 * margin) // 5
    heights = [0.4, 0.65, 0.85, 0.55, 1.0]
    for i, h in enumerate(heights):
        x = margin + i * bar_w
        y_top = int(size * (1 - h * 0.7) - margin/2)
        y_bot = size - margin
        color = (255, 255, 255, 255) if i < 4 else (250, 204, 21, 255)
        draw.rectangle([x, y_top, x + bar_w - 4, y_bot], fill=color)
    img.save(path)

make_icon(192, '/home/z/my-project/public/icons/icon-192.png')
make_icon(512, '/home/z/my-project/public/icons/icon-512.png')
print("Icons generated")
