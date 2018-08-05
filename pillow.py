from PIL import Image, ImageFont, ImageDraw
from time import sleep

im = Image.new('RGB', (200,200), (255,0,0))
dr = ImageDraw.Draw(im)


for i in range(0, 130, 10):
    dr.rectangle(((i,i),(i+10,i+10)), fill="black", outline = "blue")
    sleep(1)
    im.show()