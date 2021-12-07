# This file is part of the DMComm project by BladeSabre. License: MIT.

import board
import digitalio
import time
import usb_cdc

from dmcomm import CommandError, ReceiveError
import dmcomm.hardware as hw
import dmcomm.protocol

class Comm:
    def __init__(self,monster):
        #self.pins_extra_power = [board.GP11, board.GP13, board.GP18]
        #self.outputs_extra_power = []
        #for pin in self.pins_extra_power:
        #    self.output = digitalio.DigitalInOut(pin)
        #    self.output.direction = digitalio.Direction.OUTPUT
        #    self.output.value = True
        #    self.outputs_extra_power.append(output)

        self.controller = hw.Controller()
        self.controller.register(hw.ProngOutput(board.GP19, board.GP21))
        self.controller.register(hw.ProngInput(board.GP26))
        self.controller.register(hw.InfraredOutput(board.GP16))
        self.controller.register(hw.InfraredInputModulated(board.GP17))
        self.controller.register(hw.InfraredInputRaw(board.GP14))
        #self.usb_cdc.console.timeout = 1
        self.digirom = None

    def execute(self,digirom):
        serial_str = digirom.strip()
        print("got %d bytes: %s -> " % (len(serial_str), serial_str), end="")
        try:
            command = dmcomm.protocol.parse_command(serial_str)
            if hasattr(command, "op"):
                # It's an OtherCommand
                raise NotImplementedError("op=" + command.op)
            self.digirom = command
            print(f"{self.digirom.physical}{self.digirom.turn}-[{len(self.digirom)} packets]")
        except (CommandError, NotImplementedError) as e:
            print(repr(e))
        time.sleep(1)
        if self.digirom is not None:
            error = ""
            result_end = "\n"
            try:
                self.controller.execute(self.digirom)
            except (CommandError, ReceiveError) as e:
                error = repr(e)
                result_end = " "
            print(self.digirom.result, end=result_end)
            if error != "":
                print(error)
        #seconds_passed = time.monotonic() - time_start
        #if seconds_passed < 5:
        #    time.sleep(5 - seconds_passed)
