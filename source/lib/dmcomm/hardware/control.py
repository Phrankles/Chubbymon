# This file is part of the DMComm project by BladeSabre. License: MIT.

from dmcomm import CommandError
from . import WAIT_REPLY
from . import pins

class Controller:
	"""Main class which controls the communication.

	The constructor takes no parameters.
	"""
	def __init__(self):
		self._digirom = None
		self._communicator = None
		self._prong_output = None
		self._prong_input = None
		self._ir_output = None
		self._ir_input_modulated = None
		self._ir_input_raw = None
		self._prong_comm = None
		self._ic_comm = None
		self._modulated_comm = None
		self._barcode_comm = None
	def register(self, io_object) -> None:
		"""Registers pins for a particular type of input or output.

		Each type should only be provided once.

		:param io_object: One of the `Input` or `Output` types provided.
		"""
		if isinstance(io_object, pins.ProngOutput):
			self._prong_output = io_object
		if isinstance(io_object, pins.ProngInput):
			self._prong_input = io_object
		if isinstance(io_object, pins.InfraredOutput):
			self._ir_output = io_object
		if isinstance(io_object, pins.InfraredInputModulated):
			self._ir_input_modulated = io_object
		if isinstance(io_object, pins.InfraredInputRaw):
			self._ir_input_raw = io_object
		if self._prong_comm is None and self._prong_output is not None and self._prong_input is not None:
			from . import prongs
			self._prong_comm = prongs.ProngCommunicator(self._prong_output, self._prong_input)
		if self._ic_comm is None and self._ir_output is not None and self._ir_input_raw is not None:
			from . import ic
			self._ic_comm = ic.iC_Communicator(self._ir_output, self._ir_input_raw)
		if self._modulated_comm is None and self._ir_output is not None and self._ir_input_modulated is not None:
			from . import modulated
			self._modulated_comm = modulated.ModulatedCommunicator(self._ir_output, self._ir_input_modulated)
		if self._barcode_comm is None and self._ir_output is not None:
			from . import barcode
			self._barcode_comm = barcode.BarcodeCommunicator(self._ir_output)
	def execute(self, digirom) -> None:
		"""Carries out the communication specified.

		:param digirom: The DigiROM to execute.
		:raises CommandError: If the required pins for the selected physical protocol are not registered.
		:raises ReceiveError: If a broken transmission was received.
		"""
		self._digirom = digirom
		try:
			self._prepare()
			if digirom.turn in [0, 2]:
				if not self._received(5000):
					return
			if digirom.turn == 0:
				while True:
					if not self._received(WAIT_REPLY):
						return
			else:
				while True:
					data_to_send = self._digirom.send()
					if data_to_send is None:
						return
					self._communicator.send(data_to_send)
					if not self._received(WAIT_REPLY):
						return
		finally:
			self._disable()
			self._digirom = None
	def _prepare(self):
		"""Prepares for a single interaction.
		"""
		protocol = self._digirom.physical
		self._disable()
		if protocol in ["V", "X", "Y"]:
			if self._prong_output is None:
				raise CommandError("no prong output registered")
			if self._prong_input is None:
				raise CommandError("no prong input registered")
			self._communicator = self._prong_comm
		elif protocol == "!IC":
			if self._ir_output is None:
				raise CommandError("no infrared output registered")
			if self._ir_input_raw is None:
				raise CommandError("no raw infrared input registered")
			self._communicator = self._ic_comm
		elif protocol in ["!DL", "!FL"]:
			if self._ir_output is None:
				raise CommandError("no infrared output registered")
			if self._ir_input_modulated is None:
				raise CommandError("no modulated infrared input registered")
			self._communicator = self._modulated_comm
		elif protocol in ["!BC"]:
			if self._ir_output is None:
				raise CommandError("no infrared output registered")
			self._communicator = self._barcode_comm
		else:
			raise CommandError("protocol=" + protocol)
		self._communicator.enable(protocol)
		self._digirom.prepare()
	def _received(self, timeout_ms):
		received_data = self._communicator.receive(timeout_ms)
		self._digirom.receive(received_data)
		if received_data is None or received_data == []:
			return False
		return True
	def _disable(self):
		if self._communicator is not None:
			self._communicator.disable()
			self._communicator = None
