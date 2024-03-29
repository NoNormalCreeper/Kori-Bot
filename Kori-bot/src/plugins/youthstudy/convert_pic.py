from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
from os.path import dirname

font_path = f'{dirname(__file__)}/resource/font/font.otf'
bold_path = f'{dirname(__file__)}/resource/font/font-bold.otf'
icon_path = f'{dirname(__file__)}/resource/bac/bac.png'


def size(size: int) -> ImageFont:
    return ImageFont.truetype(font_path, size)

def bold(size: int) -> ImageFont:
    return ImageFont.truetype(bold_path, size)


async def convert_pic(text):
    img = Image.new('RGB', (902, 987), (255, 255, 255))
    icon = Image.open(icon_path)
    img.paste(icon, (0, 0))
    draw = ImageDraw.Draw(img)
    title = "".join(f"{i}\n" for i in text["title"])
    period = "".join(f"{i}\n" for i in text["period"])
    draw.multiline_text((10, 10), title, fill='gold', font=size(55))
    draw.multiline_text((100, 80), period, fill='gold', font=size(50))
    for j, i in enumerate(text["answer"]):
        draw.multiline_text((200 + j * 150, 40 if j == 0 else 90), i, fill='gold', font=bold(40))
    draw.multiline_text((200, 700), text["end_time"], fill='gold', font=bold(40))
    buf = BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return f"base64://{base64_str}"
