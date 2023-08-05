import base64, re, os
from PIL import Image
from io import BytesIO

def saveToBmp(fileIn,fileOut,width=None,fmt="BMP",base64Input=False):
    if (type(fileIn) == str and fileIn.startswith("data:image")) or base64Input:
        b64 = re.sub('^data:image/.+;base64,', '', fileIn)
        image_data = base64.b64decode(b64)
        img = Image.open(BytesIO(image_data))
    else:    
        img = Image.open(fileIn)


    w, h = img.size
    if h > 128 or w > 160 or fmt.upper() == 'BMP':
        img = img.convert("RGB")

    if not width:
        width = w

    if h>128:
        hpercent = (128/h)
        w = int(w*hpercent)
        h = int(h*hpercent)
    width = w
    width = int(width/8)*8 #align to 8pix
    if width == 0:
        width = 8
    if width > 160:
        width = 160
    wpercent = (width/float(w))
    hsize = int((float(h)*float(wpercent)))
       
    img = img.resize((width,hsize))
    img.save(fileOut, fmt.upper())

if __name__ == "__main__":
    saveToBmp('test.jpg', 'test1.bmp')
    data = open('test.jpg', "rb").read()
    encoded = base64.b64encode(data)
    saveToBmp("data:image/jpeg;base64,"+encoded.decode(), 'test2.bmp')

