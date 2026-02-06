from PIL import Image, ImageDraw, ImageFont
import os

def create_app_icon(target_path="app_icon.ico"):
    # Create valid size for ICO
    size = (256, 256)
    color_bg = "#2C3E50" # Dark Slate
    color_text = "#18BC9C" # Teal
    
    img = Image.new('RGB', size, color=color_bg)
    d = ImageDraw.Draw(img)
    
    # Draw simple "B" or chart symbol
    # Since we can't easily load custom fonts without knowing path, we'll draw shapes.
    
    # Draw a border
    d.rectangle([10, 10, 246, 246], outline=color_text, width=10)
    
    # Draw a bar chart symbol
    # Bar 1 (Left)
    d.rectangle([50, 100, 90, 200], fill=color_text)
    # Bar 2 (Center - taller)
    d.rectangle([110, 60, 150, 200], fill=color_text)
    # Bar 3 (Right)
    d.rectangle([170, 120, 210, 200], fill=color_text)
    
    img.save(target_path, format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    print(f"Icon created at {os.path.abspath(target_path)}")

if __name__ == "__main__":
    create_app_icon()
