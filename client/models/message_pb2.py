# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: message.proto
# Protobuf Python Version: 5.29.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    1,
    '',
    'message.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rmessage.proto\x12\x15sistemas_distribuidos\"Y\n\x07Message\x12\x35\n\x04type\x18\x01 \x01(\x0e\x32\".sistemas_distribuidos.MessageTypeH\x00\x88\x01\x01\x12\x0e\n\x06params\x18\x02 \x03(\x05\x42\x07\n\x05_type\"l\n\x10\x46orwardedMessage\x12\x0f\n\x02id\x18\x01 \x01(\x05H\x00\x88\x01\x01\x12\x34\n\x07\x63ontent\x18\x02 \x01(\x0b\x32\x1e.sistemas_distribuidos.MessageH\x01\x88\x01\x01\x42\x05\n\x03_idB\n\n\x08_content*\xe2\x02\n\x0bMessageType\x12\x14\n\x10\x44\x45VICE_DISCOVERY\x10\x00\x12\x13\n\x0fREGISTER_DEVICE\x10\x01\x12\x0b\n\x07TURN_ON\x10\x02\x12\x0c\n\x08TURN_OFF\x10\x03\x12\x16\n\x12\x43HANGE_TEMPERATURE\x10\x04\x12\x14\n\x10TEMPERATURE_INFO\x10\x05\x12\x10\n\x0c\x43HANGE_COLOR\x10\x06\x12\x14\n\x10\x43HANGE_INTENSITY\x10\x07\x12\x11\n\rCHANGE_VOLUME\x10\x08\x12\x15\n\x11TURN_ON_BLUETOOTH\x10\t\x12\x16\n\x12TURN_OFF_BLUETOOTH\x10\n\x12\x12\n\x0e\x43HANGE_CHANNEL\x10\x0b\x12\x1b\n\x17TURN_ON_LED_VOLUME_SYNC\x10\x0c\x12\x1c\n\x18TURN_OFF_LED_VOLUME_SYNC\x10\r\x12\x08\n\x04LOCK\x10\x0e\x12\n\n\x06UNLOCK\x10\x0f\x12\x10\n\x0c\x43HANGE_MUSIC\x10\x10*z\n\nDeviceType\x12\x14\n\x10\x41IR_CONDITIONING\x10\x00\x12\x0b\n\x07\x41\x42\x41JOUR\x10\x01\x12\x14\n\x10\x41RTIFICIAL_LIGHT\x10\x02\x12\n\n\x06\x41\x42\x41JUR\x10\x03\x12\r\n\tSOUND_BOX\x10\x04\x12\x0e\n\nTELEVISION\x10\x05\x12\x08\n\x04\x44OOR\x10\x06\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'message_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_MESSAGETYPE']._serialized_start=242
  _globals['_MESSAGETYPE']._serialized_end=596
  _globals['_DEVICETYPE']._serialized_start=598
  _globals['_DEVICETYPE']._serialized_end=720
  _globals['_MESSAGE']._serialized_start=40
  _globals['_MESSAGE']._serialized_end=129
  _globals['_FORWARDEDMESSAGE']._serialized_start=131
  _globals['_FORWARDEDMESSAGE']._serialized_end=239
# @@protoc_insertion_point(module_scope)