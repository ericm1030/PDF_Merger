# from tkinter import font
# import tkinter
# root = tkinter.Tk()
# fonts = list(font.families())
# print(f"Fonts: {fonts}")
# fonts.sort()
# root.destroy()
import base64
import io
from PIL import Image

data = 0
with open('pdf.ico', 'rb') as f:
    data = base64.b64encode(f.read())
    print(data)

stream = io.BytesIO(data)
img = Image.open(stream)
img.show()