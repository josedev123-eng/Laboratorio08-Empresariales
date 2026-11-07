"""Trim the empty white space at the bottom of the API screenshots."""
import os
from PIL import Image, ImageOps

CARPETA = os.path.join("docs", "capturas")

for name in sorted(os.listdir(CARPETA)):
    if not name.lower().endswith(".png"):
        continue
    path = os.path.join(CARPETA, name)
    img = Image.open(path).convert("RGB")
    width, height = img.size

    # Mask of "ink" pixels, ignoring the near-white background.
    gray = img.convert("L")
    mask = gray.point(lambda p: 0 if p < 245 else 255)
    bbox = ImageOps.invert(mask).getbbox()

    last = bbox[3] if bbox else height
    new_height = min(height, last + 24)
    if new_height < height:
        img.crop((0, 0, width, new_height)).save(path)
    print(f"{name}: {height} -> {new_height}px")
