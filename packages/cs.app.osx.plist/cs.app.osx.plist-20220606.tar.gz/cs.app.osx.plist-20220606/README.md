Some simple MacOS plist facilities.
Supports binary plist files, which the stdlib `plistlib` module does not.

*Latest release 20220606*:
Initial PyPI release.

## Function `export_xml_to_plist(E, fp=None, fmt='binary1')`

Export the content of an `etree.Element` to a plist file.

Parameters:
* `E`: the source `etree.Element`.
* `fp`: the output file or filename (if a str).
* `fmt`: the output format, default `"binary1"`.
  The format must be a valid value for the `-convert` option of plutil(1).

## Function `import_as_etree(plist)`

Load an Apple plist and return an etree.Element.

Paramaters:
* `plist`: the source plist: data if `bytes`, filename if `str`,
  otherwise a file object open for binary read.

## Function `ingest_plist(plist, recurse=False, resolve=False)`

Ingest an Apple plist and return as a `PListDict`.
Trivial wrapper for `import_as_etree` and `ingest_plist_etree`.

Parameters:
* `recurse`: unpack any `bytes` objects as plists
* `resolve`: resolve unpacked `bytes` plists' `'$objects'` entries

## Function `ingest_plist_array(pa)`

Ingest a plist <array>, returning a Python list.

## Function `ingest_plist_dict(pd)`

Ingest a plist <dict> Element, returning a PListDict.

## Function `ingest_plist_elem(e)`

Ingest a plist `Element`, converting various types to native Python objects.
Unhandled types remain as the original `Element`.

## Function `ingest_plist_etree(plist_etree)`

Recursively a plist's `ElementTree` into a native Python structure.
This returns a `PListDict`, a mapping of the plists's top dict
with attribute access to key values.

## Function `is_iphone()`

Test if we're on an iPhone.

## Class `ObjectClassDefinition`

A representation of a "class" object, used in `resolve_object()`
for otherwise unrecognised objects which contain a `$classname` member.

## Class `ObjectClassInstance`

A representation of a "class instance", used in `resolve_object()`
for objects with a `$class` member.

*Method `ObjectClassInstance.items(self)`*:
pylint: disable=missing-function-docstring

*Method `ObjectClassInstance.keys(self)`*:
pylint: disable=missing-function-docstring

*Property `ObjectClassInstance.name`*:
The name from teh class definiton.

*Method `ObjectClassInstance.values(self)`*:
pylint: disable=missing-function-docstring

## Class `PListDict(builtins.dict)`

A mapping for a plist, subclassing `dict`, which also allows
access to the elements by attribute if that does not conflict
with a `dict` method.

## Function `readPlist(path, binary=False)`

An old routine I made to use inside my jailbroken iPhone.

## Function `resolve_object(objs, i)`

Resolve an object definition from structures like an iPhoto album
queryData object list.

## Function `writePlist(rootObj, path, binary=False)`

An old routine I made to use inside my jailbroken iPhone.

# Release Log



*Release 20220606*:
Initial PyPI release.
