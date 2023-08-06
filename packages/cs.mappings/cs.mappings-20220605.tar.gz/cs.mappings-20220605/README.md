Facilities for mappings and objects associated with mappings.

*Latest release 20220605*:
* named_row_tuple et al: plumb a new optional snake_case parameter to snake case mixed case attribute names.
* Drop Python 2 support and the cs.py3 shims.

In particular `named_column_tuple(column_names)`,
a function returning a factory
for namedtuples subclasses derived from the supplied column names,
and `named_column_tuples(rows)`,
a function returning a namedtuple factory and an iterable of instances
containing the row data.
These are used by the `csv_import` and `xl_import` functions
from `cs.csvutils`.

## Class `AttrableMapping(builtins.dict, AttrableMappingMixin)`

A `dict` subclass using `AttrableMappingMixin`.

## Class `AttrableMappingMixin`

Provides a `__getattr__` which accesses the mapping value.

*Method `AttrableMappingMixin.__getattr__(self, attr)`*:
Unknown attributes are obtained from the mapping entries.

Note that this first consults `self.__dict__`.
For many classes that is redundant, but subclasses of
`dict` at least seem not to consult that with attribute
lookup, likely because a pure `dict` has no `__dict__`.

## Class `AttributableList(builtins.list)`

An `AttributableList` maps unimplemented attributes
onto the list members and returns you a new `AttributableList`
with the results, ready for a further dereference.

Example:

    >>> class C(object):
    ...   def __init__(self, i):
    ...     self.i = i
    >>> Cs = [ C(1), C(2), C(3) ]
    >>> AL = AttributableList( Cs )
    >>> print(AL.i)
    [1, 2, 3]

*Method `AttributableList.__init__(self, initlist=None, strict=False)`*:
Initialise the list.

The optional parameter `initlist` initialises the list
as for a normal list.

The optional parameter `strict`, if true, causes list elements
lacking the attribute to raise an AttributeError. If false,
list elements without the attribute are omitted from the results.

## Function `dicts_to_namedtuples(dicts, class_name, keys=None)`

Scan an iterable of `dict`s,
yield a sequence of `namedtuple`s derived from them.

Parameters:
* `dicts`: the `dict`s to scan and convert, an iterable
* `class_name`: the name for the new `namedtuple` class
* `keys`: optional iterable of `dict` keys of interest;
  if omitted then the `dicts` are scanned in order to learn the keys

Note that if `keys` is not specified
this generator prescans the `dicts` in order to learn their keys.
As a consequence, all the `dicts` will be kept in memory
and no `namedtuple`s will be yielded until after that prescan completes.

## Class `FallbackDict(collections.defaultdict, builtins.dict)`

A dictlike object that inherits from another dictlike object;
this is a convenience subclass of `defaultdict`.

## Class `IndexedMapping(IndexedSetMixin)`

Interface to a mapping with `IndexedSetMixin` style `.by_*` attributes.

*Method `IndexedMapping.__init__(self, mapping=None, pk='id')`*:
Initialise the `IndexedMapping`.

Parameters:
* `mapping`: the mapping to wrap; a new `dict` will be made if not specified
* `pk`: the primary key of the mapping, default `'id'`

*Method `IndexedMapping.add_backend(self, record)`*:
Save `record` in the mapping.

*Method `IndexedMapping.scan(self)`*:
The records from the mapping.

## Class `IndexedSetMixin`

A base mixin to provide `.by_`* attributes
which index records from an autoloaded backing store,
which might be a file or might be another related data structure.
The records are themselves key->value mappings, such as `dict`s.

The primary key name is provided by the `.IndexedSetMixin__pk`
class attribute, to be provided by subclasses.

Note that this mixin keeps the entire loadable mapping in memory.

Note that this does not see subsequent changes to loaded records
i.e. changing the value of some record[k]
does not update the index associated with the .by_k attribute.

Subclasses must provide the following attributes and methods:
* `IndexedSetMixin__pk`: the name of the primary key;
  it is an error for multiple records to have the same primary key
* `scan`: a generator method to scan the backing store
  and yield records, used for the inital load of the mapping
* `add_backend(record)`: add a new record to the backing store;
  this is called from the `.add(record)` method
  after indexing to persist the record in the backing store

See `UUIDNDJSONMapping` and `UUIDedDict` for an example subclass
indexing records from a newline delimited JSON file.

*Method `IndexedSetMixin.__len__(self)`*:
The length of the primary key mapping.

*Method `IndexedSetMixin.add(self, record, exists_ok=False)`*:
Add a record to the mapping.

This indexes the record against the various `by_`* indices
and then calls `self.add_backend(record)`
to save the record to the backing store.

*Method `IndexedSetMixin.scan(self)`*:
Scan the mapping records (themselves mappings) from the backing store,
which might be a file or another related data structure.
Yield each record as scanned.

*Property `IndexedSetMixin.scan_length`*:
The number of records encountered during the backend scan.

## Class `JSONableMappingMixin`

Provide `.from_json()`, `.as_json()` and `.append_ndjson()` methods,
and `__str__=as_json` and a `__repr__`.

*Method `JSONableMappingMixin.__str__(self)`*:
Return the `dict` transcribed as JSON.

If the instance's class has `json_default` or `json_separators` these
are used for the `default` and `separators` parameters of the `json.dumps()`
call.
Note that the default value of `separators` is `(',',':')`
which produces the most compact JSON form.

*Method `JSONableMappingMixin.append_ndjson(arg, *a, **kw)`*:
Append this object to `f`, a file or filename, as NDJSON.

*Method `JSONableMappingMixin.as_json(self)`*:
Return the `dict` transcribed as JSON.

If the instance's class has `json_default` or `json_separators` these
are used for the `default` and `separators` parameters of the `json.dumps()`
call.
Note that the default value of `separators` is `(',',':')`
which produces the most compact JSON form.

*Method `JSONableMappingMixin.from_json(js)`*:
Prepare a `dict` from JSON text.

If the class has `json_object_hook` or `json_object_pairs_hook`
attributes these are used as the `object_hook` and
`object_pairs_hook` parameters respectively of the `json.loads()` call.

## Class `MappingChain`

A mapping interface to a sequence of mappings.

It does not support `__setitem__` at present;
that is expected to be managed via the backing mappings.

*Method `MappingChain.__init__(self, mappings=None, get_mappings=None)`*:
Initialise the MappingChain.

Parameters:
* `mappings`: initial sequence of mappings, default None.
* `get_mappings`: callable to obtain the initial sequence of

Exactly one of `mappings` or `get_mappings` must be provided.

*Method `MappingChain.__getitem__(self, key)`*:
Return the first value for `key` found in the mappings.
Raise `KeyError` if the key in not found in any mapping.

*Method `MappingChain.get(self, key, default=None)`*:
Get the value associated with `key`, return `default` if missing.

*Method `MappingChain.keys(self)`*:
Return the union of the keys in the mappings.

## Class `MethodicalList(AttributableList, builtins.list)`

A MethodicalList subclasses a list and maps unimplemented attributes
into a callable which calls the corresponding method on each list members
and returns you a new `MethodicalList` with the results, ready for a
further dereference.

Example:

    >>> n = 1
    >>> class C(object):
    ...   def __init__(self):
    ...     global n
    ...     self.n = n
    ...     n += 1
    ...   def x(self):
    ...     return self.n
    ...
    >>> Cs=[ C(), C(), C() ]
    >>> ML = MethodicalList( Cs )
    >>> print(ML.x())
    [1, 2, 3]

*Method `MethodicalList.__init__(self, initlist=None, strict=False)`*:
Initialise the list.

The optional parameter `initlist` initialises the list
as for a normal list.

The optional parameter `strict`, if true, causes list elements
lacking the attribute to raise an AttributeError. If false,
list elements without the attribute are omitted from the results.

## Function `named_column_tuples(rows, class_name=None, column_names=None, computed=None, preprocess=None, mixin=None, snake_case=False)`

Process an iterable of data rows, usually with the first row being
column names.
Return a generated `namedtuple` factory (the row class)
and an iterable of instances of the namedtuples for each row.

Parameters:
* `rows`: an iterable of rows, each an iterable of data values.
* `class_name`: option class name for the namedtuple class
* `column_names`: optional iterable of column names used as the basis for
  the namedtuple. If this is not provided then the first row from
  `rows` is taken to be the column names.
* `computed`: optional mapping of str to functions of `self`
* `preprocess`: optional callable to modify CSV rows before
  they are converted into the namedtuple.  It receives a context
  object an the data row.
  It should return the row (possibly modified), or `None` to drop the
  row.
* `mixin`: an optional mixin class for the generated `namedtuple` subclass
  to provide extra methods or properties

The context object passed to `preprocess` has the following attributes:
* `.cls`: the generated namedtuple subclass;
  this is useful for obtaining things like the column names
  or column indices;
  this is `None` when preprocessing the header row, if any
* `.index`: attribute with the row's enumeration, which counts from `0`
* `.previous`: the previously accepted row's `namedtuple`,
  or `None` if there is no previous row;
  this is useful for differencing

Rows may be flat iterables in the same order as the column names
or mappings keyed on the column names.

If the column names contain empty strings they are dropped
and the corresponding data row entries are also dropped. This
is very common with spreadsheet exports with unused padding
columns.

Typical human readable column headings, also common in
speadsheet exports, are lowercased and have runs of whitespace
or punctuation turned into single underscores; trailing
underscores then get dropped.

Basic example:

    >>> data1 = [
    ...   ('a', 'b', 'c'),
    ...   (1, 11, "one"),
    ...   (2, 22, "two"),
    ... ]
    >>> rowtype, rows = named_column_tuples(data1)
    >>> print(list(rows))
    [NamedRow(a=1, b=11, c='one'), NamedRow(a=2, b=22, c='two')]

Human readable column headings:

    >>> data1 = [
    ...   ('Index', 'Value Found', 'Descriptive Text'),
    ...   (1, 11, "one"),
    ...   (2, 22, "two"),
    ... ]
    >>> rowtype, rows = named_column_tuples(data1)
    >>> print(list(rows))
    [NamedRow(index=1, value_found=11, descriptive_text='one'), NamedRow(index=2, value_found=22, descriptive_text='two')]

Rows which are mappings:

    >>> data1 = [
    ...   ('a', 'b', 'c'),
    ...   (1, 11, "one"),
    ...   {'a': 2, 'c': "two", 'b': 22},
    ... ]
    >>> rowtype, rows = named_column_tuples(data1)
    >>> print(list(rows))
    [NamedRow(a=1, b=11, c='one'), NamedRow(a=2, b=22, c='two')]

CSV export with unused padding columns:

    >>> data1 = [
    ...   ('a', 'b', 'c', '', ''),
    ...   (1, 11, "one"),
    ...   {'a': 2, 'c': "two", 'b': 22},
    ...   [3, 11, "three", '', 'dropped'],
    ... ]
    >>> rowtype, rows = named_column_tuples(data1, 'CSV_Row')
    >>> print(list(rows))
    [CSV_Row(a=1, b=11, c='one'), CSV_Row(a=2, b=22, c='two'), CSV_Row(a=3, b=11, c='three')]

A mixin class providing a `test1` method and a `test2` property:

    >>> class Mixin(object):
    ...   def test1(self):
    ...     return "test1"
    ...   @property
    ...   def test2(self):
    ...     return "test2"
    >>> data1 = [
    ...   ('a', 'b', 'c'),
    ...   (1, 11, "one"),
    ...   {'a': 2, 'c': "two", 'b': 22},
    ... ]
    >>> rowtype, rows = named_column_tuples(data1, mixin=Mixin)
    >>> rows = list(rows)
    >>> rows[0].test1()
    'test1'
    >>> rows[0].test2
    'test2'

## Function `named_row_tuple(*column_names, class_name=None, computed=None, column_map=None, snake_case=False, mixin=None)`

Return a `namedtuple` subclass factory derived from `column_names`.
The primary use case is using the header row of a spreadsheet
to key the data from the subsequent rows.

Parameters:
* `column_names`: an iterable of `str`, such as the heading columns
  of a CSV export
* `class_name`: optional keyword parameter specifying the class name
* `computed`: optional keyword parameter providing a mapping
  of `str` to functions of `self`; these strings are available
  via `__getitem__`
* `mixin`: an optional mixin class for the generated namedtuple subclass
  to provide extra methods or properties

The tuple's attributes are computed by converting all runs
of nonalphanumerics
(as defined by the `re` module's "\W" sequence)
to an underscore, lowercasing and then stripping
leading and trailing underscores.

In addition to the normal numeric indices, the tuple may
also be indexed by the attribute names or the column names.

The new class has the following additional attributes:
* `attributes_`: the attribute names of each tuple in order
* `names_`: the originating name strings
* `name_attributes_`: the computed attribute names corresponding to the
  `names`; there may be empty strings in this list
* `attr_of_`: a mapping of column name to attribute name
* `name_of_`: a mapping of attribute name to column name
* `index_of_`: a mapping of column names and attributes their tuple indices

Examples:

    >>> T = named_row_tuple('Column 1', '', 'Column 3', ' Column 4', 'Column 5 ', '', '', class_name='Example')
    >>> T.attributes_
    ['column_1', 'column_3', 'column_4', 'column_5']
    >>> row = T('val1', 'dropped', 'val3', 4, 5, 6, 7)
    >>> row
    Example(column_1='val1', column_3='val3', column_4=4, column_5=5)

## Class `PrefixedMappingProxy(RemappedMappingProxy)`

A proxy for another mapping
operating on keys commencing with a prefix.

*Method `PrefixedMappingProxy.keys(self)`*:
Yield the post-prefix suffix of the keys in `self.mapping`.

*Method `PrefixedMappingProxy.prefixify_subkey(subk, prefix)`*:
Return the external (prefixed) key from a subkey `subk`.

*Method `PrefixedMappingProxy.unprefixify_key(key, prefix)`*:
Return the internal subkey (unprefixed) from the external `key`.

## Class `RemappedMappingProxy`

A proxy for another mapping
with translation functions between the external keys
and the keys used inside the other mapping.

Example:

    >>> proxy = RemappedMappingProxy(
    ...   {},
    ...   lambda key: 'prefix.' + key,
    ...   lambda subkey: cutprefix('prefix.', subkey))
    >>> proxy['key'] = 1
    >>> proxy['key']
    1
    >>> proxy.mapping
    {'prefix.key': 1}
    >>> list(proxy.keys())
    ['key']
    >>> proxy.subkey('key')
    'prefix.key'
    >>> proxy.key('prefix.key')
    'key'

*Method `RemappedMappingProxy.get(self, key, default=None)`*:
Return the value for key `key` or `default`.

*Method `RemappedMappingProxy.key(self, *a, **kw)`*:
Return the external key for `subk`.

*Method `RemappedMappingProxy.keys(self, select_key=None)`*:
Yield the external keys.

*Method `RemappedMappingProxy.subkey(self, *a, **kw)`*:
Return the internal key for `key`.

## Class `SeenSet`

A set-like collection with optional backing store file.

*Method `SeenSet.add(self, s, foreign=False)`*:
Add the value `s` to the set.

Parameters:
* `s`: the value to add
* `foreign`: default `False`:
  whether the value came from an outside source,
  usually a third party addition to the backing file;
  this prevents appending the value to the backing file.

## Class `SeqMapUC_Attrs`

A wrapper for a mapping from keys
(matching the regular expression `^[A-Z][A-Z_0-9]*$`)
to tuples.

Attributes matching such a key return the first element
of the sequence (and requires the sequence to have exactly on element).
An attribute `FOOs` or `FOOes`
(ending in a literal 's' or 'es', a plural)
returns the sequence (`FOO` must be a key of the mapping).

## Class `StackableValues`

A collection of named stackable values with the latest value
available as an attribute.

*DEPRECATED*: I now recommend my `cs.context.stackattrs` context
manager for most uses; it may be applied to any object instead of
requiring use of this class.

Note that names conflicting with methods are not available
as attributes and must be accessed via `__getitem__`.
As a matter of practice, in addition to the mapping methods,
avoid names which are verbs or which begin with an underscore.

Example:

    >>> S = StackableValues()
    >>> print(S)
    StackableValues()
    >>> S.push('x', 1)
    >>> print(S)
    StackableValues(x=1)
    >>> print(S.x)
    1
    >>> S.push('x', 2)
    1
    >>> print(S.x)
    2
    >>> S.x = 3
    >>> print(S.x)
    3
    >>> S.pop('x')
    3
    >>> print(S.x)
    1
    >>> with S.stack(x=4):
    ...   print(S.x)
    ...
    4
    >>> print(S.x)
    1
    >>> S.update(x=5)
    {'x': 1}

*Method `StackableValues.__getattr__(self, attr)`*:
Convenience: present the top value of key `attr` as an attribute.

Note that attributes `push`, `pop` and the mapping method names
are shadowed by the instance methods
and should be accessed with the traditional `[]` key dereference.

*Method `StackableValues.__getitem__(self, key)`*:
Return the top value for `key` or raise `KeyError`.

*Method `StackableValues.__setattr__(self, attr, value)`*:
For nonunderscore attributes, replace the top element of the stack.

*Method `StackableValues.get(self, key, default=None)`*:
Get the top value for `key`, or `default`.

*Method `StackableValues.items(self)`*:
Mapping method returning an iterable of (name, value) tuples.

*Method `StackableValues.keys(self)`*:
Mapping method returning a list of the names.

*Method `StackableValues.pop(self, key)`*:
Pop and return the latest value for `key`.

*Method `StackableValues.push(self, key, value)`*:
Push a new `value` for `key`.
Return the previous value
or `None` if this is the first value for `key`.

*Method `StackableValues.stack(self, *a, **kw)`*:
Context manager which saves and restores the current state.
Any parameters are passed to `update()` after the save
but before the yield.

*Method `StackableValues.update(self, *ms, **kw)`*:
Update the mapping like `dict.update` method.
Return a mapping with the preupdate values
of the updated keys.

*Method `StackableValues.values(self)`*:
Mapping method returning an iterable of the values.

## Class `UC_Sequence(builtins.list)`

A tuple-of-nodes on which `.ATTRs` indirection can be done,
yielding another tuple-of-nodes or tuple-of-values.

*Method `UC_Sequence.__init__(self, Ns)`*:
Initialise from an iterable sequence.

## Class `UUIDedDict(builtins.dict, JSONableMappingMixin, AttrableMappingMixin)`

A handy `dict` subtype providing the basis for mapping classes
indexed by `UUID`s.

The `'uuid'` attribute is always a `UUID` instance.

*Method `UUIDedDict.__init__(self, _d=None, **kw)`*:
Initialise the `UUIDedDict`,
generating a `'uuid'` key value if omitted.

*Property `UUIDedDict.uuid`*:
A UUID from `self['uuid']`.

This does a sanity check that the stored value is a `UUID`,
but primarily exists to support the setter,
which promotes `str` to `UUID`, thus also validating UUID strings.

# Release Log



*Release 20220605*:
* named_row_tuple et al: plumb a new optional snake_case parameter to snake case mixed case attribute names.
* Drop Python 2 support and the cs.py3 shims.

*Release 20220318*:
Bump cs.sharedfile requirement to get an import fix.

*Release 20211208*:
* PrefixedMappingProxy: swap to_subkey/from_subkey prefix/unprefix actions, were backwards.
* PrefixedMappingProxy: make the key and subkey conversion methods public static methods for reuse.
* Assorted minor internal changes.

*Release 20210906*:
New RemappedMappingProxy with general subkey(key) and key(subkey) methods.

*Release 20210717*:
* New IndexedMapping: wrapper for another mapping providing LoadableMappingMixin stype .by_* attributes.
* Rename LoadableMappingMixin to IndexedSetMixin and make it abstract, rename .scan_mapping to .scan, .add_to_mapping to .add etc.

*Release 20210306*:
StackableValues: fix typo, make deprecation overt.

*Release 20210123*:
AttrableMappingMixin.__getattr__: some bugfixes.

*Release 20201228*:
New PrefixedMappingProxy presenting the keys of another mapping commencing with a prefix.

*Release 20201102*:
* StackableValues is obsolete, add recommendation for cs.context.stackattrs to the docstring.
* New AttrableMappingMixin with a __getattr__ which looks up unknown attributes as keys.
* New JSONableMappingMixin with methods for JSON actions: from_json, as_json, append_ndjson and a __str__ and __repr__.
* New LoadableMappingMixin to load .by_* attributes on demand.
* New AttrableMapping(dict, AttrableMappingMixin).

*Release 20200130*:
New dicts_to_namedtuples function to yield namedtuples from an iterable of dicts.

*Release 20191120*:
named_row_tuple: support None in a column name, as from Excel unfilled heading row entries

*Release 20190617*:
* StackableValues.push now returns the previous value.
* StackableValues.update has a signature like dict.update.
* StackableValues.pop removes entries when their stack becomes empty.
* StackableValues.stack: clean implementation of save/restore.
* StackableValues: avoid infinite recursion through ._fallback.
* StackableValues.keys now returns a list of the nonempty keys.
* Update doctests.

*Release 20190103*:
Documentation update.

*Release 20181231*:
* Bugfix for mapping of column names to row indices.
* New subclass._fallback method for when a stack is empty.

*Release 20180720*:
Initial PyPI release specificly for named_column_tuple and named_column_tuples.
