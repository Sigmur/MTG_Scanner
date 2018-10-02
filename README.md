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
  We bough 15.000 cards from a guy in a garage sale. After an hour of sorting & referencing ~1000 i got bored. So i spent the next month building something to do it automatically. I am not a smart man.
  Edit : we bought another 20k+ cards. Cards, cards everywhere.
  
## Software versions & requirements

### Python 3.4
  
| Name  | Description |
| ------------- | ------------- |
| Pillow  | Image manipulation library, required for pytesseract.   |
| pytesseract  | Wrapper around Tesseract OCR, see https://pypi.org/project/pytesseract/#installation for more installation instructions |
| mtgsdk  | Will use later, wrapper for easy calls on MTG official API to get card datas  |
| opencv-contrib-python | OpenCV (cv2) is a huge and powerfull image manipulation library, but it's hard to setup on raspberry. I followed http://www.life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3/ and had a few problems but got it working in the end  |

  Various required packages for tesseract, opencv, ect ect
  - sudo apt-get install libjpeg8-dev
  - sudo apt-get install libhdf5-dev
  - sudo apt-get install libhdf5-serial-dev
  - sudo apt install libqtgui4
  - sudo apt-get install tesseract-ocr
  
### Arduino

To speed up input/output :
https://github.com/mmarchetti/DirectIO

## Parts used

| Name | Description & usage | Image |
| ------------- | ------------- | ------------- |
| Raspberry 3 B+ (1) | The brain of the operation, ~30€ | ![Alt text](imgs/raspberry_pi_3.jpg?raw=true "Raspberry") |
| Arduino pro mini (~3/4+) | Used to drive the servos. A servo need a PWM signal, this type of arduino has 6 PWM pins, so 6 servos max per arduinos. They can be linked to handle 16/32/64 ... servos. | ![Alt text](imgs/arduino.jpg?raw=true "Arduino pro mini") |
| Dupont wires (a LOT) | Buy a lot of them and watch them spread all around your workbench. | ![Alt text](imgs/dupont_wires.jpg?raw=true "Dupont wires") |
| Stepper motor Nema 17 40Ncm (1) | Much torque, such precision (1.8°), very power (1.7A). Wow. Commonly found in cheap ass 3d printers (~10€/u). | ![Alt text](imgs/NEMA17.jpg?raw=true "Stepper motor NEMA 17") |
| Stepper motor driver board L298N (1) | Required, or no vroom. ~5€/u | ![Alt text](imgs/L298N.jpg?raw=true "L298N Stepper driver board") |
| Small servomotor SG90 (10+) | Used to move the filters, linked to the arduinos. ~2€/u | ![Alt text](imgs/servo-sg90.jpg?raw=true "Servomotor SG90") |
| Photo sensor (1) | Used to detect if a card is right under the camera | ![Alt text](imgs/photoresistor.jpg?raw=true "Raspberry") |
| USB Camera 'microscope' (1) | Not realy a microscope, ok magnification, manual calibration, with built in lighting. ~30€. | - |
| Lego (1 fuckton) | I don't have a CNC, but i've gathered the whole family Lego fortune. | - |
| Weird power supply (1) | I reconverted an old computer power supply, thank to our friendly german Great Scott for that trick. It's probably unsafe but heh. | - |

Overall cost ~150€
