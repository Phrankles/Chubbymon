# This file is part of the DMComm project by BladeSabre. License: MIT.

import array
import pulseio

from dmcomm import CommandError, ReceiveError
from . import WAIT_REPLY
from . import misc

class ModulatedCommunicator:
	def __init__(self, ir_output, ir_input_modulated):
		self._pin_output = ir_output.pin_output
		self._pin_input = ir_input_modulated.pin_input
		self._output_pulses = None
		self._input_pulses = None
		self._params = ModulatedParams()
		self._enabled = False
	def enable(self, protocol):
		self.disable()
		self._params.set_protocol(protocol)
		try:
			self._output_pulses = pulseio.PulseOut(self._pin_output, frequency=38000, duty_cycle=0x8000)
			self._input_pulses = pulseio.PulseIn(self._pin_input, maxlen=300, idle_state=True)
			self._input_pulses.pause()
		except:
			self.disable()
			raise
		self._enabled = True
	def disable(self):
		for item in [self._output_pulses, self._input_pulses]:
			if item is not None:
				item.deinit()
		self._ouput_pulses = None
		self._input_pulses = None
		self._enabled = False
	def reset(self):
		pass
	def send(self, bytes_to_send):
		if not self._enabled:
			raise RuntimeError("not enabled")
		num_durations = len(bytes_to_send) * 16 + 4
		array_to_send = array.array("H")
		for i in range(num_durations):
			array_to_send.append(0)
			#This function would be simpler if we append as we go along,
			#but still hoping for a fix that allows reuse of the array.
		array_to_send[0] = self._params.start_pulse_send
		array_to_send[1] = self._params.start_gap_send
		buf_cursor = 2
		for current_byte in bytes_to_send:
			for j in range(8):
				array_to_send[buf_cursor] = self._params.bit_pulse_send
				buf_cursor += 1
				if current_byte & 1:
					array_to_send[buf_cursor] = self._params.bit_gap_send_long
				else:
					array_to_send[buf_cursor] = self._params.bit_gap_send_short
				buf_cursor += 1
				current_byte >>= 1
		array_to_send[buf_cursor] = self._params.stop_pulse_send
		array_to_send[buf_cursor + 1] = self._params.stop_gap_send
		self._output_pulses.send(array_to_send)
	def receive(self, timeout_ms):
		if not self._enabled:
			raise RuntimeError("not enabled")
		pulses = self._input_pulses
		pulses.clear()
		pulses.resume()
		if timeout_ms == WAIT_REPLY:
			timeout_ms = self._params.reply_timeout_ms
		misc.wait_for_length_no_more(pulses, timeout_ms,
			self._params.packet_length_timeout_ms, self._params.packet_continue_timeout_ms)
		pulses.pause()
		if len(pulses) == 0:
			return []
		bytes_received = []
		t = misc.pop_pulse(pulses, -2)
		if t < self._params.start_pulse_min or t > self._params.start_pulse_max:
			raise ReceiveError("start pulse = %d" % t)
		t = misc.pop_pulse(pulses, -1)
		if t < self._params.start_gap_min or t > self._params.start_gap_max:
			raise ReceiveError("start gap = %d" % t)
		current_byte = 0
		bit_count = 0
		while True:
			t = misc.pop_pulse(pulses, 2*bit_count+1)
			if t >= self._params.bit_pulse_min and t <= self._params.bit_pulse_max:
				#normal pulse
				pass
			elif t >= self._params.stop_pulse_min and t <= self._params.stop_pulse_max:
				#stop pulse
				break
			else:
				raise ReceiveError("bit %d pulse = %d" % (bit_count, t))
			t = misc.pop_pulse(pulses, 2*bit_count+2)
			if t < self._params.bit_gap_min or t > self._params.bit_gap_max:
				raise ReceiveError("bit %d gap = %d" % (bit_count, t))
			current_byte >>= 1
			if t > self._params.bit_gap_threshold:
				current_byte |= 0x80
			bit_count += 1
			if bit_count % 8 == 0:
				bytes_received.append(current_byte)
				current_byte = 0
		if bit_count % 8 != 0:
			raise ReceiveError("bit_count = %d" % bit_count)
		return bytes_received

class ModulatedParams:
	def __init__(self):
		self.set_protocol("!DL")
	def set_protocol(self, protocol):
		if protocol == "!DL":
			self.start_pulse_min = 9000
			self.start_pulse_send = 9800
			self.start_pulse_max = 11000
			self.start_gap_min = 2000
			self.start_gap_send = 2450
			self.start_gap_max = 3000
			self.bit_pulse_min = 300
			self.bit_pulse_send = 500
			self.bit_pulse_max = 650
			self.bit_gap_min = 300
			self.bit_gap_send_short = 700
			self.bit_gap_threshold = 800
			self.bit_gap_send_long = 1300
			self.bit_gap_max = 1500
			self.stop_pulse_min = 1000
			self.stop_pulse_send = 1300
			self.stop_pulse_max = 1400
			self.stop_gap_send = 400
			self.reply_timeout_ms = 40
			self.packet_length_timeout_ms = 300
			self.packet_continue_timeout_ms = 10
		elif protocol == "!FL":
			self.start_pulse_min = 5000
			self.start_pulse_send = 5880
			self.start_pulse_max = 7000
			self.start_gap_min = 3000
			self.start_gap_send = 3872
			self.start_gap_max = 4000
			self.bit_pulse_min = 250
			self.bit_pulse_send = 480
			self.bit_pulse_max = 600
			self.bit_gap_min = 200
			self.bit_gap_send_short = 480
			self.bit_gap_threshold = 650
			self.bit_gap_send_long = 1450
			self.bit_gap_max = 1600
			self.stop_pulse_min = 700
			self.stop_pulse_send = 950
			self.stop_pulse_max = 1100
			self.stop_gap_send = 1500
			self.reply_timeout_ms = 100
			self.packet_length_timeout_ms = 300
			self.packet_continue_timeout_ms = 10
		else:
			raise ValueError("protocol must be !DL/!FL")
		self.protocol = protocol
