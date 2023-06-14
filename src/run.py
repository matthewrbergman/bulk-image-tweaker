import os
import shutil

import helper

from PIL import Image


# Directories
ROOT = os.getcwd()
ROOT_INPUT_FOLDER = os.path.join(ROOT, "input")
ROOT_OUTPUT_FOLDER = os.path.join(ROOT, "output")
ROOT_ERROR_FOLDER = os.path.join(ROOT, "error")

FILE_TYPE = ".webp"
MAX_WIDTH = 1260
REMOVE_EXIF = False
FLIP_HORIZONTALLY = False


# Image Enhancements
BRIGHTNESS = 1.00
CONTRAST = 1.05
SHARPNESS = 1.25
COLOR = 1.30


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

		if helper.IsImage(image):
			try:
				# Open
				img = Image.open(file_input_path)

				# Resize
				img = helper.ResizeImageWithRatio(img, MAX_WIDTH)

				# Strip EXIF Data
				if REMOVE_EXIF:
					img = helper.RemoveEXIF(img)

				# Enhance
				img = helper.EnhanceImage(BRIGHTNESS, CONTRAST, SHARPNESS, COLOR)

				# Flip?
				if FLIP_HORIZONTALLY:
					img = img.transpose(Image.FLIP_LEFT_RIGHT)

				# Save
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