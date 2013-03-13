"""A collection of functions for programming the adafruit ultimate GPS

Complete command reference is here:
    http://www.adafruit.com/datasheets/PMTK_A08.pdf
"""
import serial

ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

class NmeaSentences(object):
    """An enumeration of legal NMEA sentences.

    Learn more about NMEA sentences here:
        http://aprs.gids.nl/nmea/

    These values are actually integer intervals. 0 disables things. A 1
    would set the interval to every 1 second. 5 means send that sentence
    every 5 seconds.
    """

    def __init__(self):
        self.gll = 0
        self.rmc = 0
        self.vtg = 0
        self.gga = 0
        self.gsa = 0
        self.gsv = 0


def run_cmd(cmd):
    ser.flushOutput()
    ser.flushInput()
    checksum = 0
    for c in cmd:
        checksum ^= ord(c)
    checksum = hex(checksum)[2:]

    cmd_line = '\r\n$%s*%s\r\n' % (cmd, checksum)
    ser.write(cmd_line)
    for i in range(15):
        line = ser.readline()
        if line.startswith('$PM'):
            return True
            break
    else:
        return False


def set_nmea_output(desired_sentences):
    cmd_string = 'PMTK314,%(gll)d,%(rmc)d,%(vtg)d,%(gga)d,%(gsa)d,%(gsv)d,' \
                 '0,0,0,0,0,0,0,0,0,0,0,0,0' % desired_sentences.__dict__
    if not run_cmd(cmd_string):
        print 'Failed to get reply for set_nmea_output'


def enable_waas():
    if not run_cmd('PMTK313,1'):
        print 'Failed to set SBAS'
    if not run_cmd('PMTK301,2'):
        print 'Failed to enable WAAS'


def send_test_packet():
    print ser.write('\r\n$PMTK000*32\r\n')

desired_sentences = NmeaSentences()
desired_sentences.rmc = 1
set_nmea_output(desired_sentences)

enable_waas()

