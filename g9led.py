#!/usr/bin/python2

import usb
import os
G9_VENDOR_ID = 0x046d
G9_PRODUCT_IDS = [0xc048, 0xc066, 0xc066]


def get_g9_device():
    for bus in usb.busses():
        for device in bus.devices:
            if device.idVendor == G9_VENDOR_ID and \
                   device.idProduct in G9_PRODUCT_IDS:
                return device.open()
    return None

def g9_change_color(device=None, red=None, green=None, blue=None):
    """ Change the color of an G9(X) leds
    g9: device 
    red: int between 0 and 255
    green: int between 0 and 255
    blue: int between 0 and 255
    """
    device = device or get_g9_device()
    assert device
    COMMAND = "\x10\x00\x80\x57"
    data = "%s%c%c%c" % (COMMAND, red, green, blue)
    REQUEST_TYPE = 0x34
    REQUEST = 0x09
    VALUE = 0x210
    INDEX = 0x01
    device.controlMsg(REQUEST_TYPE, REQUEST, data,
                      VALUE, INDEX)

def usage():
    exit('Usage: g9led.py RRGGBB')

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        if os.geteuid() != 0:
            exit("You aren't root. Exiting.")
        if len(argv[1]) != 6:
            usage() 
        g9_change_color(red=int(argv[1][:2], 16),
                        green=int(argv[1][2:4], 16),
                        blue=int(argv[1][4:6], 16))
    else:
        usage
