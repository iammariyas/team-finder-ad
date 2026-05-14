import io
import random
import uuid

from django.core.files import File
from PIL import Image, ImageDraw, ImageFont

_FONTS = (
    'C:/Windows/Fonts/arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
)


def generate_avatar(user):
    letter = (user.name or user.email or '?')[0].upper()
    bg = random.choice(('#d4e5f7', '#e8d4f5', '#d4f5e3', '#e0e8f0', '#dde8e4'))
    size = 200
    img = Image.new('RGB', (size, size), bg)
    draw = ImageDraw.Draw(img)
    font = None
    for path in _FONTS:
        try:
            font = ImageFont.truetype(path, 96)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    if hasattr(draw, 'textbbox'):
        bbox = draw.textbbox((0, 0), letter, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    else:
        tw, th = draw.textsize(letter, font=font)
    draw.text(((size - tw) / 2, (size - th) / 2), letter, fill='#2a2a2a', font=font)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return File(buf, name=f'avatar_{uuid.uuid4().hex}.png')
