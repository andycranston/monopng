#
# @(!--#) @(#) monopng.py, version 007, 17-september-2019
#
# Python class to create monochrome PNG files
#

import zlib

class MonoPNG:

    def __init__(self, wide, high):
        self.wide = wide
        self.high = high
        self.bitmap = bytearray((wide + 1) * high)

    def dword(self, i):
        b0 = (i & 0x000000FF) // 0x00000001
        b1 = (i & 0x0000FF00) // 0x00000100
        b2 = (i & 0x00FF0000) // 0x00010000
        b3 = (i & 0xFF000000) // 0x01000000
    
        return bytes([b3, b2, b1, b0])

    def dwordreverse(self, ba):
        return (ba[0] << 24) + (ba[1] << 16) + (ba[2] << 8) + ba[3]

    def fill(self, brightness):
        for x in range(0, self.wide):
            for y in range(0, self.high):
                self.bitmap[(y * (self.wide + 1)) + (x + 1)] = brightness

    def plot(self, x, y, brightness):
        if ((x >= 0) and (x < self.wide) and (y >= 0) and (y < self.high)):
            self.bitmap[(y * (self.wide + 1)) + (x + 1)] = brightness & 0xFF

    def peek(self, x, y):
        if ((x >= 0) and (x < self.wide) and (y >= 0) and (y < self.high)):
            brightness = self.bitmap[(y * (self.wide + 1)) + (x + 1)]
        else:
            brightness = 0
        return brightness

    def deltaline(self, x, y, xdelta, ydelta, llength, brightness):
        for i in range(0, llength):
            self.plot(x, y, brightness)
            x += xdelta
            y += ydelta

    def horizline(self, x, y, llength, brightness):
        for i in range(0, llength):
            self.plot(x + i, y, brightness)

    def vertiline(self, x, y, llength, brightness):
        for i in range(0, llength):
            self.plot(x, y + i, brightness)

    def solidrectangle(self, x, y, wide, high, brightness):
        for i in range(0, wide):
            for j in range(0, high):
                self.plot(x+i, y+j, brightness)

    def rectangle(self, x, y, wide, high, brightness, thickness=1):
        while thickness > 0:
            self.horizline(x,            y,            wide, brightness)
            self.horizline(x,            y + high - 1, wide, brightness)
            self.vertiline(x,            y,            high, brightness)
            self.vertiline(x + wide - 1, y,            high, brightness)
            x += 1
            y += 1
            thickness -= 1
            wide -= 2
            high -= 2

    def paste(self, overlay, x, y):
        for i in range(0, overlay.wide):
            for j in range(0, overlay.high):
                self.plot(x+i, y+j, overlay.peek(i, j))

    def print(self):
        print("Wide:{}   High:{}".format(self.wide, self.high))
        
        for y in range(0, self.high):
            for x in range(0, self.wide):
                brightness = self.bitmap[(y * (self.wide + 1)) + (x + 1)]
                if brightness == 0xFF:
                    print(".", sep='', end='')
                elif brightness == 0x00:
                    print("#", sep='', end='')
                else:
                    print("?", sep='', end='')
            print("")

    def write(self, filename):
        f = open(filename, "wb")
    
        bitdepth = 8             # one byte per pixel
        colourtype = 0           # true grayscale (no palette)
        compression = 0          # zlib
        filtertype = 0           # adaptive (each scanline seperately)
        interlaced = 0           # no interlacing
    
        pnghdr = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')

        f.write(pnghdr)

        data = b""
        data += self.dword(self.wide) + self.dword(self.high)
        data += bytes([bitdepth])
        data += bytes([colourtype])
        data += bytes([compression])
        data += bytes([filtertype])
        data += bytes([interlaced])
    
        block = "IHDR".encode('ascii') + data
    
        ihdr = self.dword(len(data)) + block + self.dword(zlib.crc32(block))
    
        f.write(ihdr)
    
        data = b""
        compressor = zlib.compressobj()
        data = compressor.compress(self.bitmap)
        data += compressor.flush()       #!! what!?
    
        block = "IDAT".encode('ascii') + data
    
        idat = self.dword(len(data)) + block + self.dword(zlib.crc32(block))
    
        f.write(idat)
    
        data = b""
        block = "IEND".encode('ascii') + data
    
        iend = self.dword(len(data)) + block + self.dword(zlib.crc32(block))
    
        f.write(iend)
        f.flush()
        f.close()
    
    def read(self, filename):
        f = open(filename, "rb")

        ba = bytearray(f.read())

        f.close()

        pos = 0

        if pos + 8 > len(ba):
            return False

        pnghdr = bytearray(8)

        pnghdr[0] = 0x89
        pnghdr[1] = ord('P')
        pnghdr[2] = ord('N')
        pnghdr[3] = ord('G')
        pnghdr[4] = 13
        pnghdr[5] = 10
        pnghdr[6] = 26
        pnghdr[7] = 10

        if pnghdr != ba[pos:pos+8]:
            return False

        ### print('PNG header present')

        pos += 8

        if pos + 25 > len(ba):
            return False

        sizeihdr = self.dwordreverse(ba[pos:pos+4])

        if sizeihdr != 13:
            return False

        ihdrtext = bytearray(4)
        ihdrtext[0] = ord('I')
        ihdrtext[1] = ord('H')
        ihdrtext[2] = ord('D')
        ihdrtext[3] = ord('R')

        if ihdrtext != ba[pos+4:pos+8]:
            return False

        ### print('IHDR found')

        if ba[pos+16] != 8:
            return False
        if ba[pos+17] != 0:
            return False
        if ba[pos+18] != 0:
            return False
        if ba[pos+19] != 0:
            return False
        if ba[pos+20] != 0:
            return False

        ### print('IHDR detail ok')

        self.wide = self.dwordreverse(ba[pos+8:pos+12])
        self.high = self.dwordreverse(ba[pos+12:pos+16])

        pos += 25

        if pos + 12 > len(ba):
            return False

        sizeidat = self.dwordreverse(ba[pos:pos+4])

        idattext = bytearray(4)
        idattext[0] = ord('I')
        idattext[1] = ord('D')
        idattext[2] = ord('A')
        idattext[3] = ord('T')

        if idattext != ba[pos+4:pos+8]:
            return False

        ### print(pos + 8, pos + 8 + sizeidat - 1)

        self.bitmap = zlib.decompress(ba[pos+8:pos+8+sizeidat])

        ### print(len(self.bitmap))
        if len(self.bitmap) != (self.wide + 1) * self.high:
            return False

        return True

############################################################

# end of file
