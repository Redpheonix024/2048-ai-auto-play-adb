import subprocess
import cv2 as cv
import numpy as np
import undobottonhandle
import time
import divimage
import manager
import matplotlib.pyplot as plt
from PIL import Image

def get_letter(num):
    mapping = {
        0: 'u',
        1: 'd',
        2: 'l',
        3: 'r'
    }
    return mapping.get(num, 'Invalid input')

def find_middle_coordinates(top_left, bottom_right):
    top_left_x, top_left_y = top_left
    bottom_right_x, bottom_right_y = bottom_right

    middle_x = (top_left_x + bottom_right_x) // 2
    middle_y = (top_left_y + bottom_right_y) // 2

    return middle_x, middle_y

same_array_count = 0
previous_array = None

# Start ADB server
subprocess.run(['adb', 'start-server'])

# Connect to ADB client
devices_output = subprocess.check_output(['adb', 'devices']).decode('utf-8')
devices = devices_output.strip().split('\n')[1:]  # Remove header and split into lines

if not devices:
    print("No devices found")
    exit()

print("Connected devices:")
for device_line in devices:
    print(device_line)

device = devices[0].split('\t')[0]
total_moves = 0
moves = 0
runs = int(input("Enter initial runs number (preferably in the range of 100 to 1000): "))

#Check for undo button coordinates
undo_button_coords = None
while undo_button_coords is None:
    try:
        image = subprocess.check_output(['adb', '-s', device, 'exec-out', 'screencap', '-p'])
        img = cv.imdecode(np.frombuffer(image, np.uint8), cv.IMREAD_COLOR)
        undo_button_coords = undobottonhandle.find_undo_button(img)
        if undo_button_coords:
            print("Undo button found at", undo_button_coords)
            undo_button_x, undo_button_y = undo_button_coords
            middle_x, middle_y = find_middle_coordinates(undo_button_x,undo_button_y)
        else:
            print("Undo button not found")

    except cv.error as e:
        print("Error processing image with OpenCV:", e)
        time.sleep(1)

try:
    while True:
        try:
            max_retries = 3
            retries = 0
            image = None

            while retries < max_retries:
                try:
                    image = subprocess.check_output(['adb', '-s', device, 'exec-out', 'screencap', '-p'])
                    img = cv.imdecode(np.frombuffer(image, np.uint8), cv.IMREAD_COLOR)
                    image = cv.resize(img, (400, 900))
                    img = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                    # plt.imshow(img)
                    # plt.axis('off')  # Turn off the axis labels
                    # plt.show()
                    screen_height, screen_width, _ = img.shape
                    crop_top = int(screen_height * 295 / 2400)
                    crop_bottom = int(screen_height * 690 / 2400)
                    crop_left = int(screen_width * 15 / 1080)
                    crop_right = int(screen_width * 390 / 1080)
                    crimage = img[295:690, 15:390]
                    # plt.imshow(img)
                    # plt.axis('off')  # Turn off the axis labels
                    # plt.show()  # Adjust the cropping region according to your screen resolution
                    break  #image = cv.resize(img, (400, 900))
#                     screen_height, screen_width, _ = img.shape
#                     crop_top = int(screen_height * 295 / 2400)
#                     crop_bottom = int(screen_height * 690 / 2400)
#                     crop_left = int(screen_width * 15 / 1080)
#                     crop_right = int(screen_width * 390 / 1080)
                    np_image = np.array(img)

# # Crop the NumPy array directly
                    cropped_image = np_image[810:1800, 35:1030, :]

# # Convert the cropped NumPy array back to PIL Image
                    cropped_img = Image.fromarray(cropped_image)

# # Convert the PIL Image to RGB mode
#                     cropped_img_rgb = cropped_img.convert('RGB')
                    plt.imshow(cropped_img)
                    plt.axis('off')  # Turn off the axis labels
                    plt.show() 
                     # Adjust the cropping region according to your screen resolution
                    break

                except cv.error as e:
                    print("Error processing image with OpenCV:", e)
                    retries += 1
                    time.sleep(1)

            if image is None:
                print("Failed to capture or process image after multiple retries")
                continue

            # Rest of the code (function calls, swipe commands, etc.) goes here

            start_time = time.time()
            array = divimage.scanimage(crimage)
            print(array)

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Function 'scanimage' took {execution_time:.6f} seconds.")
            if np.array_equal(array, previous_array):
                same_array_count += 1
            else:
                same_array_count = 0
            if same_array_count == 5:
                undobottonhandle.click_coordinates(middle_x,middle_y) 
                same_array_count = 0  # Reset the count
                previous_array = None  # Reset the previous array
                continue  # Start the loop again 
            previous_array = array      
            moveno = manager.runa(array)
            move=get_letter(moveno)
            print(move)

            if move == 'u':
                swipe_command = ['adb', '-s', device, 'shell', 'input', 'swipe', '500', '2000', '500', '1000', '100']
                subprocess.run(swipe_command)
            if move == 'd':
                swipe_command = ['adb', '-s', device, 'shell', 'input', 'swipe', '500', '1000', '500', '2000', '100']
                subprocess.run(swipe_command)
            if move == 'r':
                swipe_command = ['adb', '-s', device, 'shell', 'input', 'swipe', '200', '1000', '700', '1000', '100']
                subprocess.run(swipe_command)
            if move == 'l':
                swipe_command = ['adb', '-s', device, 'shell', 'input', 'swipe', '700', '1000', '200', '1000', '100']
                subprocess.run(swipe_command)

            moves += 1
            total_moves += 1
            if moves == 30:
                runs += 10
                moves = 0

        except subprocess.CalledProcessError as e:
            print("Error executing ADB command:", e)
            time.sleep(1)

        except Exception as e:
            print("An error occurred:", e)
            time.sleep(1)

except KeyboardInterrupt:
    print("Keyboard interrupt. Exiting...")

print("Total moves:", total_moves)
print("Final runs:", runs)
