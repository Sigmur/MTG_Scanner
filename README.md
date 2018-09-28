# MTG_Scanner
Magic The gathering card scanning & sorting machine

Current rev : 3
 - Read cards
 - Open correct filters
 - ~2sec per card
 - Store results in json file for later referencement
 
This is based on the card reference ad the bottom of the card, references were introduced in 2015, so this is not ideal for old cards, but whatever, it'll do for now.
Rev 4 will read card title and do more, but that means getting whole card database from MTG, ect ect. Bleh.

## How it works
  - Hardware side, the machine roll a card from the card dispenser, takes a picture with the camera, software magic happen to read the card, then open the corresponding filter and drop the card in the right bin.
  - Software side, we use OpenCV to cleanup & threshold the image, then send it to Tesseract OCR that will give us a text string from an image, after that the software parse the string using some regexps and voila, we have the card number, extention, language and type.
  
## Why ?
  We bough 20.000 cards from a guy in a garage sale. After an hour of sorting & referencing ~1000 i got bored. So i spent the next month building something to do it automatically. I am not a smart man.
  
## Python version & requirements
  Python version used to dev
  - Python 3.4+
  
| Name  | Description |
| ------------- | ------------- |
| Pillow  | Image manipulation library, required for pytesseract.   |
| pytesseract  | Wrapper around Tesseract OCR, see https://pypi.org/project/pytesseract/#installation for more installation instructions |
| mtgsdk  | Will use later, wrapper for easy calls on MTG official API to get card datas  |
| opencv-contrib-python | OpenCV (cv2) is a huge and powerfull image manipulation library, but it's hard to setup on raspberry. I followed http://www.life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3/ and had a few problems but got it working in the end  |
