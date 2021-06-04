# lineprinter
Print to thermal printers (such as Posiflex Aura PP7000-II) that understand raw serial data for text and signals.

Most methods are based on <http://www.dream-enterprise.com/_wp/340-2/>, whose author says the following: "As I am working on this project I will add more items to this page. If you have any feedback or if you know of any commands I can add please send them my way to Contact@DREAM-Enterprise.com.  Thank you."
The following significant changes apply:
- Almost no code is untouched, and there is now a python module with a reusable class.
- The codes for center and right justify are switched to match the hardware codes.
- The width and height can be set independently.
- Formatting is tracked for debugging purposes (Show formatting in the console by setting `printer.enableEcho = True`).
- Opcodes are stored in variables (used as constants by convention: all-uppercase) and have tables for converting to or from formatting strings for debugging or future use.
- Invalid opcodes result in errors.


## Usage

- Import the class such as via:
  `from lineprinter import LinePrinter`
- Set variables in the constructor when you create a LinePrinter. For example:
  - `printer = LinePrinter(com='/dev/ttyS0')` for Linux
  - `printer = LinePrinter(com='COM7')` for Windows (may not work yet)


## Troubleshooting
### Serial mode
- Set all switches to 0 as per the defaults for serial mode in the PP7700-II manual and ensure that the printer driver and port are set to a baud rate of 19200 accordingly.
- If you are using a Prolific USB to serial adapter and the port in device manager is called "PL2303HXA PHASED OUT SINCE 2012", go to properties, choose other driver, and choose the prolific driver. Ensure the baud rate is 19200.
### Other modes
- Set the baud rate to match the device, such as via:
  `printer = LinePrinter(com='COM7' baud=...)` where `...` is the correct baud rate.


## Related Projects

On pypi:
- `linemode` - "Python library for communicating with line-mode thermal printers (currently tested with the TSP700II USB). Currently works only with printers that support the star line mode protocol but adding support for other similar printers should be possible." - https://github.com/bwhmather/python-linemode

More:
- https://github.com/midhunmadhuk/Posiflex: *completely* undocumented--See [issue 1 on Posiflex](https://github.com/midhunmadhuk/Posiflex/issues/1)

### For a specific brand or model of printer or host
On pypi:
- `ppa6`: "for Peripage A6 and A6+" - https://github.com/bitrate16/ppa6-python
- `zebra`: "While EPL2 commands are used for most functions, raw ZPL can still be sent to the label printer" - https://www.wyre-it.co.uk/zebra/
- `PyESCPOS`: "for Epson© ESC/POS® compatible printers" - https://github.com/base4sistemas/pyescpos/
- ~~`python-thermal-printer-3`: "Adafruit thermal library modified for python 3." - https://github.com/ConorMatthews/Python-Thermal-Printer/tree/Python3andRaspberryPi3~~
- `adafruit-circuitpython-thermal-printer`: "CircuitPython module for control of various small serial thermal printers" - https://github.com/adafruit/Adafruit_CircuitPython_Thermal_Printer
- `afthermal`: "...alpha status...driver/library for the popular Adafruit (originally Cashino A2) thermal printer" - https://github.com/mbr/afthermal

### For languages other than Python
- sales-device-server (Java): "Work with Posiflex aura 6900u-b by serial port(rs-232)" - https://github.com/croacker/sales-device-server
- PosiflexDemo (Java): "A demo android project for posiflex thermal pos printer" - https://github.com/alex31n/PosiflexDemo
- PosiflexPrinter (Kotlin): "printer app for posiflex devices" - https://github.com/htetarkarzaw/PosiflexPrinter
  - It only has 3 commits but one is barcode printing.
- cordova-plugin-posiflexprint (Java): (*completely* undocumented--See [issue 1 on cordova-plugin-posiflexprint](https://github.com/thembinkosiklein/cordova-plugin-posiflexprint/issues/1)) - https://github.com/thembinkosiklein/cordova-plugin-posiflexprint

If you find more projects to add to this list including your own, please post it as an issue or PR!
