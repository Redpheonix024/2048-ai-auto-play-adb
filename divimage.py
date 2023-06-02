import cv2
import pytesseract
import matplotlib.pyplot as plt
import numpy as np

def preprocess_image(img):
    # Apply image processing techniques here
    # For example, you can enhance sharpness using a sharpening filter
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sharpened_img = cv2.Canny(gray, 10, 150)

    # Perform any other desired image processing steps
    processed_img = sharpened_img

    return processed_img


def mydata(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Preprocess the image
    #imgs = preprocess_image(img)

    # Convert the preprocessed image to text
    imgs=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # plt.imshow(imgs)
    # plt.axis('on')  # Turn off the axis labels
    # plt.show()
    text = pytesseract.image_to_string(imgs, config='--psm 6 -l eng')

    numbers = [int(s) for s in text.split() if s.isdigit()]
    if numbers:
        return numbers[0]
    return 0

# def divide_image(image, grid_size):
#     height, width, _ = image.shape
#     cell_width = width // grid_size[1]+1
#     cell_height = height // grid_size[0]
#     crop_margin = 10  # Adjust this value to control the amount of cropping
#     width_shift = 0  # Adjust this value to control the width shift
#     height_shift = 0  # Adjust this value to control the height shift

#     divided_image_tiles = []
#     for i in range(4):
#         for j in range(4):
#             x = j * cell_width + crop_margin - width_shift
#             y = i * cell_height + crop_margin - height_shift

#             # # Crop the first row slightly differently
#             # if j == 1:
#             #     width_shift=2
#             if j == 3:
#                 width_shift=3 
#                 height_shift=6   
#             # if j == 1:
#             #     width_shift=5    
#             if j == 0:
#                 height_shift=-6
#                 #width_shift=3
#             #     y += crop_margin
#             if i == 2:
#                 height_shift=5
#             if i == 3:
#                 width_shift=2
#                 height_shift=5

#                 #y += crop_margin   
#             # Crop the bottom row slightly differently
#             # elif i == grid_size[0] - 1:
#             #     y -= crop_margin

#             cell_image = image[y:y+cell_height-2*crop_margin, x:x+cell_width-2*crop_margin]

#             # plt.imshow(cell_image)
#             # plt.axis('on')  # Turn off the axis labels
#             # plt.show()
#             divided_image_tiles.append(cell_image)

#     return divided_image_tiles

def divide_image(image):
    divided_image_tiles = []

    grid_size = 4



    for i in range(grid_size):
        for j in range(grid_size):

            if(i==0 and j==0 ):
                cell_image = image[20:95, 10:85]
                divided_image_tiles.append(cell_image)
            if(i==0 and j==1 ):
                cell_image = image[20:95, 100:175]
                divided_image_tiles.append(cell_image)
            if(i==0 and j==2 ):
                cell_image = image[20:95, 190:265]
                divided_image_tiles.append(cell_image) 
            if(i==0 and j==3 ):
                cell_image = image[20:95, 280:355]
                divided_image_tiles.append(cell_image)       
            if(i==1 and j==0 ):
                cell_image = image[110:185, 10:85]
                divided_image_tiles.append(cell_image)
            if(i==1 and j==1 ):
                cell_image = image[110:185, 100:175]
                divided_image_tiles.append(cell_image)
            if(i==1 and j==2 ):
                cell_image = image[110:185, 190:265]
                divided_image_tiles.append(cell_image) 
            if(i==1 and j==3 ):
                cell_image = image[110:185, 280:355]
                divided_image_tiles.append(cell_image) 
            if(i==2 and j==0 ):
                cell_image = image[204:279, 10:85]
                divided_image_tiles.append(cell_image)
            if(i==2 and j==1 ):
                cell_image = image[204:279, 100:175]
                divided_image_tiles.append(cell_image)
            if(i==2 and j==2 ):
                cell_image = image[204:279, 190:265]
                divided_image_tiles.append(cell_image) 
            if(i==2 and j==3 ):
                cell_image = image[204:279, 280:355]
                divided_image_tiles.append(cell_image) 
            if(i==3 and j==0 ):
                cell_image = image[295:370, 10:85]
                divided_image_tiles.append(cell_image)
            if(i==3 and j==1 ):
                cell_image = image[295:370, 100:175]
                divided_image_tiles.append(cell_image)
            if(i==3 and j==2 ):
                cell_image = image[295:370, 190:265]
                divided_image_tiles.append(cell_image) 
            if(i==3 and j==3 ):
                cell_image = image[295:370, 278:360]
                divided_image_tiles.append(cell_image)     
    return divided_image_tiles




def scanimage(image):
    #image = cv2.resize(image, (350, 350))
    # plt.imshow(image)
    # plt.axis('on')  # Turn off the axis labels
    # plt.show() 
    # resized_image_path = 'debugg.jpg'
    # cv2.imwrite(resized_image_path, image)
    rgb_image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    grid_size = (4, 4)
    divided_image_tiles = divide_image(rgb_image)

    number_array = []
    for i, tile in enumerate(divided_image_tiles):
        number = mydata(tile)
        # if (number >16000):
        #     number=16384

        number_array.append(number)
        
        # if number != 0:
        #     cv2.imwrite(f"data1/tile_{i}.png", tile)

    
    return number_array

# # Path to the image file
# image_path = 'debugg.jpg'

# # Read the image using OpenCV
# image = cv2.imread(image_path)

# # Extract numbers from the image using OCR
# number_array = scanimage(image)
# print(number_array)
# # Divide the image into tiles
# #divided_image_tiles = divide_image(image, (4, 4))

# # Check if the number of elements in number_array matches the number of divided_image_tiles
# # if len(number_array) != len(divided_image_tiles):
# #     missing_elements = len(divided_image_tiles) - len(number_array)
# #     number_array += [0] * missing_elements

# # # Display the cropped images in a single screen
# # fig, axes = plt.subplots(4, 4, figsize=(10, 10))
# # for i, ax in enumerate(axes.flat):
# #     ax.imshow(cv2.cvtColor(divided_image_tiles[i], cv2.COLOR_BGR2RGB))
# #     ax.axis('on')
# #     ax.set_title(str(number_array[i]))

# # plt.tight_layout()
# # plt.show()