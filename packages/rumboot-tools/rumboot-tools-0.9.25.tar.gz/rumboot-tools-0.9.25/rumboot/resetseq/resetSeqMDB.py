import os
import time
import usb.core
import pygpiotools
import usb.util
from parse import parse
from rumboot.resetseq.resetSeqBase import base
from serial import Serial

class mdb(base):
    name = "Malina Debug Bridge"
    swap   = False
    supported = ["POWER", "RESET", "HOST", "EDCL_LOCK"]

    def __init__(self, terminal, opts):
        port = os.path.realpath(terminal.ser._port)
        self.ctlport = opts["mdb_ctl_port"]
        if self.ctlport is None:
            id = parse("/dev/ttyACM{:d}", port)[0]
            id += 1
            self.ctlport = f"/dev/ttyACM{id}"
        self.serial = Serial(self.ctlport, 115200)        
        super().__init__(terminal, opts)
        self["EDCL_LOCK"] = 0
        self["HOST"] = 0

    def __setitem__(self, key, value):
        super().__setitem__(key, value)

        if "HOST" in self._states and "EDCL_LOCK" in self._states:
            self.serial.write(f"bootm {self._states['HOST']} {self._states['EDCL_LOCK']}\r\n".encode())
        if "RESET" in self._states:
            self.serial.write(f"rst {1 - self._states['RESET']}\r\n".encode())



    def get_options(self):
        return {
                "mdb-ctl-port" : {
                    "help" : "Malina Debug Bridge port",
                    "default" : None,
                },
            }