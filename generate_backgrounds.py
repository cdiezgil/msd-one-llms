from PIL import Image, ImageDraw, ImageFont
import os

W, H = 854, 480

# 1. Solid Black Image
img_black = Image.new('RGB', (W, H), color='black')
img_black.save('black_background.jpg', quality=95)

# 2. cdiezgil Brand Image
img_brand = Image.new('RGB', (W, H), color='#0A1122')
draw = ImageDraw.Draw(img_brand)

# Add a subtle dot grid texture (Engineering vibe)
# The lateral screen is approximately the rightmost 144 pixels.
# Let's draw dots everywhere just in case
for x in range(0, W, 20):
    for y in range(0, H, 20):
        draw.rectangle([x, y, x+1, y+1], fill='#1A2235')

# We want to place the logo on the right side (lateral screen)
# The lateral screen is around x=690 to 854. Let's center it at x=770.
# Logo: { cdiezgil }
try:
    font_brackets = ImageFont.truetype("Arial.ttf", 44)
    font_name = ImageFont.truetype("Arial Bold.ttf", 44)
except:
    font_brackets = ImageFont.load_default()
    font_name = ImageFont.load_default()

bracket_left = "{ "
name = "cdiezgil"
bracket_right = " }"

# Create a transparent image to draw the text, then rotate it
# Estimate width:
text_img = Image.new('RGBA', (800, 100), (0,0,0,0))
text_draw = ImageDraw.Draw(text_img)

b_left_bbox = text_draw.textbbox((0, 0), bracket_left, font=font_brackets)
b_left_w = b_left_bbox[2] - b_left_bbox[0]

name_bbox = text_draw.textbbox((0, 0), name, font=font_name)
name_w = name_bbox[2] - name_bbox[0]

b_right_bbox = text_draw.textbbox((0, 0), bracket_right, font=font_brackets)
b_right_w = b_right_bbox[2] - b_right_bbox[0]

total_w = b_left_w + name_w + b_right_w
total_h = name_bbox[3] - name_bbox[1]

# Draw the text on the transparent image
text_draw.text((0, 0), bracket_left, fill='#FFD700', font=font_brackets)
text_draw.text((b_left_w, 0), name, fill='#FFFFFF', font=font_name)
text_draw.text((b_left_w + name_w, 0), bracket_right, fill='#FFD700', font=font_brackets)

# Crop the text image tightly
text_img = text_img.crop((0, 0, total_w, total_h + 20))

# Rotate "a la derecha" (clockwise 90 degrees) -> in PIL rotate(angle) is counter-clockwise, so -90 is clockwise.
text_rotated = text_img.rotate(-90, expand=True)

# Paste it into the main image
# Center it in the sidebar area (approx x=690 to 854)
sidebar_center_x = 810
sidebar_center_y = H // 2

paste_x = sidebar_center_x - (text_rotated.width // 2)
paste_y = sidebar_center_y - (text_rotated.height // 2)

img_brand.paste(text_rotated, (paste_x, paste_y), text_rotated)

img_brand.save('cdiezgil_background.jpg', quality=95)

print("Images regenerated at 854x480.")
