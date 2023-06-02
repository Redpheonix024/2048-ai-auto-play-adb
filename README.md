# 2048 Automatic Player

This is a simple 2048 automatic player that is guaranteed to win and achieve a high score. The player is designed to be connected to your phone for seamless gameplay.

## Introduction

2048 is a popular puzzle game where the objective is to slide numbered tiles on a grid to combine them and create a tile with the number 2048. This automatic player takes control of the game and uses an algorithm to make optimal moves and achieve the highest possible score.

## Features

- Automatically plays the 2048 game on your phone
- Uses an algorithm to make optimal moves and maximize the score
- Guarantees a win and achieves a high score

## Installation

1. Clone the repository to your local machine.
2. Open the interference in Python script using Visual Studio Code (preferred) by navigating to the project folder and opening `main.py`.
3. Connect your phone to your computer using a USB cable.

4.  Download and install Tesseract OCR by following these steps:

- Download the Tesseract OCR installer for Windows from the official GitHub repository: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)
- Run the installer and follow the on-screen instructions to install Tesseract OCR. Make note of the installation directory.
- Open the `divimage.py` file in your project folder using a text editor.
- Locate the line that sets the Tesseract executable path:

  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

- Update the path in this line to match the directory where you installed Tesseract OCR. For example:

  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Path\To\Tesseract-OCR\tesseract.exe'
  ```this is the default path

5. Enable USB debugging on your Android device by following these steps:

   - Open the Settings app on your Android device.
   - Scroll down and tap on "About phone" or "About device."
   - Find the "Build number" entry and tap it seven times to enable Developer options.
   - Go back to the main Settings screen and scroll down to find "Developer options."
   - Enter the Developer options menu and toggle on the "USB debugging" option.

6. Install ADB (Android Debug Bridge) on your computer by following these steps:

   - Download the Android SDK Platform-Tools from the official Android Developers website: [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)
   - Extract the downloaded ZIP file to a location on your computer.
   - Add the location of the extracted `platform-tools` folder to your system's PATH environment variable.

   Note: For detailed instructions on installing ADB, please refer to the official Android documentation: [https://developer.android.com/studio/command-line/adb](https://developer.android.com/studio/command-line/adb)
   
7.Run  cammand pip install -r requirements.txt in cmd or terminal all the the extra moudles will be installed 

## Usage

1. Open the 2048 game on your phone.
2. For linux systems frist use cammand
   g++ -shared -fPIC -o lib20489.so 2048.cpp 
   after installing g++ and fPIC and then run the above command
   You also want to uncomment the line  "pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'" as it uses windows directory of      tesseract  
3. Run the automatic player script by executing `main.py`.
4. The script will automatically take control of the game and make optimal moves.
5. Sit back and watch as the player wins and achieves a high score.

   


## Credits

This project takes inspiration and leverages code from the following repositories:

- [nneonneo/2048-ai](https://github.com/nneonneo/2048-ai): The AI brain for playing 2048.
- [saibhaskar24/2408AI](https://github.com/saibhaskar24/2408AI): Provides the basic idea for the automatic player.
- This project also utilizes ChatGPT, a powerful language model developed by OpenAI. ChatGPT is employed to provide assistance and support in developing the automatic player. We acknowledge the contribution of ChatGPT in enhancing the project's capabilities.

I express our gratitude to the authors of these repositories for their valuable contributions and insights.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue on the GitHub repository.

## About This Repository

This is my first GitHub repository, and I'm excited to share my project with the community. I appreciate any feedback and guidance as I continue to learn and improve my coding skills.

Thank you for checking out my project!

