import cv2
import numpy as np
import subprocess

def find_undo_button(image):
    # Load the image and template
    #image = cv2.imread(image_path)
    template_path = 'undotemplete.png'
    template = cv2.imread(template_path)

    # Convert both images to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Perform template matching
    result = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)

    # Find the location of the template in the image
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    height, width = gray_template.shape[::-1]
    bottom_right = (top_left[0] + width, top_left[1] + height)

    return top_left, bottom_right

def click_coordinates(x, y):

    # Format the ADB command to click the coordinates
    command = f"adb shell input tap {x} {y}"
    print("used undo")
    # Run the ADB command
    subprocess.run(command, shell=True)

# click_coordinates(1,2)    