import math

from PIL import Image, ImageEnhance

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".bmp", ".webp", ".png"]

def IsImage(file):
	for extension in IMAGE_EXTENSIONS:
		if file.endswith(extension):
			return True
	
	return False

def ResizeImageWithRatio(img, max_width):
    w, h = img.size
    ratio = h / w
    new_h = math.floor(max_width * ratio)
    img = img.resize( (max_width, new_h) )

    return img

def EnhanceImage(brightness, contrast, sharpness, color):
	img = ImageEnhance.Brightness(img).enhance(brightness)
	img = ImageEnhance.Contrast(img).enhance(contrast)
	img = ImageEnhance.Sharpness(img).enhance(sharpness)
	img = ImageEnhance.Color(img).enhance(color)
	
	return img

def StripEXIF(img):
	img_data = list(img.getdata())
	img = Image.new('RGB', img.size)
	img.putdata(img_data)
	
	return img