# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: training_chunk.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='training_chunk.proto',
  package='protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x14training_chunk.proto\x12\x06protos\"1\n\x0bPolicyChunk\x12\x12\n\nmove_index\x18\x01 \x02(\r\x12\x0e\n\x06weight\x18\x02 \x02(\r\"D\n\rPositionChunk\x12\x0e\n\x06planes\x18\x03 \x03(\x04\x12#\n\x06policy\x18\x04 \x03(\x0b\x32\x13.protos.PolicyChunk\"\x91\x02\n\tGameChunk\x12=\n\x0fpolicy_encoding\x18\x01 \x02(\x0e\x32$.protos.GameChunk.PolicyEncodingType\x12;\n\x0e\x62oard_encoding\x18\x02 \x02(\x0e\x32#.protos.GameChunk.BoardEncodingType\x12(\n\tpositions\x18\x03 \x03(\x0b\x32\x15.protos.PositionChunk\x12\x0e\n\x06result\x18\x04 \x02(\x01\"\'\n\x12PolicyEncodingType\x12\x11\n\rSIMPLE_POLICY\x10\x00\"%\n\x11\x42oardEncodingType\x12\x10\n\x0cSIMPLE_BOARD\x10\x00'
)



_GAMECHUNK_POLICYENCODINGTYPE = _descriptor.EnumDescriptor(
  name='PolicyEncodingType',
  full_name='protos.GameChunk.PolicyEncodingType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SIMPLE_POLICY', index=0, number=0,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=349,
  serialized_end=388,
)
_sym_db.RegisterEnumDescriptor(_GAMECHUNK_POLICYENCODINGTYPE)

_GAMECHUNK_BOARDENCODINGTYPE = _descriptor.EnumDescriptor(
  name='BoardEncodingType',
  full_name='protos.GameChunk.BoardEncodingType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SIMPLE_BOARD', index=0, number=0,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=390,
  serialized_end=427,
)
_sym_db.RegisterEnumDescriptor(_GAMECHUNK_BOARDENCODINGTYPE)


_POLICYCHUNK = _descriptor.Descriptor(
  name='PolicyChunk',
  full_name='protos.PolicyChunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='move_index', full_name='protos.PolicyChunk.move_index', index=0,
      number=1, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='weight', full_name='protos.PolicyChunk.weight', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=32,
  serialized_end=81,
)


_POSITIONCHUNK = _descriptor.Descriptor(
  name='PositionChunk',
  full_name='protos.PositionChunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='planes', full_name='protos.PositionChunk.planes', index=0,
      number=3, type=4, cpp_type=4, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='policy', full_name='protos.PositionChunk.policy', index=1,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=83,
  serialized_end=151,
)


_GAMECHUNK = _descriptor.Descriptor(
  name='GameChunk',
  full_name='protos.GameChunk',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='policy_encoding', full_name='protos.GameChunk.policy_encoding', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='board_encoding', full_name='protos.GameChunk.board_encoding', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='positions', full_name='protos.GameChunk.positions', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='protos.GameChunk.result', index=3,
      number=4, type=1, cpp_type=5, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _GAMECHUNK_POLICYENCODINGTYPE,
    _GAMECHUNK_BOARDENCODINGTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=154,
  serialized_end=427,
)

_POSITIONCHUNK.fields_by_name['policy'].message_type = _POLICYCHUNK
_GAMECHUNK.fields_by_name['policy_encoding'].enum_type = _GAMECHUNK_POLICYENCODINGTYPE
_GAMECHUNK.fields_by_name['board_encoding'].enum_type = _GAMECHUNK_BOARDENCODINGTYPE
_GAMECHUNK.fields_by_name['positions'].message_type = _POSITIONCHUNK
_GAMECHUNK_POLICYENCODINGTYPE.containing_type = _GAMECHUNK
_GAMECHUNK_BOARDENCODINGTYPE.containing_type = _GAMECHUNK
DESCRIPTOR.message_types_by_name['PolicyChunk'] = _POLICYCHUNK
DESCRIPTOR.message_types_by_name['PositionChunk'] = _POSITIONCHUNK
DESCRIPTOR.message_types_by_name['GameChunk'] = _GAMECHUNK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PolicyChunk = _reflection.GeneratedProtocolMessageType('PolicyChunk', (_message.Message,), {
  'DESCRIPTOR' : _POLICYCHUNK,
  '__module__' : 'training_chunk_pb2'
  # @@protoc_insertion_point(class_scope:protos.PolicyChunk)
  })
_sym_db.RegisterMessage(PolicyChunk)

PositionChunk = _reflection.GeneratedProtocolMessageType('PositionChunk', (_message.Message,), {
  'DESCRIPTOR' : _POSITIONCHUNK,
  '__module__' : 'training_chunk_pb2'
  # @@protoc_insertion_point(class_scope:protos.PositionChunk)
  })
_sym_db.RegisterMessage(PositionChunk)

GameChunk = _reflection.GeneratedProtocolMessageType('GameChunk', (_message.Message,), {
  'DESCRIPTOR' : _GAMECHUNK,
  '__module__' : 'training_chunk_pb2'
  # @@protoc_insertion_point(class_scope:protos.GameChunk)
  })
_sym_db.RegisterMessage(GameChunk)


# @@protoc_insertion_point(module_scope)
