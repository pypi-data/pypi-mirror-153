Facilities for ISO14496 files - the ISO Base Media File Format,
the basis for several things including MP4 and MOV.

*Latest release 20220606*:
Update obsolete use of Tag.with_prefix.

ISO make the standard available here:
* [link](http://standards.iso.org/ittf/PubliclyAvailableStandards/index.html)
* [link](http://standards.iso.org/ittf/PubliclyAvailableStandards/c068960_ISO_IEC_14496-12_2015.zip)

## Function `add_body_class(klass)`

Register a box body class in KNOWN_BOXBODY_CLASSES.

## Function `add_body_subclass(superclass, box_type, section, desc)`

Create and register a new BoxBody class that is simply a subclass of
another.  Returns the new class.

## Function `add_generic_sample_boxbody(box_type, section, desc, struct_format_v0, sample_fields, struct_format_v1=None, has_inferred_entry_count=False)`

Create and add a specific Time to Sample box - section 8.6.1.

## Function `add_time_to_sample_boxbody(box_type, section, desc)`

Add a Time to Sample box - section 8.6.1.

## Class `Box(cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

Base class for all boxes - ISO14496 section 4.2.

This has the following fields:
* `header`: a `BoxHeader`
* `body`: a `BoxBody` instance, usually a specific subclass
* `unparsed`: any unconsumed bytes from the `Box` are stored as here

*Property `Box.BOX_TYPE`*:
The default .BOX_TYPE is inferred from the class name.

*Method `Box.__getattr__(self, attr)`*:
If there is no direct attribute from `SimpleBinary.__getattr__`,
have a look in the `.header` and `.body`.

*Method `Box.__iter__(self)`*:
Iterating over a `Box` iterates over its body.
Typically that would be the `.body.boxes`
but might be the samples if the body is a sample box,
etc.

*Method `Box.ancestor(self, box_type)`*:
Return the closest ancestor box of type `box_type`.

*Property `Box.box_type`*:
The Box header type.

*Property `Box.box_type_path`*:
The type path to this Box.

*Property `Box.box_type_s`*:
The Box header type as a string.

If the header type bytes decode as ASCII, return that,
otherwise the header bytes' repr().

*Method `Box.dump(self, **kw)`*:
Dump this Box.

*Method `Box.gather_metadata(self)`*:
Walk the `Box` hierarchy looking for metadata.
Yield `(Box,TagSet)` for each `b'moov'` or `b'trak'` `Box`.

*Method `Box.metatags(self)`*:
Return a `TagSet` containing metadata for this box.

*Method `Box.parse(bfr)`*:
Decode a Box from `bfr` and return it.

*Method `Box.parse_field(self, field_name, bfr, binary_cls)`*:
`parse_field` delegates to the `Box` body `parse_field`.

*Property `Box.parse_length`*:
The length of the box as consumed from the buffer,
computed as `self.end_offset-self.offset`.

*Method `Box.reparse_buffer(self)`*:
Context manager for continuing a parse from the `unparsed` field.

Pops the final `unparsed` field from the `Box`,
yields a `CornuCopyBuffer` make from it,
then pushes the `unparsed` field again
with the remaining contents of the buffer.

*Method `Box.self_check(self)`*:
Sanity check this Box.

*Method `Box.transcribe(self)`*:
Transcribe the `Box`.

Before transcribing the data, we compute the total box_size
from the lengths of the current header, body and unparsed
components, then set the header length if that has changed.
Since setting the header length can change its representation
we compute the length again and abort if it isn't stable.
Otherwise we proceeed with a regular transcription.

*Property `Box.unparsed_bs`*:
The unparsed data as a single `bytes` instance.

*Property `Box.user_type`*:
The header user_type.

*Method `Box.walk(self)`*:
Walk this `Box` hierarchy.

Yields the starting box and its children as `(self,subboxes)`
and then yields `(subbox,subsubboxes)` for each child in turn.

As with `os.walk`, the returned `subboxes` list
may be modified to prune the subsequent walk.

## Class `BoxBody(cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

Abstract basis for all `Box` bodies.

*Method `BoxBody.__getattr__(self, attr)`*:
The following virtual attributes are defined:
* *TYPE*`s`:
  "boxes of type *TYPE*",
  an uppercased box type name with a training `s`;
  a list of all elements whose `.box_type`
  equals *TYPE*`.lower().encode('ascii')`.
  The elements are obtained by iterating over `self`
  which normally means iterating over the `.boxes` attribute.
* *TYPE*:
  "the box of type *TYPE*",
  an uppercased box type name;
  the sole element whose box type matches the type,
  obtained from `.`*TYPE*`s[0]`
  with a requirement that there is exactly one match.
* *TYPE*`0`:
  "the optional box of type *TYPE*",
  an uppercased box type name with a trailing `0`;
  the sole element whose box type matches the type,
  obtained from `.`*TYPE*`s[0]`
  with a requirement that there is exactly zero or one match.
  If there are zero matches, return `None`.
  Otherwise return the matching box.

*Method `BoxBody.add_field(self, field_name, value)`*:
Add a field named `field_name` with the specified `value`
to the box fields.

*Method `BoxBody.boxbody_type_from_klass()`*:
Compute the Box's 4 byte type field from the class name.

*Method `BoxBody.parse(bfr)`*:
Create a new instance and gather the `Box` body fields from `bfr`.

Subclasses implement a `parse_fields` method to parse additional fields.

*Method `BoxBody.parse_boxes(self, bfr, **kw)`*:
Utility method to parse the remainder of the buffer as a
sequence of `Box`es.

*Method `BoxBody.parse_field(self, field_name, bfr, binary_cls)`*:
Parse an instance of `binary_cls` from `bfr`
and store it as the attribute named `field_name`.

`binary_cls` may also be an `int`, in which case that many
bytes are read from `bfr`.

*Method `BoxBody.parse_field_value(self, field_name, bfr, binary_cls)`*:
Parse a single value binary, store the value as `field_name`,
store the instance as the field `field_name+'__Binary'`
for transcription.

Note that this disassociaes the plain value attribute
from what gets transcribed.

*Method `BoxBody.parse_fields(self, bfr)`*:
Parse additional fields.
This base class implementation consumes nothing.

*Method `BoxBody.transcribe(self)`*:
Transcribe the binary structure.

This default implementation transcribes the fields parsed with the
`parse_field` method in the order parsed.

*Method `BoxBody.transcribe_fields(self)`*:
Transcribe the fields parsed with the `parse_field` method in the
order parsed.

## Class `BoxHeader(cs.binary.BoxHeader, cs.binary._BinaryMultiValue_Base, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An ISO14496 Box header packet.

*Method `BoxHeader.parse(bfr)`*:
Decode a box header from `bfr`.

## Class `BTRTBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

BitRateBoxBody - section 8.5.2.2.

*Method `BTRTBoxBody.parse_fields(self, bfr)`*:
Gather the `bufferSizeDB`, `maxBitrate` and `avgBitrate` fields.

## Class `CO64BoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'c064' Chunk Offset box - section 8.7.5.

*Property `CO64BoxBody.chunk_offsets`*:
Boilerplate for the property: test for parsed value, parse
from raw data if not yet present.

*Method `CO64BoxBody.parse_fields(self, bfr)`*:
Gather the `entry_count` and `chunk_offsets` fields.

*Method `CO64BoxBody.transcribe(self)`*:
Transcribe a `CO64BoxBody`.

## Class `ContainerBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

Common subclass of several things with `.boxes`.

## Class `CPRTBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'cprt' Copyright box - section 8.10.2.

*Property `CPRTBoxBody.language`*:
The `language_field` as the 3 character ISO 639-2/T language code.

*Method `CPRTBoxBody.parse_fields(self, bfr)`*:
Gather the `language` and `notice` fields.

## Class `CSLGBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'cslg' Composition to Decode box - section 8.6.1.4.

*`CSLGBoxBody.CSLGParamsLong`*

*`CSLGBoxBody.CSLGParamsQuad`*

*Method `CSLGBoxBody.__getattr__(self, attr)`*:
Present the `params` attributes at the top level.

*Method `CSLGBoxBody.parse_fields(self, bfr)`*:
Gather the compositionToDTSShift`, `leastDecodeToDisplayDelta`,
`greatestDecodeToDisplayDelta`, `compositionStartTime` and
`compositionEndTime` fields.

## Function `decode_itunes_date_field(data)`

The iTunes 'Date' meta field: a year or an ISO timestamp.

## Function `deref_box(B, path)`

Dereference a path with respect to this Box.

## Class `DREFBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'dref' Data Reference box containing Data Entry boxes - section 8.7.2.1.

*Method `DREFBoxBody.parse_fields(self, bfr)`*:
Gather the `entry_count` and `boxes` fields.

## Function `dump_box(B, indent='', fp=None, crop_length=170, indent_incr=None)`

Recursively dump a Box.

## Class `ELNGBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A ELNGBoxBody is a Extended Language Tag box - ISO14496 section 8.4.6.

*Method `ELNGBoxBody.parse_fields(self, bfr)`*:
Gather the `extended_language` field.

## Class `ELSTBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An 'elst' Edit List FullBoxBody - section 8.6.6.

*`ELSTBoxBody.V0EditEntry`*

*`ELSTBoxBody.V1EditEntry`*

*Property `ELSTBoxBody.entry_class`*:
The class representing each entry.

*Property `ELSTBoxBody.entry_count`*:
The number of entries.

*Method `ELSTBoxBody.parse_fields(self, bfr)`*:
Parse the fields of an `ELSTBoxBody`.

*Method `ELSTBoxBody.transcribe(self)`*:
Transcribe an `ELSTBoxBody`.

## Class `FallbackBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A `BoxBody` subclass which parses nothing for unimplemented `Box` types,
used by `pick_boxbody_class()`.

## Class `FREEBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'free' or 'skip' box - ISO14496 section 8.1.2.
Note the length and discard the data portion.

*Method `FREEBoxBody.parse_fields(self, bfr, end_offset=Ellipsis, **kw)`*:
Gather the `padding` field.

## Class `FTYPBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An 'ftyp' File Type box - ISO14496 section 4.3.
Decode the major_brand, minor_version and compatible_brands.

*Property `FTYPBoxBody.compatible_brands`*:
The compatible brands as a list of 4 byte bytes instances.

*Method `FTYPBoxBody.parse_fields(self, bfr, **kw)`*:
Gather the `major_brand`, `minor_version` and `brand_bs` fields.

## Class `FullBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A common extension of a basic BoxBody, with a version and flags field.
ISO14496 section 4.2.

*Property `FullBoxBody.flags`*:
The flags value, computed from the 3 flag bytes.

## Class `HDLRBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A HDLRBoxBody is a Handler Reference box - ISO14496 section 8.4.3.

*Property `HDLRBoxBody.handler_type`*:
The handler_type as an ASCII string, its usual form.

*Method `HDLRBoxBody.parse_fields(self, bfr)`*:
Gather the `handler_type_long` and `name` fields.

## Function `ILSTAofBSchema(attribute_name)`

Attribute name and type for ILST "A of B" schema.

## Class `ILSTBoxBody(ContainerBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

Apple iTunes Information List, container for iTunes metadata fields.

The basis of the format knowledge here comes from AtomicParsley's
documentation here:

    http://atomicparsley.sourceforge.net/mpeg-4files.html

and additional information from:

    https://github.com/sergiomb2/libmp4v2/wiki/iTunesMetadata

*Method `ILSTBoxBody.parse_fields(self, bfr)`*:
pylint: disable=attribute-defined-outside-init,too-many-locals,too-many-statements

## Function `ILSTISOFormatSchema(attribute_name)`

Attribute name and type for ILST ISO format schema.

## Function `ILSTRawSchema(attribute_name)`

Attribute name and type for ILST raw schema.

## Function `ILSTTextSchema(attribute_name)`

Attribute name and type for ILST text schema.

## Function `ILSTUInt32BESchema(attribute_name)`

Attribute name and type for ILST UInt32BE schema.

## Function `ILSTUInt8Schema(attribute_name)`

Attribute name and type for ILST UInt8BE schema.

## Class `itunes_media_type(builtins.tuple)`

itunes_media_type(type, stik)

*Property `itunes_media_type.stik`*:
Alias for field number 1

*Property `itunes_media_type.type`*:
Alias for field number 0

## Class `itunes_store_country_code(builtins.tuple)`

itunes_store_country_code(country_name, iso_3166_1_code, itunes_store_code)

*Property `itunes_store_country_code.country_name`*:
Alias for field number 0

*Property `itunes_store_country_code.iso_3166_1_code`*:
Alias for field number 1

*Property `itunes_store_country_code.itunes_store_code`*:
Alias for field number 2

## Function `main(argv=None)`

Command line mode.

## Class `MDATBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A Media Data Box - ISO14496 section 8.1.1.

*Method `MDATBoxBody.parse_fields(self, bfr)`*:
Gather all data to the end of the field.

*Method `MDATBoxBody.transcribe(self)`*:
Transcribe the data.
Raise an `AssertionError` if we skipped the data during the parse.

*Method `MDATBoxBody.transcribed_length(self)`*:
Return the transcription length even if we didn't keep the data.

## Class `MDHDBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A MDHDBoxBody is a Media Header box - ISO14496 section 8.4.2.

*Method `MDHDBoxBody.parse_fields(self, bfr)`*:
Gather the `creation_time`, `modification_time`, `timescale`,
`duration` and `language_short` fields.

## Class `METABoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'meta' Meta BoxBody - section 8.11.1.

*Method `METABoxBody.__getattr__(self, *a, **kw)`*:
Present the `ilst` attributes if present.

*Method `METABoxBody.parse_fields(self, bfr)`*:
Gather the `theHandler` Box and gather the following Boxes as `boxes`.

## Class `MOOVBoxBody(ContainerBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An 'moov' Movie box - ISO14496 section 8.2.1.
Decode the contained boxes.

## Class `MP4Command(cs.cmdutils.BaseCommand)`

Command line usage:

Usage: mp4 subcommand [...]
  Subcommands:
    autotag autotag [-n] [-p prefix] [--prefix=prefix] paths...
      Tag paths based on embedded MP4 metadata.
      -n  No action.
      -p prefix, --prefix=prefix
          Set the prefix of added tags, default: 'mp4'
    deref ...
        Dereference a Box specification against ISO14496 files.
    extract extract [-H] filename boxref output
      Extract the referenced Box from the specified filename into output.
      -H  Skip the Box header.
    help [-l] [subcommand-names...]
      Print the full help for the named subcommands,
      or for all subcommands if no names are specified.
      -l  Long help even if no subcommand-names provided.
    info info [{-|filename}]...]
      Print informative report about each source.
    parse [parse [{-|filename}]...]
      Parse the named files (or stdin for "-").
    tags path
      Report the tags of `path` based on embedded MP4 metadata.
    test [testnames...]
      Run self tests.

*Method `MP4Command.cmd_autotag(self, argv)`*:
Usage: {cmd} autotag [-n] [-p prefix] [--prefix=prefix] paths...
Tag paths based on embedded MP4 metadata.
-n  No action.
-p prefix, --prefix=prefix
    Set the prefix of added tags, default: 'mp4'

*Method `MP4Command.cmd_deref(argv)`*:
Dereference a Box specification against ISO14496 files.

*Method `MP4Command.cmd_extract(argv)`*:
Usage: {cmd} extract [-H] filename boxref output
Extract the referenced Box from the specified filename into output.
-H  Skip the Box header.

*Method `MP4Command.cmd_info(argv)`*:
Usage: {cmd} info [{{-|filename}}]...]
Print informative report about each source.

*Method `MP4Command.cmd_parse(argv)`*:
Usage: {cmd} [parse [{{-|filename}}]...]
Parse the named files (or stdin for "-").

*Method `MP4Command.cmd_tags(self, argv)`*:
Usage: {cmd} path
Report the tags of `path` based on embedded MP4 metadata.

*Method `MP4Command.cmd_test(self, argv)`*:
Usage: {cmd} [testnames...]
Run self tests.

## Class `MVHDBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An 'mvhd' Movie Header box - ISO14496 section 8.2.2.

## Class `OverBox(cs.binary.BinaryListValues, cs.binary.AbstractBinary, cs.binary.BinaryMixin, HasBoxesMixin)`

A fictitious `Box` encompassing all the Boxes in an input buffer.

*Property `OverBox.boxes`*:
Alias `.value` as `.boxes`: the `Box`es encompassed by this `OverBox`.

*Method `OverBox.dump(self, **kw)`*:
Dump this OverBox.

*Property `OverBox.length`*:
The `OverBox` is as long as the subsidary Boxes.

*Method `OverBox.parse(bfr)`*:
Parse the `OverBox`.

*Method `OverBox.walk(self)`*:
Walk the `Box`es in the `OverBox`.

This does not yield the `OverBox` itself, it isn't really a `Box`.

## Function `parse(o)`

Return the `OverBox` from a source (str, int, bytes, file).

The leading `o` parameter may be one of:
* `str`: a filesystem file pathname
* `int`: a OS file descriptor
* `bytes`: a `bytes` object
* `file`: if not `int` or `str` the presumption
  is that this is a file-like object

Keyword arguments are as for `OverBox.from_buffer`.

## Function `parse_deref_path(path, offset=0)`

Parse a `path` string from `offset`.
Return the path components and the offset where the parse stopped.

Path components:
* _identifier_: an identifier represents a Box field or if such a
  field is not present, a the first subbox of this type
* `[`_index_`]`: the subbox with index _index_

Examples:

    >>> parse_deref_path('.abcd[5]')
    ['abcd', 5]

## Function `parse_fields(bfr, copy_offsets=None, **kw)`

Parse an ISO14496 stream from the CornuCopyBuffer `bfr`,
yield top level OverBoxes.

Parameters:
* `bfr`: a `CornuCopyBuffer` provided the stream data,
  preferably seekable
* `discard_data`: whether to discard unparsed data, default `False`
* `copy_offsets`: callable to receive Box offsets

## Function `parse_tags(path, tag_prefix=None)`

Parse the tags from `path`.
Yield `(box,tags)` for each subbox with tags.

The optional `tag_prefix` parameter
may be specified to prefix each tag name with a prefix.
Other keyword arguments are passed to `parse()`
(typical example: `discard_data=True`).

## Class `PDINBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'pdin' Progressive Download Information box - ISO14496 section 8.1.3.

*`PDINBoxBody.PDInfo`*

*Method `PDINBoxBody.parse_fields(self, bfr, **kw)`*:
Gather the normal version information
and then the `(rate,initial_delay)` pairs of the data section
as the `pdinfo` field.

## Function `pick_boxbody_class(box_type: bytes)`

Infer a `BoxBody` subclass from the 4-byte bytes `box_type`.
Returns `FallbackBoxBody` for unimplemented types.

## Function `report(box, indent='', fp=None, indent_incr=None)`

Report some human friendly information about a box.

## Class `SMHDBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'smhd' Sound Media Headerbox - section 12.2.2.

*Method `SMHDBoxBody.parse_fields(self, bfr)`*:
Gather the `balance` field.

## Class `STCOBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'stco' Chunk Offset box - section 8.7.5.

*Property `STCOBoxBody.chunk_offsets`*:
Parse the `UInt32BE` chunk offsets from stashed buffer.

*Method `STCOBoxBody.parse_fields(self, bfr)`*:
Gather the `entry_count` and `chunk_offsets` fields.

## Class `STSCBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

'stsc' (Sample Table box - section 8.7.4.1.

*`STSCBoxBody.STSCEntry`*

*Property `STSCBoxBody.entries`*:
Parse the `STSCEntry` list into a list of `int`s.

*Method `STSCBoxBody.parse_fields(self, bfr)`*:
Gather the `entry_count` and `entries` fields.

## Class `STSZBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'stsz' Sample Size box - section 8.7.3.2.

*Property `STSZBoxBody.entry_sizes`*:
Parse the `UInt32BE` entry sizes from stashed buffer
into a list of `int`s.

*Method `STSZBoxBody.parse_fields(self, bfr)`*:
Gather the `sample_size`, `sample_count`, and `entry_sizes` fields.

*Method `STSZBoxBody.transcribe(self)`*:
Transcribe the `STSZBoxBody`.

## Class `STZ2BoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'stz2' Compact Sample Size box - section 8.7.3.3.

*Method `STZ2BoxBody.parse_fields(self, bfr)`*:
Gather the `field_size`, `sample_count` and `entry_sizes` fields.

*Method `STZ2BoxBody.transcribe(self)`*:
transcribe the STZ2BoxBody.

## Class `TimeStamp32(cs.binary.UInt32BE, cs.binary.UInt32BE, builtins.tuple, cs.binary.AbstractBinary, cs.binary.BinaryMixin, TimeStampMixin)`

The 32 bit form of an ISO14496 timestamp.

## Class `TimeStamp64(cs.binary.UInt64BE, cs.binary.UInt64BE, builtins.tuple, cs.binary.AbstractBinary, cs.binary.BinaryMixin, TimeStampMixin)`

The 64 bit form of an ISO14496 timestamp.

## Class `TimeStampMixin`

Methods to assist with ISO14496 timestamps.

*Property `TimeStampMixin.datetime`*:
This timestamp as an UTC datetime.

*Property `TimeStampMixin.unixtime`*:
This timestamp as a UNIX time (seconds since 1 January 1970).

## Class `TKHDBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'tkhd' Track Header box - ISO14496 section 8.2.2.

*`TKHDBoxBody.TKHDMatrix`*

## Class `TrackGroupTypeBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A TrackGroupTypeBoxBody contains a track group id - ISO14496 section 8.3.3.2.

*Method `TrackGroupTypeBoxBody.parse_fields(self, bfr)`*:
Gather the `track_group_id` field.

## Class `TrackReferenceTypeBoxBody(BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A TrackReferenceTypeBoxBody contains references to other tracks - ISO14496 section 8.3.3.2.

*Method `TrackReferenceTypeBoxBody.parse_fields(self, bfr)`*:
Gather the `track_ids` field.

## Class `TREFBoxBody(ContainerBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

Track Reference BoxBody, container for trackReferenceTypeBoxes - ISO14496 section 8.3.3.

## Class `TTSB_Sample(builtins.tuple)`

TTSB_Sample(count, delta)

*Property `TTSB_Sample.count`*:
Alias for field number 0

*Property `TTSB_Sample.delta`*:
Alias for field number 1

## Class `URL_BoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An 'url ' Data Entry URL BoxBody - section 8.7.2.1.

*Method `URL_BoxBody.parse_fields(self, bfr)`*:
Gather the `location` field.

## Class `URN_BoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An 'urn ' Data Entry URL BoxBody - section 8.7.2.1.

*Method `URN_BoxBody.parse_fields(self, bfr)`*:
Gather the `name` and `location` fields.

## Class `UTF8or16Field(cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

An ISO14496 UTF8 or UTF16 encoded string.

*Method `UTF8or16Field.parse(bfr)`*:
Gather optional BOM and then UTF8 or UTF16 string.

*Method `UTF8or16Field.transcribe(self)`*:
Transcribe the field suitably encoded.

## Class `VMHDBoxBody(FullBoxBody, BoxBody, cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin)`

A 'vmhd' Video Media Headerbox - section 12.1.2.

*`VMHDBoxBody.OpColor`*

*Method `VMHDBoxBody.parse_fields(self, bfr)`*:
Gather the `graphicsmode` and `opcolor` fields.

# Release Log



*Release 20220606*:
Update obsolete use of Tag.with_prefix.

*Release 20210306*:
* Huge refactor of the Box classes to the new Binary* classes from cs.binary.
* mp4: new "tags" subcommand to print the tags parsed from a file.
* BoxHeader: fix the definition of MAX_BOX_SIZE_32.
* BoxBody: new parse_boxes utility method to part the remainder of a Box as subBoxes.
* MP4.cmd_parse: run the main parse in discard_data=True mode.
* METABoxBody.__getattr__: fix ILST typo.
* MP4Command: update for new cs.cmdutils.BaseCommand API.
* Many small fixes and tweaks.

*Release 20200229*:
* ILST: recognise @cpy as copyright, sfID as itunes_store_country_code.
* ILST: new SFID_ISO_3166_1_ALPHA_3_CODE and STIK_MEDIA_TYPES providing context data for various field values, as yet unused.
* Make various list fields of some boxes deferred because they are expensive to parse (uses new cs.binary deferred_field).
* add_generic_sample_boxbody: drop __iter__, causes dumb iterators to parse the samples.
* ILST: iTunes "Date" metadata seem to contain plain years or ISO8601 datestamps.
* mp4 autotag: add -n (no action) and -p,--prefix (set tag prefix, default 'mp4') options.
* mp4 autotag: use "mp4." as the tag prefix.

*Release 20200130*:
* Parsing of ILST boxes (iTunes metadata).
* Command line: new "info" subcommand reporting metadata, "autotag" applying metadata to fstags.
* Box tree walk, ancestor, iteration.
* Assorted cleanups and internal changes.

*Release 20190220*:
parse_buffer yields instead of returns; some small bugfixes.

*Release 20180810*:
* parse_fd(): use a mmap to access the descriptor if a regular file and not discard_data;
* this lets us use the mmapped file as backing store for the data, a big win for the media sections.

*Release 20180805*:
Initial PyPI release.
