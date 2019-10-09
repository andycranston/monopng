#! /usr/bin/python3
#
# @(!--#) @(#) scrtrigger.py, version 001, 09-october-2019
#
# trigger a screenshot by sending a UDP packet to the scrshot.py program
#
#

############################################################################

DEBUG = False

############################################################################

import sys
import os
import socket

############################################################################

UDP_PORT = 8333

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

    if DEBUG:
        print(sys.argv)
        print(len(sys.argv))

    if len(sys.argv) <= 1:
        host = '127.0.0.1'
    else:
        host = sys.argv[1]

    payloadstring = 'please take a screenshot now'
    packetpayload = string2bytearray(payloadstring)

    print('Sending "{}" to host {} on UDP port {}'.format(payloadstring, host, UDP_PORT))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(packetpayload, (host, UDP_PORT))

    sock.close()

    print('Done')

    return 0

############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
