import asyncio

from .LPF_Device import LPF_Device, Devtype
from ..Decoder import Decoder

class AngularSmall(LPF_Device):

	def __init__(self, port=-1):
		super().__init__(port)

		self.devtype = Devtype.LPF

		self.port_id = 0x41
		self.name = Decoder.io_type_id_str[self.port_id]
							# Identifier for the type of device attached
							# Index into Decoder.io_type_id_str

		self.mode_subs = {
			# mode_number: [ delta_interval, subscribe_boolean, Mode Information Name (Section 3.20.1), tuple of generated messages when subscribed to this mode ]
			0: [ self.delta_interval, False, 'POWER', ()],
			1: [ self.delta_interval, False, 'SPEED', ()],
			2: [ self.delta_interval, False, 'POS', ()],
			3: [ self.delta_interval, False, 'APOS', ()]
		}
