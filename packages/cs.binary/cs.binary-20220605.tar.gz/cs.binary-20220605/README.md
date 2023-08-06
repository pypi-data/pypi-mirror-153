Facilities associated with binary data parsing and transcription.
The classes in this module support easy parsing of binary data
structures,
returning instances with the binary data decoded into attributes
and capable of transcribing themselves in binary form
(trivially via `bytes(instance)` and also otherwise).

*Latest release 20220605*:
BinaryMixin: replace scan_file with scan_fspath, as the former left uncertainty about the amount of the file consumed.

Note: this module requires Python 3.6+ because various default
behaviours rely on `dict`s preserving their insert order.

See `cs.iso14496` for an ISO 14496 (eg MPEG4) parser
built using this module.

**Deprecation**: the `Packet` and `PacketField` classes
were unnecessarily hard to use and are deprecated
in favour of the `Binary`* suite of classes and factories.
All the *`Field` classes and other subclasses
derived from `Packet` and `PacketField` are also deprecated.

Terminology used below:
* buffer:
  an instance of `cs.buffer.CornuCopyBuffer`,
  which presents an iterable of bytes-like values
  via various useful methods;
  it also has a few factory methods to make one from a variety of sources
  such as bytes, iterables, binary files, `mmap`ped files,
  TCP data streams, etc.
* chunk:
  a piece of binary data obeying the buffer protocol,
  almost always a `bytes` instance or a `memoryview`,
  but in principle also things like `bytearray`.

There are 5 main classes on which an implementor should base their data structures:
* `BinarySingleStruct`: a factory for classes based
  on a `struct.struct` format string with a single value;
  this builds a `namedtuple` subclass
* `BinaryMultiStruct`: a factory for classes based
  on a `struct.struct` format string with multiple values;
  this also builds a `namedtuple` subclass
* `BinarySingleValue`: a base class for subclasses
  parsing and transcribing a single value
* `BinaryMultiValue`: a base class for subclasses
  parsing and transcribing multiple values
  with no variation
* `SimpleBinary`: a base class for subclasses
  with custom `.parse` and `.transcribe` methods,
  for structures with variable fields

All the classes derived from the above inherit all the methods
of `BinaryMixin`.
Amongst other things, this means that the binary transcription
can be had simply from `bytes(instance)`,
although there are more transcription methods provided
for when greater flexibility is desired.
It also means that all classes have `parse`* and `scan`* methods
for parsing binary data streams.

You can also instantiate objects directly;
there's no requirement for the source information to be binary.

There are several presupplied subclasses for common basic types
such as `UInt32BE` (an unsigned 32 bit big endian integer).

## Class `AbstractBinary(BinaryMixin)`

Abstract class for all `Binary`* implementations,
specifying the `parse` and `transcribe` methods
and providing the methods from `BinaryMixin`.

*Method `AbstractBinary.parse(bfr)`*:
Parse an instance of `cls` from the buffer `bfr`.

*Method `AbstractBinary.transcribe(self)`*:
Return or yield `bytes`, ASCII string, `None` or iterables
comprising the binary form of this instance.

This aims for maximum convenience
when transcribing a data structure.

This may be implemented as a generator, yielding parts of the structure.

This may be implemented as a normal function, returning:
* `None`: no bytes of data,
  for example for an omitted or empty structure
* a `bytes`-like object: the full data bytes for the structure
* an ASCII compatible string:
  this will be encoded with the `'ascii'` encoding to make `bytes`
* an iterable:
  the components of the structure,
  including substranscriptions which themselves
  adhere to this protocol - they may be `None`, `bytes`-like objects,
  ASCII compatible strings or iterables.
  This supports directly returning or yielding the result of a field's
  `.transcribe` method.

## Class `BinaryByteses(AbstractBinary, BinaryMixin)`

A list of `bytes` parsed directly from the native iteration of the buffer.

## Function `BinaryFixedBytes(class_name, length: int)`

Factory for an `AbstractBinary` subclass matching `length` bytes of data.
The bytes are saved as the attribute `.data`.

## Class `BinaryListValues(AbstractBinary, BinaryMixin)`

A list of values with a common parse specification,
such as sample or Boxes in an ISO14496 Box structure.

*Method `BinaryListValues.parse(bfr, count=None, *, end_offset=None, min_count=None, max_count=None, pt)`*:
Read values from `bfr`.
Return a `BinaryListValue` containing the values.

Parameters:
* `count`: optional count of values to read;
  if specified, exactly this many values are expected.
* `end_offset`: an optional bounding end offset of the buffer.
* `min_count`: the least acceptable number of values.
* `max_count`: the most acceptable number of values.
* `pt`: a parse/transcribe specification
  as accepted by the `pt_spec()` factory.
  The values will be returned by its parse function.

*Method `BinaryListValues.transcribe(self)`*:
Transcribe all the values.

## Class `BinaryMixin`

Presupplied helper methods for binary objects.

*Method `BinaryMixin.__bytes__(self)`*:
The binary transcription as a single `bytes` object.

*Method `BinaryMixin.__len__(self)`*:
Compute the length by running a transcription and measuring it.

*Method `BinaryMixin.from_bytes(bs, **kw)`*:
Factory to parse an instance from the
bytes `bs` starting at `offset`.
Returns the new instance.

Raises `ValueError` if `bs` is not entirely consumed.
Raises `EOFError` if `bs` has insufficient data.

Keyword parameters are passed to the `.parse_bytes` method.

This relies on the `cls.parse` method for the parse.

*Method `BinaryMixin.parse_bytes(bs, offset=0, length=None, **kw)`*:
Factory to parse an instance from the
bytes `bs` starting at `offset`.
Returns `(instance,offset)` being the new instance and the post offset.

Raises `EOFError` if `bs` has insufficient data.

The parameters `offset` and `length` are passed to the
`CornuCopyBuffer.from_bytes` factory.

Other keyword parameters are passed to the `.parse` method.

This relies on the `cls.parse` method for the parse.

*Method `BinaryMixin.scan(bfr, count=None, min_count=None, max_count=None)`*:
Function to scan the buffer `bfr` for repeated instances of `cls`
until end of input and yield them.

Parameters:
* `bfr`: the buffer to scan
* `count`: the required number of instances to scan,
  equivalent to setting `min_count=count` and `max_count=count`
* `min_count`: the minimum number of instances to scan
* `max_count`: the maximum number of instances to scan
It is in error to specify both `count` and one of `min_count` or `max_count`.

Scanning stops after `max_count` instances (if specified).
If fewer than `min_count` instances (if specified) are scanned
a warning is issued.
This is to accomodate nonconformant streams
without raising exceptions.
Callers wanting to validate `max_count` may want to probe `bfr.at_eof()`
after return.
Callers not wanting a warning over `min_count` should not specify it,
and instead check the number of instances returned themselves.

*Method `BinaryMixin.scan_fspath(fspath: str, *, with_offsets=False, **kw)`*:
Open the file with filesystenm path `fspath` for read
and yield from `self.scan(..,**kw)` or
`self.scan_with_offsets(..,**kw)` according to the
`with_offsets` parameter.

Parameters:
* `fspath`: the filesystem path of the file to scan
* `with_offsets`: optional flag, default `False`;
  if true then scan with `scan_with_offsets` instead of
  with `scan`
Other keyword parameters are passed to `scan` or
`scan_with_offsets`.

*Method `BinaryMixin.scan_with_offsets(bfr, count=None, min_count=None, max_count=None)`*:
Wrapper for `scan()` which yields (pre_offset,instance,post_offset)`
indicating the start and end offsets of the yielded instances.
All parameters are as for `scan()`.

*Method `BinaryMixin.self_check(self, *a, **kw)`*:
Internal self check. Returns `True` if passed.

If the structure has a `FIELD_TYPES` attribute, normally a
class attribute, then check the fields against it. The
`FIELD_TYPES` attribute is a mapping of `field_name` to
a specification of `required` and `types`. The specification
may take one of 2 forms:
* a tuple of `(required,types)`
* a single `type`; this is equivalent to `(True,(type,))`
Their meanings are as follows:
* `required`: a Boolean. If true, the field must be present
  in the packet `field_map`, otherwise it need not be present.
* `types`: a tuple of acceptable field types

There are some special semantics involved here.

An implementation of a structure may choose to make some
fields plain instance attributes instead of binary objects
in the `field_map` mapping, particularly variable structures
such as a `cs.iso14496.BoxHeader`, whose `.length` may be parsed
directly from its binary form or computed from other fields
depending on the `box_size` value. Therefore, checking for
a field is first done via the `field_map` mapping, then by
`getattr`, and as such the acceptable `types` may include
nonstructure types such as `int`.

Here is the `BoxHeader.FIELD_TYPES` definition as an example:

    FIELD_TYPES = {
      'box_size': UInt32BE,
      'box_type': BytesField,
      'length': (
          True,
          (
              type(Ellipsis),
              UInt64BE,
              UInt32BE,
              int
          ),
      ),
    }

Note that `length` includes some nonstructure types,
and that it is written as a tuple of `(True,types)` because
it has more than one acceptable type.

*Method `BinaryMixin.transcribe_flat(self)`*:
Return a flat iterable of chunks transcribing this field.

*Method `BinaryMixin.transcribed_length(self)`*:
Compute the length by running a transcription and measuring it.

## Function `BinaryMultiStruct(class_name: str, struct_format: str, field_names: str)`

A class factory for `AbstractBinary` `namedtuple` subclasses
built around complex `struct` formats.

Parameters:
* `class_name`: name for the generated class
* `struct_format`: the `struct` format string
* `field_names`: field name list,
  a space separated string or an interable of strings

## Function `BinaryMultiValue(class_name, field_map, field_order=None)`

Construct a `SimpleBinary` subclass named `class_name`
whose fields are specified by the mapping `field_map`.

The `field_map` is a mapping of field name to buffer parsers and transcribers.

*Note*:
if `field_order` is not specified
it is constructed by iterating over `field_map`.
Prior to Python 3.6, `dict`s do not provide a reliable order
and should be accompanied by an explicit `field_order`.
From 3.6 onward a `dict` is enough and its insertion order
will dictate the default `field_order`.

For a fixed record structure
the default `.parse` and `.transcribe` methods will suffice;
they parse or transcribe each field in turn.
Subclasses with variable records should override
the `.parse` and `.transcribe` methods
accordingly.

The `field_map` is a mapping of field name
to a class returned by the `pt_spec()` function.

If the class has both `parse_value` and `transcribe_value` methods
then the value itself will be directly stored.
Otherwise the class it presumed to be more complex subclass
of `AbstractBinary` and the instance is stored.

Here is an example exhibiting various ways of defining each field:
* `n1`: defined with the *`_value` methods of `UInt8`,
  which return or transcribe the `int` from an unsigned 8 bit value;
  this stores a `BinarySingleValue` whose `.value` is an `int`
* `n2`: defined from the `UInt8` class,
  which parses an unsigned 8 bit value;
  this stores an `UInt8` instance
  (also a `BinarySingleValue` whole `.value` is an `int`)
* `n3`: like `n2`
* `data1`: defined with the *`_value` methods of `BSData`,
  which return or transcribe the data `bytes`
  from a run length encoded data chunk;
  this stores a `BinarySingleValue` whose `.value` is a `bytes`
* `data2`: defined from the `BSData` class
  which parses a run length encoded data chunk;
  this is a `BinarySingleValue` so we store its `bytes` value directly.

    >>> class BMV(BinaryMultiValue("BMV", {
    ...         'n1': (UInt8.parse_value, UInt8.transcribe_value),
    ...         'n2': UInt8,
    ...         'n3': UInt8,
    ...         'nd': ('>H4s', 'short bs'),
    ...         'data1': (
    ...             BSData.parse_value,
    ...             BSData.transcribe_value,
    ...         ),
    ...         'data2': BSData,
    ... })):
    ...     pass
    >>> BMV.FIELD_ORDER
    ['n1', 'n2', 'n3', 'nd', 'data1', 'data2']
    >>> bmv = BMV.from_bytes(b'\x11\x22\x77\x81\x82zyxw\x02AB\x04DEFG')
    >>> bmv.n1  #doctest: +ELLIPSIS
    17
    >>> bmv.n2
    34
    >>> bmv  #doctest: +ELLIPSIS
    BMV(n1=17, n2=34, n3=119, nd=nd_1_short__bs(short=33154, bs=b'zyxw'), data1=b'AB', data2=b'DEFG')
    >>> bmv.nd  #doctest: +ELLIPSIS
    nd_1_short__bs(short=33154, bs=b'zyxw')
    >>> bmv.nd.bs
    b'zyxw'
    >>> bytes(bmv.nd)
    b'zyxw'
    >>> bmv.data1
    b'AB'
    >>> bmv.data2
    b'DEFG'
    >>> bytes(bmv)
    b'\x11"w\x81\x82zyxw\x02AB\x04DEFG'
    >>> list(bmv.transcribe_flat())
    [b'\x11', b'"', b'w', b'\x81\x82zyxw', b'\x02', b'AB', b'\x04', b'DEFG']

## Function `BinarySingleStruct(class_name, struct_format, field_name=None)`

A convenience wrapper for `BinaryMultiStruct`
for `struct_format`s with a single field.

Parameters:
* `class_name`: the class name for the generated class
* `struct_format`: the struct format string, specifying a
  single struct field
* `field_name`: optional field name for the value,
  default `'value'`

Example:

    >>> UInt16BE = BinarySingleStruct('UInt16BE', '>H')
    >>> UInt16BE.__name__
    'UInt16BE'
    >>> UInt16BE.format
    '>H'
    >>> UInt16BE.struct   #doctest: +ELLIPSIS
    <_struct.Struct object at ...>
    >>> field = UInt16BE.from_bytes(bytes((2,3)))
    >>> field
    UInt16BE(value=515)
    >>> field.value
    515

## Class `BinarySingleValue(AbstractBinary, BinaryMixin)`

A representation of a single value as the attribute `.value`.

Subclasses must implement:
* `parse` or `parse_value`
* `transcribe` or `transcribe_value`

*Method `BinarySingleValue.parse(bfr)`*:
Parse an instance from `bfr`.

Subclasses must implement this method or `parse_value`.

*Method `BinarySingleValue.parse_value(bfr)`*:
Parse a value from `bfr` based on this class.

Subclasses must implement this method or `parse`.

*Method `BinarySingleValue.parse_value_from_bytes(bs, offset=0, length=None, **kw)`*:
Parse a value from the bytes `bs` based on this class.
Return `(value,offset)`.

*Method `BinarySingleValue.scan_values(bfr, **kw)`*:
Scan `bfr`, yield values.

*Method `BinarySingleValue.transcribe(self)`*:
Transcribe this instance as bytes.

Subclasses must implement this method or `transcribe_value`.

*Method `BinarySingleValue.transcribe_value(value)`*:
Transcribe `value` as bytes based on this class.

Subclasses must implement this method or `transcribe`.

## Class `BinaryUTF16NUL(BinarySingleValue, AbstractBinary, BinaryMixin)`

A NUL terminated UTF-16 string.

*Method `BinaryUTF16NUL.__init__(self, value, *, encoding)`*:
pylint: disable=super-init-not-called

*Method `BinaryUTF16NUL.parse(bfr, *, encoding)`*:
Parse the encoding and value and construct an instance.

*Method `BinaryUTF16NUL.parse_value(bfr, *, encoding)`*:
Read a NUL terminated UTF-16 string from `bfr`, return a `UTF16NULField`..
The mandatory parameter `encoding` specifies the UTF16 encoding to use
(`'utf_16_be'` or `'utf_16_le'`).

*Method `BinaryUTF16NUL.transcribe(self)`*:
Transcribe `self.value` in UTF-16 with a terminating NUL.

*Method `BinaryUTF16NUL.transcribe_value(value, encoding='utf-16')`*:
Transcribe `value` in UTF-16 with a terminating NUL.

## Class `BinaryUTF8NUL(BinarySingleValue, AbstractBinary, BinaryMixin)`

A NUL terminated UTF-8 string.

*Method `BinaryUTF8NUL.parse_value(bfr)`*:
Read a NUL terminated UTF-8 string from `bfr`, return field.

*Method `BinaryUTF8NUL.transcribe_value(s)`*:
Transcribe the `value` in UTF-8 with a terminating NUL.

## Class `BSData(BinarySingleValue, AbstractBinary, BinaryMixin)`

A run length encoded data chunk, with the length encoded as a `BSUInt`.

*Property `BSData.data`*:
An alias for the `.value` attribute.

*Property `BSData.data_offset`*:
The length of the length indicator,
useful for computing the location of the raw data.

*Method `BSData.data_offset_for(bs)`*:
Compute the `data_offset` which would obtain for the bytes `bs`.

*Method `BSData.parse_value(bfr)`*:
Parse the data from `bfr`.

*Method `BSData.transcribe_value(data)`*:
Transcribe the payload length and then the payload.

## Class `BSSFloat(BinarySingleValue, AbstractBinary, BinaryMixin)`

A float transcribed as a BSString of str(float).

*Method `BSSFloat.parse_value(bfr)`*:
Parse a BSSFloat from a buffer and return the float.

*Method `BSSFloat.transcribe_value(f)`*:
Transcribe a float.

## Class `BSString(BinarySingleValue, AbstractBinary, BinaryMixin)`

A run length encoded string, with the length encoded as a BSUInt.

*Method `BSString.parse_value(bfr, encoding='utf-8', errors='strict')`*:
Parse a run length encoded string from `bfr`.

*Method `BSString.transcribe_value(s, encoding='utf-8')`*:
Transcribe a string.

## Class `BSUInt(BinarySingleValue, AbstractBinary, BinaryMixin)`

A binary serialised unsigned `int`.

This uses a big endian byte encoding where continuation octets
have their high bit set. The bits contributing to the value
are in the low order 7 bits.

*Method `BSUInt.decode_bytes(data, offset=0)`*:
Decode an extensible byte serialised unsigned `int` from `data` at `offset`.
Return value and new offset.

Continuation octets have their high bit set.
The octets are big-endian.

If you just have a `bytes` instance, this is the go. If you're
reading from a stream you're better off with `parse` or `parse_value`.

Examples:

    >>> BSUInt.decode_bytes(b'\0')
    (0, 1)

Note: there is of course the usual `BinaryMixin.parse_bytes`
but that constructs a buffer to obtain the individual bytes;
this static method will be more performant
if all you are doing is reading this serialisation
and do not already have a buffer.

*Method `BSUInt.parse_value(bfr)`*:
Parse an extensible byte serialised unsigned `int` from a buffer.

Continuation octets have their high bit set.
The value is big-endian.

This is the go for reading from a stream. If you already have
a bare bytes instance then the `.decode_bytes` static method
is probably most efficient;
there is of course the usual `BinaryMixin.parse_bytes`
but that constructs a buffer to obtain the individual bytes.

*Method `BSUInt.transcribe_value(n)`*:
Encode an unsigned int as an entensible byte serialised octet
sequence for decode. Return the bytes object.

## Class `BytesesField(PacketField)`

A field containing a list of bytes chunks.

The following attributes are defined:
* `value`: the gathered data as a list of bytes instances,
  or None if the field was gathered with `discard_data` true.
* `offset`: the starting offset of the data.
* `end_offset`: the ending offset of the data.

The `offset` and `end_offset` values are recorded during the
parse, and may become irrelevant if the field's contents are
changed.

*Method `BytesesField.from_buffer(bfr, end_offset=None, discard_data=False, short_ok=False)`*:
Create a new `BytesesField` from a buffer
by gathering from `bfr` until `end_offset`.

Parameters:
* `bfr`: the input buffer
* `end_offset`: the ending buffer offset; if this is Ellipsis
  then all the remaining data in `bfr` will be collected
* `discard_data`: discard the data, keeping only the offset information
* `short_ok`: if true, do not raise EOFError if there are
  insufficient data; the field's .end_offset value will be
  less than `end_offset`; the default is False

Note that this method also sets the following attributes
on the new `BytesesField`:
* `offset`: the starting offset of the gathered bytes
* `end_offset`: the ending offset after the gathered bytes
* `length`: the length of the data

## Class `BytesField(BinarySingleValue, AbstractBinary, BinaryMixin)`

A field of bytes.

*Method `BytesField.__len__(self)`*:
The length is the length of the data.

*Property `BytesField.data`*:
Alias for the `.value` attribute.

*Property `BytesField.length`*:
Convenient length attribute.

*Method `BytesField.transcribe_value(value)`*:
A `BytesField` is its own transcription.

*Method `BytesField.value_from_buffer(bfr, length=None)`*:
Parse a `BytesField` of length `length` from `bfr`.

## Class `BytesRunField(PacketField)`

A field containing a continuous run of a single bytes value.

The following attributes are defined:
* `length`: the length of the run
* `bytes_value`: the repeated bytes value

The property `value` is computed on the fly on every reference
and returns a value obeying the buffer protocol: a bytes or
memoryview object.

*Method `BytesRunField.__init__(self, length, bytes_value)`*:
pylint: disable=super-init-not-called

*Method `BytesRunField.from_buffer(bfr, end_offset=None, bytes_value=b'\x00')`*:
Parse a BytesRunField by just skipping the specified number of bytes.

Note: this *does not* check that the skipped bytes contain `bytes_value`.

Parameters:
* `bfr`: the buffer to scan
* `end_offset`: the end offset of the scan, which may be
  an int or Ellipsis to indicate a scan to the end of the
  buffer
* `bytes_value`: the bytes value to replicate, default
  `b' '`; if this is an int then a single byte of that value
  is used

*Method `BytesRunField.transcribe(self)`*:
Transcribe the BytesRunField in 256 byte chunks.

*Property `BytesRunField.value`*:
The run of bytes, computed on the fly.

Values where length <= 256 are cached.

## Function `deferred_field(from_buffer)`

A decorator for a field property.

Usage:

    @deferred_field
    def (self, bfr):
        ... parse value from `bfr`, return value

## `EmptyField = <cs.binary.EmptyPacketField object at 0x107a98220>`

An empty data field, used as a placeholder for optional
fields when they are not present.

The singleton `EmptyField` is a predefined instance.

## Class `EmptyPacketField(PacketField)`

An empty data field, used as a placeholder for optional
fields when they are not present.

The singleton `EmptyField` is a predefined instance.

*Method `EmptyPacketField.from_buffer(bfr)`*:
pylint: disable=arguments-differ

## Function `fixed_bytes_field(length, class_name=None)`

Factory for `BytesField` subclasses built from fixed length byte strings.

## Function `flatten(chunks)`

Flatten `chunks` into an iterable of `bytes` instances.

This exists to allow subclass methods to easily return
transcribeable things (having a `.transcribe` method), ASCII
strings or bytes or iterables or even `None`, in turn allowing
them simply to return their superclass' chunks iterators
directly instead of having to unpack them.

An example from the `cs.iso14496.METABoxBody` class:

    def transcribe(self):
        yield super().transcribe()
        yield self.theHandler
        yield self.boxes

The binary classes `flatten` the result of the `.transcribe`
method to obtain `bytes` insteances for the object's bnary
transcription.

## Class `Float64BE(Float64BE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'>d'` and presents the attributes ('value',).

*Method `Float64BE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `Float64BE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `Float64BE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `Float64BE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `Float64LE(Float64LE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'<d'` and presents the attributes ('value',).

*Method `Float64LE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `Float64LE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `Float64LE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `Float64LE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `Int16BE(Int16BE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'>h'` and presents the attributes ('value',).

*Method `Int16BE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `Int16BE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `Int16BE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `Int16BE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `Int16LE(Int16LE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'<h'` and presents the attributes ('value',).

*Method `Int16LE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `Int16LE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `Int16LE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `Int16LE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `Int32BE(Int32BE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'>l'` and presents the attributes ('value',).

*Method `Int32BE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `Int32BE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `Int32BE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `Int32BE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `Int32LE(Int32LE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'<l'` and presents the attributes ('value',).

*Method `Int32LE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `Int32LE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `Int32LE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `Int32LE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `ListField(PacketField)`

A field which is itself a list of other `PacketField`s.

*Method `ListField.__iter__(self)`*:
Iterating over a `ListField` iterates over its `.value`.

*Method `ListField.from_buffer(bfr)`*:
ListFields do not know enough to parse a buffer.

*Method `ListField.transcribe_value(value)`*:
Transcribe each item in `value`.

## Function `multi_struct_field(struct_format, subvalue_names=None, class_name=None)`

A class factory for `PacketField` subclasses built around complex `struct` formats.

**Deprecated**: see the `BinaryMultiValue` factory instead.

See also the convenience class factory `structtuple`
which is usually easier to work with.

Parameters:
* `struct_format`: the `struct` format string
* `subvalue_names`: an optional field name list;
  if supplied then the field value will be a `namedtuple` with
  these names
* `class_name`: option name for the generated class

## Class `Packet(PacketField)`

Base class for compound objects derived from binary data.

*DEPRECATED*:
please adopt one of the `BinaryMutli`* classes instead.

*Method `Packet.__init__(self, **fields)`*:
Initialise the `Packet`.

A `Packet` is its own `.value`.

If any keyword arguments are provided, they are used as a
mapping of `field_name` to `Field` instance, supporting
direct construction of simple `Packet`s.
From Python 3.6 onwards keyword arguments preserve the calling order;
in Python versions earlier than this the caller should
adjust the `Packet.field_names` list to the correct order after
initialisation.

*Method `Packet.__getattr__(self, attr)`*:
Unknown attributes may be field names; return their value.

*Method `Packet.add_deferred_field(self, attr_name, bfr, length)`*:
Store the unparsed data for attribute `attr_name`
comprising the next `length` bytes from `bfr`.

*Method `Packet.add_field(self, field_name, field)`*:
Add a new `PacketField` `field` named `field_name`.

*Method `Packet.add_from_buffer(self, field_name, bfr, factory, **kw)`*:
Add a new `PacketField` named `field_name` parsed from `bfr` using `factory`.
Updates the internal field records.
Returns the new `PacketField`'s .value.

Parameters:
* `field_name`: the name for the new field; it must be new.
* `bfr`: a `CornuCopyBuffer` from which to parse the field data.
* `factory`: a factory for parsing the field data, returning
  a `PacketField`. If `factory` is a class then its .from_buffer
  method is called, otherwise the factory is called directly.

Additional keyword arguments are passed to the internal
factory call.

For convenience, `factory` may also be a str in which case
it is taken to be a single struct format specifier.
Alternatively, `factory` may be an integer in which case
it is taken to be a fixed length bytes field.

*Method `Packet.add_from_bytes(self, field_name, bs, factory, offset=0, length=None, **kw)`*:
Add a new `PacketField` named `field_name` parsed from the
bytes `bs` using `factory`. Updates the internal field
records.
Returns the new `PacketField`'s .value and the new parse
offset within `bs`.

Parameters:
* `field_name`: the name for the new field; it must be new.
* `bs`: the bytes containing the field data; a `CornuCopyBuffer`
  is made from this for the parse.
* `factory`: a factory for parsing the field data, returning
  a `PacketField`. If `factory` is a class then its .from_buffer
  method is called, otherwise the factory is called directly.
* `offset`: optional start offset of the field data within
  `bs`, default 0.
* `length`: optional maximum number of bytes from `bs` to
  make available for the parse, default None meaning that
  everything from `offset` onwards is available.

Additional keyword arguments are passed to the internal
`.add_from_buffer` call.

*Method `Packet.add_from_value(self, field_name, value, transcribe_value_fn)`*:
Add a new field named `field_name` with `.value=value`.
Return the new field.

*Method `Packet.deferred_field(from_buffer)`*:
A decorator for a field property.

Usage:

    @deferred_field
    def (self, bfr):
        ... parse value from `bfr`, return value

*Method `Packet.get_field(self, field_name)`*:
Return the field named `field_name`.

*Method `Packet.pop_field(self)`*:
Remove the last field, return `(field_name,field)`.

*Method `Packet.remove_field(self, field_name)`*:
Remove the field `field_name`. Return the field.

*Method `Packet.self_check(self)`*:
Internal self check. Returns `True` if passed.

If the `Packet` has a `PACKET_FIELDS` attribute, normally a
class attribute, then check the fields against it. The
`PACKET_FIELDS` attribute is a mapping of `field_name` to
a specification of `required` and `types`. The specification
may take one of 2 forms:
* a tuple of `(required, types)`
* a single `type`; this is equivalent to `(True, (type,))`
Their meanings are as follows:
* `required`: a Boolean. If true, the field must be present
  in the packet `field_map`, otherwise it need not be present.
* `types`: a tuple of acceptable field types

There are some special semantics involved here.

An implementation of a `Packet` may choose to make some
fields plain instance attributes instead of `Field`s in the
`field_map` mapping, particularly variable packets such as
a `cs.iso14496.BoxHeader`, whose `.length` may be parsed
directly from its binary form or computed from other fields
depending on the `box_size` value. Therefore, checking for
a field is first done via the `field_map` mapping, then by
`getattr`, and as such the acceptable `types` may include
non-`PacketField` types such as `int`.

Here is the `BoxHeader.PACKET_FIELDS` definition as an example:

  PACKET_FIELDS = {
    'box_size': UInt32BE,
    'box_type': BytesField,
    'length': (
        True,
        (
            type(Ellipsis),
            UInt64BE,
            UInt32BE,
            int
        ),
    ),
  }

Note that `length` includes some non-`PacketField` types,
and that it is written as a tuple of `(True, types)` because
it has more than one acceptable type.

*Method `Packet.set_field(self, field_name, new_field)`*:
Replace the field named `field_name`.

Note that this replaces the field, not its value.

*Method `Packet.transcribe(self)`*:
Yield a sequence of bytes objects for this instance.

## Class `PacketField`

A record for an individual packet field.

*DEPRECATED*:
please adopt one of the `BinarySingle`* classes instead.

This normally holds a single value,
for example an int of a particular size or a string.

There are 2 basic ways to implement a `PacketField` subclass:
* simple: implement `value_from_buffer` and `transcribe_value`
* complex: implement `from_buffer` and `transcribe`

In the simple case subclasses should implement two methods:
* `value_from_buffer`:
  parse the value from a `CornuCopyBuffer` and return the parsed value
* `transcribe_value`:
  transcribe the value as bytes

In the more complex case,
sometimes a `PacketField` may not warrant (or perhaps fit)
the formality of a `Packet` with its multifield structure.

One example is the `cs.iso14496.UTF8or16Field` class.

`UTF8or16Field` supports an ISO14496 UTF8 or UTF16 string field,
as as such has 2 attributes:
* `value`: the string itself
* `bom`: a UTF16 byte order marker or `None`;
  `None` indicates that the string should be encoded as UTF-8
  and otherwise the BOM indicates UTF16 big endian or little endian.

To make this subclass it defines these methods:
* `from_buffer`:
  to read the optional BOM and then the following encoded string;
  it then returns the new `UTF8or16Field`
  initialised from these values via `cls(text, bom=bom)`.
* `transcribe`:
  to transcribe the optional BOM and suitably encoded string.
The instance method `transcribe` is required because the transcription
requires knowledge of the BOM, an attribute of an instance.

*Method `PacketField.__init__(self, value=None)`*:
Initialise the `PacketField`.
If omitted the inial field `value` will be `None`.

*Method `PacketField.__len__(self)`*:
Compute the length by running a transcription and measuring it.

*Method `PacketField.from_buffer(bfr, **kw)`*:
Factory to return a `PacketField` instance from a `CornuCopyBuffer`.

This default implementation is for single value `PacketField`s
and instantiates the instance from the value returned
by `cls.value_from_buffer(bfr, **kw)`;
implementors should implement `value_from_buffer`.

*Method `PacketField.from_bytes(bs, offset=0, length=None, **kw)`*:
Factory to return a `PacketField` instance parsed from the
bytes `bs` starting at `offset`.
Returns the new `PacketField` and the post parse offset.

The parameters `offset` and `length` are as for the
`CornuCopyBuffer.from_bytes` factory.

This relies on the `cls.from_buffer` method for the parse.

*Method `PacketField.parse_buffer(bfr, **kw)`*:
Function to parse repeated instances of `cls` from the buffer `bfr`
until end of input.

*Method `PacketField.parse_buffer_values(bfr, **kw)`*:
Function to parse repeated instances of `cls.value`
from the buffer `bfr` until end of input.

*Method `PacketField.parse_buffer_with_offsets(bfr, **kw)`*:
Function to parse repeated instances of `cls` from the buffer `bfr`
until end of input.
Yields `(offset,instance,post_offset)`
where `offset` if the buffer offset where the instance commenced
and `post_offset` is the buffer offset after the instance.

*Method `PacketField.parse_file(f, **kw)`*:
Function to parse repeated instances of `cls` from the file `f`
until end of input.

Parameters:
* `f`: the binary file object to parse;
  if `f` is a string, that pathname is opened for binary read.

*Method `PacketField.transcribe(self)`*:
Return or yield the bytes transcription of this field.

This may directly return:
* a `bytes` or `memoryview` holding the binary data
* `None`: indicating no binary data
* `str`: indicating the ASCII encoding of the string
* an iterable of these things (including further iterables)
  to support trivially transcribing via other fields'
  `transcribe` methods

Callers will usually call `flatten` on the output of this
method, or use the convenience `transcribe_flat` method
which calls `flatten` for them.

This default implementation is for single value fields and
just calls `self.transcribe_value(self.value)`.

*Method `PacketField.transcribe_flat(self)`*:
Return a flat iterable of chunks transcribing this field.

*Method `PacketField.transcribe_value(value, **kw)`*:
For simple `PacketField`s, return a bytes transcription of a
value suitable for the `.value` attribute.

For example, the `BSUInt` subclass stores a `int` as its
`.value` and exposes its serialisation method, suitable for
any `int`, as `transcribe_value`.

Note that this calls the class `transcribe` method, which
may return an iterable.
Use the `value_as_bytes` method to get a single flat `bytes` result.

*Method `PacketField.transcribe_value_flat(value)`*:
Return a flat iterable of chunks transcribing `value`.

*Method `PacketField.value_as_bytes(value, **kw)`*:
For simple `PacketField`s, return a transcription of a
value suitable for the `.value` attribute
as a single `bytes` value.

This flattens and joins the transcription returned by
`transcribe_value`.

*Method `PacketField.value_from_buffer(bfr, **kw)`*:
Function to parse and return the core value from a `CornuCopyBuffer`.

For single value fields it is enough to implement this method.

For multiple value fields it is better to implement `cls.from_buffer`.

*Method `PacketField.value_from_bytes(bs, offset=0, length=None, **kw)`*:
Return a value parsed from the bytes `bs` starting at `offset`.
Returns the new value and the post parse offset.

The parameters `offset` and `length` are as for the
`CornuCopyBuffer.from_bytes` factory.

This relies on the `cls.from_bytes` method for the parse.

*Property `PacketField.value_s`*:
The preferred string representation of the value.

## Function `pt_spec(pt, name=None)`

Convert a parse/transcribe specification `pt`
into an `AbstractBinary` subclass.

This is largely used to provide flexibility
in the specifications for the `BinaryMultiValue` factory
but can be used as a factory for other simple classes.

If the specification `pt` is a subclass of `AbstractBinary`
this is returned directly.

If `pt` is a 2-tuple of `str`
the values are presumed to be a format string for `struct.struct`
and filed names separated by spaces;
a new `BinaryMultiStruct` class is created from these and returned.

Otherwise two functions
`f_parse_value(bfr)` and `f_transcribe_value(value)`
are obtained and used to construct a new `BinarySingleValue` class
as follows:

If `pt` has `.parse_value` and `.transcribe_value` callable attributes,
use those for `f_parse_value` and `f_transcribe_value` respectively.

Otherwise, if `pt` is an `int`
define `f_parse_value` to obtain exactly that many bytes from a buffer
and `f_transcribe_value` to return those bytes directly.

Otherwise presume `pt` is a 2-tuple of `(f_parse_value,f_transcribe_value)`.

## Class `SimpleBinary(types.SimpleNamespace, AbstractBinary, BinaryMixin)`

Abstract binary class based on a `SimpleNamespace`,
thus providing a nice `__str__` and a keyword based `__init__`.
Implementors must still define `.parse` and `.transcribe`.

To constrain the arguments passed to `__init__`,
define an `__init__` which accepts specific keyword arguments
and pass through to `super().__init__()`. Example:

    def __init__(self, *, field1=None, field2):
        """ Accept only `field1` (optional)
            and `field2` (mandatory).
        """
        super().__init__(field1=field1, field2=field2)

## Function `structtuple(class_name, struct_format, subvalue_names)`

Convenience wrapper for `multi_struct_field`.

Example:

    Enigma2Cut = structtuple('Enigma2Cut', '>QL', 'pts type')

which is a record with big-endian unsigned 64 and 32 fields
named `pts` and `type`.

## Class `UInt16BE(UInt16BE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'>H'` and presents the attributes ('value',).

*Method `UInt16BE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt16BE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt16BE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt16BE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UInt16LE(UInt16LE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'<H'` and presents the attributes ('value',).

*Method `UInt16LE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt16LE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt16LE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt16LE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UInt32BE(UInt32BE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'>L'` and presents the attributes ('value',).

*Method `UInt32BE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt32BE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt32BE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt32BE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UInt32LE(UInt32LE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'<L'` and presents the attributes ('value',).

*Method `UInt32LE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt32LE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt32LE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt32LE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UInt64BE(UInt64BE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'>Q'` and presents the attributes ('value',).

*Method `UInt64BE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt64BE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt64BE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt64BE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UInt64LE(UInt64LE, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'<Q'` and presents the attributes ('value',).

*Method `UInt64LE.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt64LE.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt64LE.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt64LE.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UInt8(UInt8, builtins.tuple, AbstractBinary, BinaryMixin)`

An `AbstractBinary` `namedtuple` which parses and transcribes
the struct format `'B'` and presents the attributes ('value',).

*Method `UInt8.parse(bfr)`*:
Parse from `bfr` via `struct.unpack`.

*Method `UInt8.parse_value(bfr)`*:
Parse a value from `bfr`, return the value.

*Method `UInt8.transcribe(self)`*:
Transcribe via `struct.pack`.

*Method `UInt8.transcribe_value(value)`*:
Transcribe a value back into bytes.

## Class `UTF16NULField(PacketField)`

A NUL terminated UTF-16 string.

*Method `UTF16NULField.__init__(self, value, *, encoding)`*:
Initialise the `PacketField`.
If omitted the inial field `value` will be `None`.

*Method `UTF16NULField.from_buffer(bfr, encoding)`*:
Read a NUL terminated UTF-16 string from `bfr`, return a `UTF16NULField`..
The mandatory parameter `encoding` specifies the UTF16 encoding to use
(`'utf_16_be'` or `'utf_16_le'`).

*Method `UTF16NULField.transcribe_value(value, encoding='utf-16')`*:
Transcribe `value` in UTF-16 with a terminating NUL.

## Class `UTF8NULField(PacketField)`

A NUL terminated UTF-8 string.

*Method `UTF8NULField.transcribe_value(s)`*:
Transcribe the `value` in UTF-8 with a terminating NUL.

*Method `UTF8NULField.value_from_buffer(bfr)`*:
Read a NUL terminated UTF-8 string from `bfr`, return field.

# Release Log



*Release 20220605*:
BinaryMixin: replace scan_file with scan_fspath, as the former left uncertainty about the amount of the file consumed.

*Release 20210316*:
* BSUInt: rename parse_bytes to decode_bytes, the former name conflicted with BinaryMixin.parse_bytes and broken the semantics.
* Minor refactors.

*Release 20210306*:
MAJOR RELEASE: The PacketField classes and friends were hard to use; this release supplied a suite of easier to use and more consistent Binary* classes, and ports most of those things based on the old scheme to the new scheme.

*Release 20200229*:
* ListField: replace transcribe method with transcribe_value method, aids external use.
* Add `.length` attribute to struct based packet classes providing the data length of the structure (struct.Struct.size).
* Packet: new `add_deferred_field` method to consume the raw data for a field for parsing later (done automatically if the attribute is accessed).
* New `@deferred_field` decorator for the parser for that stashed data.

*Release 20191230.3*:
Docstring tweak.

*Release 20191230.2*:
Documentation updates.

*Release 20191230.1*:
Docstring updates. Semantic changes were in the previous release.

*Release 20191230*:
* ListField: new __iter__ method.
* Packet: __str__: accept optional `skip_fields` parameter to omit some field names.
* Packet: new .add_from_value method to add a named field with a presupplied value.
* Packet: new remove_field(field_name) and pop_field() methods to remove fields.
* BytesesField: __iter__ yields the bytes values, transcribe=__iter__.
* PacketField: propagate keyword arguments through various methods, required for parameterised PacketFields.
* New UTF16NULField, a NUL terminated UTF16 string.
* PacketField: provide a default `.transcribe_value` method which makes a new instance and calls its `.transcribe` method.
* Documentation update and several minor changes.

*Release 20190220*:
* Packet.self_check: fields without a sanity check cause a warning, not a ValueError.
* New Float64BE, Float64LE and BSSFloat classes for IEEE floats and floats-as-strings.
* Additional module docstringage on subclassing Packet and PacketField.
* BSString: drop redundant from_buffer class method.
* PacketField.__init__: default to value=None if omitted.

*Release 20181231*:
flatten: do not yield zero length bytelike objects, can be misread as EOF on some streams.

*Release 20181108*:
* New PacketField.transcribe_value_flat convenience method to return a flat iterable of bytes-like objects.
* New PacketField.parse_buffer generator method to parse instances of the PacketField from a buffer until end of input.
* New PacketField.parse_buffer_values generator method to parse instances of the PacketField from a buffer and yield the `.value` attribute until end of input.

*Release 20180823*:
* Some bugfixes.
* Define PacketField.__eq__.
* BSUInt, BSData and BSString classes implementing the serialisations from cs.serialise.
* New PacketField.value_from_bytes class method.
* New PacketField.value_from_buffer method.

*Release 20180810.2*:
Documentation improvements.

*Release 20180810.1*:
Improve module description.

*Release 20180810*:
BytesesField.from_buffer: make use of the buffer's skipto method if discard_data is true.

*Release 20180805*:
* Packet: now an abstract class, new self_check method initially checking the
* PACKET_FIELDS class attribute against the instance, new methods get_field
* and set_field to fetch or replace existing fields, allow keyword arguments
* to initialise the Packet fields and document the dependency on keyword
* argument ordering.
* PacketField: __len__ computed directory from a transcribe, drop other __len__
* methods.
* EmptyField singleton to use as a placeholder for missing optional fields.
* BytesField: implement value_s and from_buffer.
* multi_struct_field: implement __len__ for generated class.
* flatten: treat memoryviews like bytes.
* Assorted docstrings and fixes.

*Release 20180801*:
Initial PyPI release.
