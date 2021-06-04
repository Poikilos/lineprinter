#!/usr/bin/env python
from lineprinter import LinePrinter
import platform
import sys

try:
    import serial
    # You only need to import serial when checking for
    # serial exceptions (See
    # `except serial.serialutil.SerialException` below for an example).
except ModuleNotFoundError:
    print("You must first install pyserial such as via:")
    print("  python -m pip install --user pyserial")
    exit(1)


def test_modes(printer):
    # printer.reset()
    # ^ The constructor calls reset.
    printer.justifyCenter()
    printer.setSize(LinePrinter.SIZE_DOUBLE)
    printer.writeLine("big")
    printer.setSize(LinePrinter.SIZE_TRIPLE)
    printer.justifyRight()
    printer.writeLine("bigger")
    printer.justifyLeft()

    printer.setSize(LinePrinter.SIZE_TALL)
    printer.writeLine("tall")
    printer.setSize(LinePrinter.SIZE_TALLER)
    printer.writeLine("taller")
    printer.setSize(LinePrinter.SIZE_WIDE)
    printer.writeLine("wide")
    printer.setSize(LinePrinter.SIZE_WIDER)
    printer.writeLine("wider")

    printer.setSize(LinePrinter.SIZE_NORMAL)

    printer.flip(True)
    printer.writeLine("flipped")

    printer.flip(False)

    printer.rotateClockwise(True)
    printer.writeLine("rotated")

    printer.rotateClockwise(False)

    printer.justifyLeft()
    printer.setSize(LinePrinter.SIZE_NORMAL)
    printer.writeLine("normal")
    # printer.writeLine("{}".format(printer.com))

    printer.flip(True)
    printer.rotateClockwise(True)
    printer.writeLine("rotated&flipped")
    printer.reset()
    printer.writeLine("reset")

def ex_help():
    print("See the troubleshooting section of the readme.md file using a text editor.")
    print("")

def main():
    tryComs = []
    com = None
    if len(sys.argv) > 1:
        com = sys.argv[1]
        printer = LinePrinter(com=com)
    else:
        if platform.system() == "Windows":
            for i in range(13, 0, -1):
                tryComs.append("COM{}".format(i))
        else:
            for i in range(12, -1, -1):
                tryComs = ["/dev/ttyUSB{}".format(i)]
        lastEx = None
        foundCom = None
        for tryCom in tryComs:
            try:
                printer = LinePrinter(com=tryCom)
                lastEx = None
                foundCom = tryCom
                break
            except serial.serialutil.SerialException as ex:
                lastEx = ex
        if lastEx is not None:
            print("Tried: {}".format(tryComs))
            ex_help()
            raise lastEx
        else:
            print("Found usable COM (Set com manually in a non-test"
                  " scenario so it doesn't interrupt your 3D printer or"
                  " something!): {}".format(foundCom))
    printer.enableEcho = True
    test_modes(printer)
    printer.end()
    # ^ self.end calls self.cut() and self.close()
    print("All tests completed.")
    print("To verify success, check whether the resulting print"
          " matches the debug output above.")
    print("If nothing happens, set the com port (used {})."
          "".format(printer.com))
    print("")
    print("Examples:")
    print("- For Windows, ensure Python is installed with the"
          " Add to PATH option, go to Command Prompt, cd to the"
          " lineprinter directory, then type:")
    print("  python tests.py COM9")
    print("  REM or whatever your com port is"
          " (find it in device manager)")
    print("- Linux:")
    print("  python3 tests.py /dev/ttyUSB0")
    print("  # Only use ttyUSB0 if you use a USB-serial adapter.")


if __name__ == "__main__":
    main()
