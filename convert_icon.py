from PIL import Image
import sys

def convert_to_ico(source, target):
    img = Image.open(source)
    img.save(target, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])

if __name__ == "__main__":
    convert_to_ico("business_analytics_icon.png", "app_icon.ico")
