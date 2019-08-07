import pytesseract
import PIL.Image as Images

image = Images.open('C:\\Users\\hpqcp\\Picturestest.png')
code = pytesseract.image_to_string(image)
print(code)


