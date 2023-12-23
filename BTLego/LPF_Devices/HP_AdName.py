import asyncio

from .LPF_Device import LPF_Device, Devtype
from .Hub_Property import Hub_Property
from ..Decoder import Decoder

# Not actually SURE about the built-in devices fitting into the LPF2 model but whatever
class AdName(Hub_Property):

	def __init__(self, port=-1):
		# Port number the device is attached to on the BLE Device

		self.devtype = Devtype.PROPERTY
		self.name = 'Advertising Name'
		self.port = Decoder.hub_property_ints[self.name]
		self.port_id = 0x0	# Identifier for the type of device attached
							# Index into Decoder.io_type_id_str
		self.status = 0x1	# Decoder.io_event_type_str[0x1]
		self.delta_interval = 0

		self.generated_message_types = (
			'info',
		)

		self.mode_subs = {
			# mode_number: ( delta_interval, subscribe_boolean ) or None
			0: (0, False)
		}

	def get_message(self, bt_message):
		if self.mode_subs[0][1]:
			return ('info','ad_name',bt_message['value'])
		return None

		# Don't need to index by self.device_ports[port_id] anymore?
		# Index: Port Type per Decoder.io_type_id_str index, value: attached hardware port identifier (int or tuple)

	def PIFSetup_data_for_message_type(self, message_type):
		if message_type == 'info':
			return True

		# FIXME: What should properties be returning here, then?

		# return 4-item array [port, mode, delta interval, subscribe on/off]
		# Base class returns nothing
		# FIXME: use abc
		return None

	def set_subscribe(self, message_type, should_subscribe):
		if message_type == 'info':
			# Ignore the delta, doesn't matter for hub properties
			self.mode_subs[0] = ( 0 , should_subscribe)
		else:
			return False
		return True

	def send_message(self, message):
		# ( action, (parameters,) )
		action = message[0]
		parameters = message[1]

		if action == 'get_ad_name':
			name_update_bytes = bytearray([
				0x05,	# len
				0x00,	# padding but maybe stuff in the future (:
				0x1,	# 'hub_properties'
				self.port,	# 'Advertising Name'
				0x5		# 'Request Update'
			])

			name_update_bytes[0] = len(name_update_bytes)
			ret_message = { 'gatt_send': (name_update_bytes,) }
			return ret_message

		return None