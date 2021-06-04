#!/usr/bin/env python
try:
    import serial
except ModuleNotFoundError:
    print("You must first install pyserial such as via:")
    print("  python -m pip install --user pyserial")
    exit(1)


class LinePrinter:
    SIZE_NORMAL = 0
    SIZE_TALL = 1
    SIZE_TALLER = 2
    SIZE_WIDE = 10
    SIZE_WIDER = 20
    SIZE_DOUBLE = 11
    SIZE_TRIPLE = 22

    SIZE_MODES = [
        (SIZE_NORMAL, "normal", b'\x1D\x21\x00'),
        (SIZE_TALL, "tall", b'\x1D\x21\x01'),
        (SIZE_TALLER, "taller", b'\x1D\x21\x02'),
        (SIZE_WIDE, "wide", b'\x1D\x21\x10'),
        (SIZE_WIDER, "wider", b'\x1D\x21\x20'),
        (SIZE_DOUBLE, "big", b'\x1D\x21\x11'),
        (SIZE_TRIPLE, "bigger", b'\x1D\x21\x22'),
    ]

    JUSTIFY_LEFT = 0
    JUSTIFY_CENTER = 1
    JUSTIFY_RIGHT = 2

    JUSTIFY_MODES = [
        (JUSTIFY_LEFT, "left", b'\x1B\x61\x00'),
        (JUSTIFY_CENTER, "center", b'\x1B\x61\x01'),
        (JUSTIFY_RIGHT, "right", b'\x1B\x61\x02'),
    ]

    def __init__(self, com=None, baud=None, width=42, preCutFeedCount=6):
        '''
        Keyword arguments:
        self.preCutFeedCount -- Specify how many lines to feed before
                   cutting. Ensure there is enough paper used before
                   cutting to avoid jams.
        '''
        if com is None:
            com = "/dev/ttyUSB0"
            if platform.system() == "Windows":
                com = "COM7"
            print("WARNING: Guessed com={}:".format(com))
            print("- Set com manually in a non-test scenario"
                  " so it doesn't interrupt your 3D printer"
                  " or something!")
        self.com = com
        if baud is None:
            baud = 19200
            print("WARNING: Guessed baud={} (This rate is only"
                  " for thermal printers such as"
                  " Posiflex Aura PP7000-II when in serial mode"
                  " --See the manual for your device.)"
                  "".format(baud))
        self.baud = baud
        self.width = width
        self.preCutFeedCount = preCutFeedCount

        self.enableEcho = False
        self._indent = ""
        self._tab = "  "
        self._in_size = None
        self._in_just = None
        self._formats = []

        try:
            self.ser = serial.Serial(self.com, self.baud, timeout=0,
                                     parity=serial.PARITY_NONE)
        except serial.serialutil.SerialException as ex:
            print("")
            print("You can get the proper port via:")
            print("  sudo dmesg | grep tty")
            print("")
            print("For example,")
            print("\"[1537133.727889] usb 2-1: pl2303 converter now"
                  " attached to ttyUSB0\"")
            print("shows that /dev/ttyUSB0 is the correct com.")
            print("")
            raise ex
        self.reset()

    def _echo_if(self, text, tabs=0):
        '''
        Write to standard output if self.enableEcho is true.

        Keyword arguments:
        tabs -- Modify self._indent by this many instances of
                self._tab before writing to standard output. If
                negative then dedent this many times.
        '''
        if self.enableEcho:
            if tabs >= 0:
                print(self._indent + text)
        if tabs < 0:
            for i in range(tabs, 0):
                self._dedent_echo()
        elif tabs > 0:
            for i in range(tabs):
                self._indent_echo()
        if self.enableEcho:
            if tabs < 0:
                print(self._indent + text)

    def _push_format(self, text):
        self._formats.append(text)
        self._echo_if("<{}>".format(text), tabs=1)

    def _pop_format(self, text):
        i = None
        try:
            i = self._formats.index(text)
        except ValueError:
            i = None
        if i is not None:
            if self._formats[-1] == text:
                self._formats = self._formats[:-1]
                self._echo_if("</{}>".format(text), tabs=-1)
            else:
                self._echo_if("</{}>".format(text), tabs=-1)
                self._formats = self._formats[:i] + self._formats[i+1:]
                self._echo_if("<!--still formatted in: {} after"
                              " removing format [{}]-->"
                              "".format(self._formats, i))
        else:
            self._echo_if("<!--already not formatted: {}-->"
                          "".format(text))

    def _indent_echo(self):
        self._indent += self._tab

    def _dedent_echo(self):
        if len(self._indent) < len(self._tab):
            self._echo_if("WARNING: More modes ended than started.")
        self._indent = self._indent[:-len(self._tab)]

    def close(self):
        if self.ser.isOpen():
            self.ser.close()

    def cut(self):
        self._echo_if("<cut/>")
        if not self.ser.isOpen():
            self.ser.open()
        line = range(self.preCutFeedCount)
        for i in line:
            self.lineFeed()
        self.ser.write(b'\x1D\x56\x00')

    def end(self):
        '''cut the paper and close the connection'''
        self._indent = ""
        self.cut()
        self.close()

    def reset(self):
        '''
        Reset all commands sent to printer.
        '''
        self._indent = ""
        if not self.ser.isOpen():
             self.ser.open()
        self.ser.write(b'\x1B\x40')

    def lineFeed(self):
        if not self.ser.isOpen():
            self.ser.open()
        self._echo_if("")
        self.ser.write(b'\x0a')

    def writeLine(self, text):
        if not self.ser.isOpen():
            self.ser.open()
        self._echo_if("{}".format(text))
        self.ser.write(text.encode())
        self.lineFeed()

    def writeCentered(self, text):
        if not self.ser.isOpen():
            self.ser.open()
        self._echo_if("<center>{}</center>".format(text))
        self.ser.write((text.center(self.width)).encode())
        self.ser.write('\n'.encode())

    def writeLines(self, lines):
        for text in lines:
            self.writeLine(text)

    def rotateClockwise(self, on):
        if on is True:
            on = 1
        elif on is False:
            on = 0
        if not self.ser.isOpen():
            self.ser.open()
        if on == 0:
            self._pop_format("rotate-clockwise")
            self.ser.write(b'\x1B\x56\x48')
        elif on == 1:
            self._push_format("rotate-clockwise")
            self.ser.write(b'\x1B\x56\x49')
        else:
            raise ValueError("The value should be True/1/False/0 but is"
                             " \"{}\"".format(on))

    def justifyLeft(self):
        self._justify(0)

    def justifyRight(self):
        self._justify(1)

    def justifyCenter(self):
        self._justify(2)

    def _justify(self, justifyCode):
        if not self.ser.isOpen():
            self.ser.open()
        i = None
        name = None
        signal = None
        for mode in LinePrinter.JUSTIFY_MODES:
            if mode[0] == justifyCode:
                i, name, signal = mode
                break

        if i is None:
            raise ValueError("The value should be in"
                             " LinePrinter.JUSTIFY_CODES but is \"{}\""
                             "".format(on))
        if self._in_just is not None:
            self._echo_if("</{}>".format(self._in_just), tabs=-1)
            self._in_just = None
        if justifyCode != 0:
            self._in_just = name
            self._echo_if("<{}>".format(self._in_just), tabs=1)

        self.ser.write(signal)

    # @staticmethod
    # def sizeCodeToStr(code):

    def setSize(self, sizeCode):
        if not self.ser.isOpen():
            self.ser.open()
        i = None
        name = None
        signal = None
        for mode in LinePrinter.SIZE_MODES:
            if mode[0] == sizeCode:
                i, name, signal = mode
                break
        if i is None:
            raise ValueError("The value should be in"
                             " LinePrinter.SIZE_MODES but is"
                             " \"{}\"".format(on))
        if self._in_size is not None:
            self._echo_if("</{}>".format(self._in_size), tabs=-1)
            self._in_size = None
        if sizeCode != 0:
            self._in_size = name
            self._echo_if("<{}>".format(self._in_size), tabs=1)

        self.ser.write(signal)

    def flip(self, on):
        if on is True:
            on = 1
        elif on is False:
            on = 0
        if not self.ser.isOpen():
            self.ser.open()
        if on == 0:  # right side up
            self._pop_format("flip")
            self.ser.write(b'\x1B\x7B\x02')
        elif on == 1:  #  upside down
            self._push_format("flip")
            self.ser.write(b'\x1B\x7B\x01')
        else:
            raise ValueError("The value should be True/1/False/0 but is"
                             " {}".format(on))

def main():
    print("The module should be imported instead of running.")
    print("See readme.md or tests.py for usage.")
    pass


if __name__ == "__main__":
    main()
