from PIL import Image, ImageDraw

img = Image.new("RGBA", (96, 96), (0,0,0,0))
draw = ImageDraw.Draw(img)
# Draw Spotify green circle
draw.ellipse([8, 8, 88, 88], fill="#1DB954")

# Draw 3 black curves (arcs)
draw.arc([24, 30, 72, 70], start=210, end=330, fill="black", width=6)
draw.arc([28, 45, 68, 75], start=215, end=325, fill="black", width=5)
draw.arc([32, 58, 64, 82], start=220, end=320, fill="black", width=4)

img.save("icons_apps/Spotify.png")
print("Spotify icon drawn.")
