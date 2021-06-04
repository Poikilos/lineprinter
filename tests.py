#!/usr/bin/env python
from lineprinter import LinePrinter


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


def main():
    pass
    printer = LinePrinter()
    printer.enableEcho = True
    test_modes(printer)
    printer.end()
    # ^ self.end calls self.cut() and self.close()
    print("All tests completed.")
    print("To verify success, check whether the resulting print matches"
          " the debug output above.")


if __name__ == "__main__":
    main()
