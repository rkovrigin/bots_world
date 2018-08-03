from PIL import Image, ImageFont, ImageDraw

im = Image.new('RGB', (200,200), (255,0,0))
dr = ImageDraw.Draw(im)

dr.rectangle(((150,150),(160,160)), fill="black", outline = "blue")

im.save("rectangle.png")