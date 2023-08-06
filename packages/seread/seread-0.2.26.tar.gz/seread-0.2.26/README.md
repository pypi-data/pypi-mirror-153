Project seread
==============

**IN CONSTRUCTION NOW - VERSION 0.1.23+ now may work, 2.3 currently**

-   READ serial ports
-   save data to file and influxdb

TL;DR
=====

start
-----

**If you have a device /dev/ttyACM0**

Try `./bin_seread -D /dev/ttyACM0 -t 2,10 -c word` from git directory or

`seread  -D /dev/ttyACM0 -t 2,10 -c word` from pypi install. Supposing,
you have your device on `/dev/ttyACM0`

**If you want to serve as an interace to INFLUXDB (may run already)**
Create a virtual device and run it
`./bin_seread -D /tmp/virtser_connect` . In this case you probably want
to open ports:

-   `-s` for TCP/UDP server on 8099/8100

*see existing decoders lower*

What it does by now - HW
------------------------

-   ORTEC COUNTER (raw numbers, using the `script` file )
-   arduino analog pins A0-An (json going out from arduino)
-   arduino DHT sensor (with json output coded)
-   arduino I2C pressure sensor
-   arduino NTC temperature sensors (preprogrammed)

What it does by now - SW - port 8099
------------------------------------

A space after the word...

-   `influxmevac` - vadim vacuum report
-   `influxme` - send json - e.g.
    -   `echo 'influxme [{"measurement":"cmdline","fields":{"crap":11.1}}]'  | nc 127.0.0.1  8099`
-   `influxmegeo` - gps position
-   `influxmebeam nfs` - generate beamon beamoff image on flashcam
    (mmap)
-   `ptz` - turn raspberry PTZ

Verify what is written in influxdb

``` {.example}
influx
auth
...
use test
show measurements
select * from cmdline
```

Memory map - commands to local flashcam
---------------------------------------

-   `influxmebeam imagename` command sent to 8099 will send as a command
    to flashcam
    -   allowed images: \[\"BEAM~ON~[\", \"BEAM~OFF~\",
        \"DET~RDY~]{.underline}\",\"DET~NRDY~\"\]

SEREAD - details - description
==============================

Installation
------------

The project still develops, changes can be made anytime. The actual
dependencies can be installed by running `./pipall.py`.

The code should be run by `seread`

Basic usage
-----------

### Parameter -t

Usage: `-t 2,60`

Read serial in `Short period` (like 1s or 2s for DHT) and write to TXT
files.

Then every `Long period` (like 60s, 120s) write to influxdb(s).

AND send UDP packets (e.g. to root acquisition running to display
counters - in case of 9009 gregory server). **Deprecated in future**.

``` {.example}
~seread  -D /dev/ttyACM0 -t 2,60 -c word~
```

### Parameter -D or -l

Address the HW device. List devices with `seread`.

Device can be defined by the ttyXXX or by location.

Usage: `-l (location_usb_address)`

`-D /dev/ttyUSBX`

### Parameter -f

Usage: `-f`

Write data (short time interval) to file.

### Parameter -i

Usage: `-i`

Write to influx (long time interval).

Input/Output files
------------------

**INPUT** INP~calib~=\"\~/.seread.calib\" INP~discover~ =
\"\~/.seread~discover8086~\" INP~permanent~ =
\"\~/.seread~permanent8086~\" INP~influxcred~ =
\"\~/.influx~userpassdb~\" INP~udpout~ = \"\~/.seread~udpout~\"
INP~script~ = \"script\"

-   \~/.seread.calib
-   \~/.myservice~discover8086~
-   \~/.myservice~permanent8086~
-   \~/.influx~userpassdb~
-   \~/.sng2~udp~
-   script

**OUTPUT**

-   \~/DATA/serial~NG2udp~.log
-   \~/DATA/serial~NG2jso~.log

**MEMORY MAP**

-   \~/config/flashcam/mmapfile

### seread.calib

**Calibration after readout**

It is possible to make a calibration after reading the serial values in
json. Check the file `~/.seread.calib`

Example:

    {
    "valuea0":{"a":0.21699,"b":-61.111},
    "valuea1":{"a":0.1861328,"b":-40.2}
    }

Pay attention to commas and double quotes. `valuea0` is the same name of
the analog value exctracted from the arduino, `a` `b` are linear
coefficients.

### seread~discover8086~

This contains IP - one per line - of PCs with influxdb running The user,
pass, database is in the file `~/.influx_userpassdb`

### udp~out~

lines with IP:PORT or without PORT, then 8080 is assumed. The will be
UDP packet sent to IP:PORT (every long period)

### script

this runs one line at a time and repeats the last line forever. The
example starts the ORTEC counter.

-   `#EOT:` defines line separator
-   `#WAIT:` defines what seread waits for to complete the line

``` {.example}
#EOT:\r
#WAIT:%
INIT\r\n
SHOW_VERSION\r\n
SET_COUNT_PRESET 0\r\n
SET_DISPLAY 2\r\n
START\r\n
SHOW_COUNT\r

```

Options
-------

-   `-t` two time periods, read,writeinflux: `-t time1,time2`
-   `-i` `-influxyes [true|false]` : send to influx if `-i` is present.
    -   Sending will happen on time2: `-t time1,time2`

More functions: (in construction)
---------------------------------

### 8099 port server

*This is Vadim\'s function*. Information obtained on this port will
store data in influxdb. Vacuum mainly. For the moment, there are several
interpreters:

1.  influxme vac102

    *vac102* is a name of measurement

    `echo 'influxme [{"measurement":"geo","fields":{"longitude":15.0,"latitude":50.0}}]'`

    `for ((i=0;i<10;i++)); do echo 'influxme [{"measurement":"geo","fields":{"longitude":15.0,"latitude":50.$i}}]' ; done`

2.  influxme nfs

    *nfs* is a name of measurement, FL value for FLOW is present as 3rd
    value

3.  influxmegeo

    `echo influxmegeo geo 14.28 49.86 | nc 127.0.0.1  8099`

4.  ptz

    May need to install some stuff: `sudo apt-get install python3-smbus`

    `echo ptz pan +5 | nc 127.0.0.1 8099`
    `echo ptz tilt -5 | nc 127.0.0.1 8099`

5.  influxbeam nfs

                           order                                                        
      -------------- ----- ------- ------------ ---------------------------- ---------- ----------
      influxmebeam   nfs   0002    BEAM~OFF~    [\_\_\_\_\_\_]{.underline}   14:59:40   
      influxmebeam   nfs   0003    BEAM~ON~\_   00                           DGR=00     15:02:46
      influxmebeam   nfs   0004    BEAM~OFF~    [\_\_\_\_\_\_]{.underline}   15:02:50   
      influxmebeam   nfs   0005    DET~RDY~\_   00                           DET=05     15:03:19
      influxmebeam   nfs   0006    DET~NRDY~    [\_\_\_\_\_\_]{.underline}   15:03:23   

    ``` {.example}
    0002 BEAM_OFF _________ 14:59:40
    0003 BEAM_ON_ 00 DGR=00 15:02:46
    0004 BEAM_OFF _________ 15:02:50
    0005 DET_RDY_ 00 DET=05 15:03:19
    0006 DET_NRDY _________ 15:03:23
    ```

APPENDIX
--------

### Adding dialout group to be able to work with USB

`sudo usermod -a -G dialout $USER` then either reboot of logout/login or
try \`newgrp dialout\` in terminal.

### Arduino-mode

1.  Arduino programming remarks

    Different types need different settings in the original IDE.

    -   Chineese NANO
        -   Tools/ArduinoNano/ATmega328P(old)/ttyUSB0
    -   UNO with shield
        -   Tools/ArduinoUNO/\_\_/ACM0 with programmer AVRISM mkII

2.  Straight installer in emacs is fast

    -   go to (<https://github.com/raxod502/straight.el> and prepend

    the code to the `~/.emacs` to use `straight-use-package`

    -   say M-x `straight-use-package` `arduino-mode`
    -   install `auto-minor-mode`
    -   install somehow `arduino-cli` from
        <https://github.com/arduino/arduino-cli>) and
        \[package\](<https://arduino.github.io/arduino-cli/installation/>

3.  emacs setting

    -   copy `arduino-cli.el` file from

    <https://github.com/motform/arduino-cli-mode> to `~/.emacs.d/lisp/`
    and add `(add-to-list 'load-path "~/.emacs.d/lisp/")` and
    `(load "arduino-cli.el")` to `~/.emacs`.

    BUT as now, I cannot compile, as `--fqbn` is needed and not given
    automatically.

    -   IN EMACS say M-x `arduino-cli-mode`

    The `~/.emacs` contents:

    ``` {.commonlisp org-language="lisp"}
    (defvar bootstrap-version)
    (let ((bootstrap-file
           (expand-file-name "straight/repos/straight.el/bootstrap.el" user-emacs-directory))
          (bootstrap-version 5))
      (unless (file-exists-p bootstrap-file)
        (with-current-buffer
            (url-retrieve-synchronously
             "https://raw.githubusercontent.com/raxod502/straight.el/develop/install.el"
             'silent 'inhibit-cookies)
          (goto-char (point-max))
          (eval-print-last-sexp)))
      (load bootstrap-file nil 'nomessage))
    ;;
    ;;
    (straight-use-package 'arduino-mode)
    (add-to-list 'auto-minor-mode-alist '("\\.ino\\'" . arduino-cli-mode))
    ;;
    (add-to-list 'load-path "~/.emacs.d/lisp/")
    (load "arduino-cli.el")

    ```

4.  Arduino-cli commandline

    -   `arduino-cli config init`
    -   `arduino-cli core update-index`
    -   `arduino-cli board list`
    -   `arduino-cli core install arduino:samd`
    -   `arduino-cli core install arduino:avr`
    -   `arduino-cli core list`
    -   `arduino-cli core listall`
    -   `arduino-cli core --fqbn arduino:avr:diecimila  test.ino`

    -   `arduino-cli compile 20200411-logoled-ser1sd0.ino --fqbn arduino:avr:nano`

    and
    `arduino-cli upload --fqbn arduino:avr:nano -i 20200411-logoled-ser1sd0.ino.arduino.avr.nano.hex -p /dev/ttyUSB0`
    should work

### readme in org

Pypi has problems with org, see:
<https://packaging.python.org/specifications/core-metadata/#description-content-type-optional>

### bin~seread~ TESTing behavior:

1.  no paramters:

    **Expected RESULT:**

    -   version
    -   use
    -   MODES
    -   device list
    -   X not exists, advice to virtual socket

2.  -D realDev -t 2,10 -c word

    **Expected RESULT:**

    -   loop entered, check the files
    -   X... NOT FOUND \~/.sng2~udp~

### HTTPS is treated without security check

    #==================== insecure treatment of https is WITHOUT WARNINGS NOW
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
