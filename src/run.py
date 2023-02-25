import math
import os
import shutil

from PIL import Image, ImageEnhance


# Directories
ROOT = os.getcwd()
ROOT_INPUT_FOLDER = os.path.join(ROOT, "input")
ROOT_OUTPUT_FOLDER = os.path.join(ROOT, "output")
ROOT_ERROR_FOLDER = os.path.join(ROOT, "error")

FILE_TYPE = ".webp"
MAX_WIDTH = 1260
FLIP_HORIZONTALLY = False
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".bmp", ".webp", ".png"]

# Image Enhancements
BRIGHTNESS = 1.00
CONTRAST = 1.05
SHARPNESS = 1.25
COLOR = 1.30


def IsImage(file):
	for extension in IMAGE_EXTENSIONS:
		if file.endswith(extension):
			return True
	
	return False


# Introduction
print("**************************************")
print("*** Bulk Image Tweaker ***************")
print("**************************************\n")

# Folder Loop
for folder in os.listdir(ROOT_INPUT_FOLDER):
	folder_input_path = os.path.join(ROOT_INPUT_FOLDER, folder)
	folder_output_path = os.path.join(ROOT_OUTPUT_FOLDER, folder)

	# Create Output Folders
	if not os.path.exists(folder_output_path):
		os.makedirs(folder_output_path)

	# File Loop
	for image in os.listdir(folder_input_path):
		file_input_path = os.path.join(folder_input_path, image)
		file_output_path = os.path.join(folder_output_path, image)
		file_error_path = os.path.join(ROOT_ERROR_FOLDER, image)

		if IsImage(image):
			try:
				# Open
				img = Image.open(file_input_path)

				
				data = list(img.getdata())
				img = Image.new('RGB', img.size) # not handling opacity
				img.putdata(data) # should strip exif


				# Resize
				w, h = img.size
				ratio = h / w
				new_h = math.floor(MAX_WIDTH * ratio)
				img = img.resize( (MAX_WIDTH, new_h) )

				# Enhance
				img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS)
				img = ImageEnhance.Contrast(img).enhance(CONTRAST)
				img = ImageEnhance.Sharpness(img).enhance(SHARPNESS)
				img = ImageEnhance.Color(img).enhance(COLOR)

				# Flip?
				if FLIP_HORIZONTALLY:
					img = img.transpose(Image.FLIP_LEFT_RIGHT)

				# Save TODO
				basename = os.path.splitext(image)[0]
				export_file_path = os.path.join(folder_output_path, basename + FILE_TYPE)
				img = img.save(export_file_path)


				print(" [*** SAVED] " + image)
			except Exception as e:
				shutil.move(file_input_path, file_error_path)
				print(" [!!! ERROR] " + image)
				print(e)
		else:
			# Move to output folder
			shutil.move(file_input_path, file_output_path)
			print(" [>>> MOVED] " + image)

# Conclusion
print("\n DONE.")