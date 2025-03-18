import time
from PIL import Image, ImageDraw, ImageFont
import os

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
width, height = 1280, 720  # Matches hdmi_mode=4
base_img = Image.new('RGB', (width, height), color='black')
last_date = ""
last_time = ""
use_first = True

while True:
    current_date = time.strftime("%a, %B %d")  # e.g., "Mon, March 17"
    current_time = time.strftime("%H:%M")      # e.g., "14:35"

    if current_date != last_date or current_time != last_time:
        img = base_img.copy()
        draw = ImageDraw.Draw(img)
        date_font = ImageFont.truetype(font_path, 120)  # 2x original 60
        time_font = ImageFont.truetype(font_path, 240)  # 2x original 120
        
        date_bbox = draw.textbbox((0, 0), current_date, font=date_font)
        time_bbox = draw.textbbox((0, 0), current_time, font=time_font)
        date_pos = (width // 2 - (date_bbox[2] - date_bbox[0]) // 2, height // 2 - 150)
        time_pos = (width // 2 - (time_bbox[2] - time_bbox[0]) // 2, height // 2 + 75)
        
        draw.text(date_pos, current_date, font=date_font, fill='white')
        draw.text(time_pos, current_time, font=time_font, fill='white')
        
        filename = 'clock1.png' if use_first else 'clock2.png'
        img.save(filename)
        os.system(f'sudo killall fbi; sudo timeout 0.5 fbi -T 1 -noverbose -a {filename} > /dev/null 2>&1 &')
        use_first = not use_first
        last_date = current_date
        last_time = current_time
        print(f"Updated: {filename}")

    time.sleep(60)  # Update every minute
