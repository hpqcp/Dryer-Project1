import pytesseract
from PIL import Image

image = Image.open('C:\\Users\\hpqcp\\Picturestest.png')
code = pytesseract.image_to_string(image)
print(code)


