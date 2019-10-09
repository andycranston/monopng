#! /usr/bin/python3
#
# @(!--#) @(#) scrshot.py, version 002, 09-october-2019
#
# a screenshot program by Andy Cranston
#
# cool feature #1: screenshots saved as monochrome PNG
#
# cool feature #2: sending a UDP packet to the host results in
#                  triggering a screen shot
#

############################################################################

DEBUG = False

############################################################################

import sys
import os
import argparse
import time
import datetime
import socket
import select
import pyautogui
from PIL import Image

import monopng

############################################################################

UDP_PORT = 8333
SLEEP_INTERVAL = 0.1
WATCHDOG_INTERVAL = 20
PIXEL_REGION = 200
TASKBAR_PIXELS = 40
SCREEN_SHOT_DIRECTORY = 'c:\\andyc\\00tmp'

############################################################################

def rgb2mono(rgb):
    return (rgb[0] + rgb[1] + rgb[2]) // 3

############################################################################

def string2bytearray(s):
    ba = bytearray(len(s))

    for i in range(0, len(s)):
        ba[i] = ord(s[i])

    return ba

############################################################################

#
# Main
#

def main():
    global progname

    # create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # bind the socket to the port
    sock.bind(('', UDP_PORT))

    packetpayload = string2bytearray('please take a screenshot now')

    screenWidth, screenHeight = pyautogui.size()

    screenregion = (0, 0, screenWidth, screenHeight - TASKBAR_PIXELS)

    mpng = monopng.MonoPNG(screenWidth, screenHeight - TASKBAR_PIXELS)

    midWidth = screenWidth // 2

    lastMouseX = -1
    lastMouseY = -1

    watchdogcounter = 0

    while True:
        takescreenshot = False

        currentMouseX, currentMouseY = pyautogui.position()

        if DEBUG:
            print(lastMouseX, lastMouseY)
            print(currentMouseX, currentMouseY)

        # see if mouse movements mean a screenshot
        if (currentMouseX != lastMouseX) or (currentMouseY != lastMouseY):
            if (lastMouseY == 0) and (currentMouseY > 0):
                if abs(midWidth - currentMouseX) <= PIXEL_REGION:
                    takescreenshot = True

        # see if a UDP packet has been receieved which would trigger a screesnot
        rlist, wlist, xlist = select.select([sock], [], [], 0.0)

        if DEBUG:
            print(rlist)

        if len(rlist) > 0:
            try:
                packet, address = sock.recvfrom(65536)
                if len(packet) == len(packetpayload):
                    if packet == packetpayload:
                        takescreenshot = True
            except ConnectionResetError:
                print("{}: connecton reset error - going again".format(progname), file=sys.stderr)

        if takescreenshot == False:
            if DEBUG:
                print('No Change - sleeping')
            time.sleep(SLEEP_INTERVAL)
            watchdogcounter += 1
            if watchdogcounter > WATCHDOG_INTERVAL:
                print('Waiting for screenshot trigger action')
                watchdogcounter = 0
        else:
            print('Taking screenshot')
            scrshotfile = '{}\\scrshot-{:%Y%m%d-%H%M%S}.png'.format(SCREEN_SHOT_DIRECTORY, datetime.datetime.now())

            scrshot = pyautogui.screenshot(region=screenregion)

            for x in range(0, screenWidth):
                for y in range(0, screenHeight - TASKBAR_PIXELS):
                    mpng.plot(x, y, rgb2mono(scrshot.getpixel( (x, y) )))

            mpng.write(scrshotfile)

            print('Done')
                
        lastMouseX = currentMouseX
        lastMouseY = currentMouseY

    return 0

############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
