"""
This project  will initialize the display using displayio and draw a solid black
background and display the Microchip "Meatball" logo
"""
import time
import board
import displayio
import adafruit_imageload
import digitalio
import microcontroller
from fourwire import FourWire
from adafruit_st7789 import ST7789
import adafruit_icm20x

import math
'''
def DisableAutoReload():
    import supervisor
    supervisor.runtime.autoreload = False
    print("Auto-reload is currently disabled.")
    print("After saving your code, press the RESET button.")
'''
       
# uncomment this if auto-reload is causing issues from your editor     
#DisableAutoReload()

# Change this to False to hide debug print statements
Debug = True

if Debug:
    print("Create pin called 'backlight' for LCD backlight on PA06")
# backlight = digitalio.DigitalInOut(board.LCD_LEDA)
backlight = digitalio.DigitalInOut(microcontroller.pin.PA06)
backlight.direction = digitalio.Direction.OUTPUT
if Debug:
    print("Turn TFT Backlight On")
backlight.value = False

# Release any resources currently in use for the displays
if Debug:
    print("Release displays")
displayio.release_displays()

if Debug:
    print("Create SPI Object for display")
spi = board.LCD_SPI()
tft_cs = board.LCD_CS
tft_dc = board.D4

DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 135
LOGO_WIDTH = 32
LOGO_HEIGHT = 30

if Debug:
    print("Create DisplayBus")
display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ST7789(
    display_bus, rotation=90, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rowstart=40, colstart=53
)

# Load the sprite sheet (bitmap)
if Debug:
    print("Load Sprite sheet")
sprite_sheet, palette = adafruit_imageload.load("/Meatball_32x30_16color.bmp",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)

# Create a sprite (tilegrid)
if Debug:
    print("Create Sprite")
sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width=1,
                            height=1,
                            tile_width=LOGO_WIDTH,
                            tile_height=LOGO_HEIGHT)

# Create a Group to hold the sprite
if Debug:
    print("Create Group to hold Sprite")
group = displayio.Group(scale=1)

# Add the sprite to the Group
if Debug:
    print("Append Sprite to Group")
group.append(sprite)

# Add the Group to the Display
if Debug:
    print("Add Group to Display")
display.root_group = group

# Set sprite location
if Debug:
    print("Set Sprite Initial Location")

i2c = board.I2C()  # use board.SCL and board.SDA pins for the IMU

try:
    icm = adafruit_icm20x.ICM20948(i2c, 0x69)
except:
    print("No ICM20948 found at default address 0x69. Trying alternate address 0x68.")
    try:
        icm = adafruit_icm20x.ICM20948(i2c, 0x68)
    except:
        print("No ICM20948 device found! Make sure the dev board and ruler are connected properly!")

#gravity = sqrt(98.8631)
#95.4991
#98.7003
#98.2958
'''
X_vals = []
Y_vals = []
Z_vals = []
'''
def game():
    
    group.x = 0
    group.y = 0
    width = 40
    height = 40
    x_rate = 5
    y_rate = 5
    counter = 0
    clock_rate = 0.1

    count = 0
    sum = 0

    while True:
        X, Y, Z = icm.acceleration
        '''
        X_vals.append(X)
        Y_vals.append(Y)
        Z_vals.append(Z)
        '''
        '''
        print("X: {:.2f}".format(X))
        print("Y: {:.2f}".format(Y))
        print("Z: {:.2f}".format(Z))
        time.sleep(0.1)
        counter += 1
        if counter > 50:
            break
        '''
        '''
        #measure gravity
        count += 1
        counter += 1
        sum += X**2 + Y**2 + Z**2
        time.sleep(0.01)
        if counter > 200:
            break
        '''
        #bounce meatball
        #if Z > 20 or Z < -20:
        if abs(X) > 3:
            x_rate = min(int(x_rate * 1.5), 30)
            print("x accelerating>>>>>>>>")
            print(f"X: {X} Y:{Y} Z: {Z}")

        if abs(Y) > 3:
            y_rate = min(int(y_rate * 1.5), 30)
            print("y accelerating>>>>>>>>")
            print(f"X: {X} Y:{Y} Z: {Z}")

        counter += 1
        if counter % 5== 0:
            if x_rate > 10:
                x_rate = int(x_rate / 2)
            elif x_rate > 5:
                x_rate -= 1

            if y_rate > 10:
                y_rate = int(y_rate / 2)
            elif y_rate > 5:
                y_rate -= 1
        group.x += x_rate
        if group.x > (DISPLAY_WIDTH - width + 5) or group.x < 0:
            x_rate = -x_rate
        
        group.y += y_rate 
        if group.y > (DISPLAY_HEIGHT - height + 5) or group.y < 0:
            y_rate = -y_rate
        time.sleep(clock_rate)
        print(counter)
        #if counter > 200:
        #    break
        if abs(Z - 10) > 5:
            break
    return

while True:
    X, Y, Z = icm.acceleration
    time.sleep(0.1)
    if abs(Z - 10) > 3:
        print("starting")
        time.sleep(1)
        game()
        time.sleep(1)
#print(sum/count)
#print(statistics.mean(X_vals), statistics.std(X_vals))
#print(statistics.mean(Y_vals), statistics.std(Y_vals))
#print(statistics.mean(Z_vals), statistics.std(Z_vals))