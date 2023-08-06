Tags and sets of tags
with __format__ support and optional ontology information.

*Latest release 20220606*:
* Tag.parse_value: bugfix parse of float.
* TagSet.edit: accept optional comments parameter with addition header comment lines, be more tolerant of errors, avoid losing data on error.

See `cs.fstags` for support for applying these to filesystem objects
such as directories and files.

See `cs.sqltags` for support for databases of entities with tags,
not directly associated with filesystem objects.
This is suited to both log entries (entities with no "name")
and large collections of named entities;
both accept `Tag`s and can be searched on that basis.

All of the available complexity is optional:
you can use `Tag`s without bothering with `TagSet`s
or `TagsOntology`s.

This module contains the following main classes:
* `Tag`: an object with a `.name` and optional `.value` (default `None`)
  and also an optional reference `.ontology`
  for associating semantics with tag values.
  The `.value`, if not `None`, will often be a string,
  but may be any Python object.
  If you're using these via `cs.fstags`,
  the object will need to be JSON transcribeable.
* `TagSet`: a `dict` subclass representing a set of `Tag`s
  to associate with something;
  it also has setlike `.add` and `.discard` methods.
  As such it only supports a single `Tag` for a given tag name,
  but that tag value can of course be a sequence or mapping
  for more elaborate tag values.
* `TagsOntology`:
  a mapping of type names to `TagSet`s defining the type
  and also to entries for the metadata for specific per-type values.

Here's a simple example with some `Tag`s and a `TagSet`.

    >>> tags = TagSet()
    >>> # add a "bare" Tag named 'blue' with no value
    >>> tags.add('blue')
    >>> # add a "topic=tagging" Tag
    >>> tags.set('topic', 'tagging')
    >>> # make a "subtopic" Tag and add it
    >>> subtopic = Tag('subtopic', 'ontologies')
    >>> tags.add(subtopic)
    >>> # Tags have nice repr() and str()
    >>> subtopic
    Tag(name='subtopic',value='ontologies')
    >>> print(subtopic)
    subtopic=ontologies
    >>> # a TagSet also has a nice repr() and str()
    >>> tags
    TagSet:{'blue': None, 'topic': 'tagging', 'subtopic': 'ontologies'}
    >>> print(tags)
    blue subtopic=ontologies topic=tagging
    >>> tags2 = TagSet({'a': 1}, b=3, c=[1,2,3], d='dee')
    >>> tags2
    TagSet:{'a': 1, 'b': 3, 'c': [1, 2, 3], 'd': 'dee'}
    >>> print(tags2)
    a=1 b=3 c=[1,2,3] d=dee
    >>> # since you can print a TagSet to a file as a line of text
    >>> # you can get it back from a line of text
    >>> TagSet.from_line('a=1 b=3 c=[1,2,3] d=dee')
    TagSet:{'a': 1, 'b': 3, 'c': [1, 2, 3], 'd': 'dee'}
    >>> # because TagSets are dicts you can format strings with them
    >>> print('topic:{topic} subtopic:{subtopic}'.format_map(tags))
    topic:tagging subtopic:ontologies
    >>> # TagSets have convenient membership tests
    >>> # test for blueness
    >>> 'blue' in tags
    True
    >>> # test for redness
    >>> 'red' in tags
    False
    >>> # test for any "subtopic" tag
    >>> 'subtopic' in tags
    True
    >>> # test for subtopic=ontologies
    >>> print(subtopic)
    subtopic=ontologies
    >>> subtopic in tags
    True
    >>> # test for subtopic=libraries
    >>> subtopic2 = Tag('subtopic', 'libraries')
    >>> subtopic2 in tags
    False

## Ontologies

`Tag`s and `TagSet`s suffice to apply simple annotations to things.
However, an ontology brings meaning to those annotations.

See the `TagsOntology` class for implementation details,
access methods and more examples.

Consider a record about a movie, with these tags (a `TagSet`):

    title="Avengers Assemble"
    series="Avengers (Marvel)"
    cast={"Scarlett Johansson":"Black Widow (Marvel)"}

where we have the movie title,
a name for the series in which it resides,
and a cast as an association of actors with roles.

An ontology lets us associate implied types and metadata with these values.

Here's an example ontology supporting the above `TagSet`:

    type.cast type=dict key_type=person member_type=character description="members of a production"
    type.character description="an identified member of a story"
    type.series type=str
    character.marvel.black_widow type=character names=["Natasha Romanov"]
    person.scarlett_johansson fullname="Scarlett Johansson" bio="Known for Black Widow in the Marvel stories."

The type information for a `cast`
is defined by the ontology entry named `type.cast`,
which tells us that a `cast` `Tag` is a `dict`,
whose keys are of type `person`
and whose values are of type `character`.
(The default type is `str`.)

To find out the underlying type for a `character`
we look that up in the ontology in turn;
because it does not have a specified `type` `Tag`, it it taken to be a `str`.

Having the types for a `cast`,
it is now possible to look up the metadata for the described cast members.

The key `"Scarlett Johansson"` is a `person`
(from the type definition of `cast`).
The ontology entry for her is named `person.scarlett_johansson`
which is computed as:
* `person`: the type name
* `scarlett_johansson`: obtained by downcasing `"Scarlett Johansson"`
  and replacing whitespace with an underscore.
  The full conversion process is defined
  by the `TagsOntology.value_to_tag_name` function.

The key `"Black Widow (Marvel)"` is a `character`
(again, from the type definition of `cast`).
The ontology entry for her is named `character.marvel.black_widow`
which is computed as:
* `character`: the type name
* `marvel.black_widow`: obtained by downcasing `"Black Widow (Marvel)"`,
  replacing whitespace with an underscore,
  and moving a bracketed suffix to the front as an unbracketed prefix.
  The full conversion process is defined
  by the `TagsOntology.value_to_tag_name` function.

## Format Strings

You can just use `str.format_map` as shown above
for the direct values in a `TagSet`,
since it subclasses `dict`.

However, `TagSet`s also subclass `cs.lex.FormatableMixin`
and therefore have a richer `format_as` method which has an extended syntax
for the format component.
Command line tools like `fstags` use this for output format specifications.

An example:

    >>> # an ontology specifying the type for a colour
    >>> # and some information about the colour "blue"
    >>> ont = TagsOntology(
    ...   {
    ...       'type.colour':
    ...       TagSet(description="a colour, a hue", type="str"),
    ...       'colour.blue':
    ...       TagSet(
    ...           url='https://en.wikipedia.org/wiki/Blue',
    ...           wavelengths='450nm-495nm'
    ...       ),
    ...   }
    ... )
    >>> # tag set with a "blue" tag, using the ontology above
    >>> tags = TagSet(colour='blue', labels=['a', 'b', 'c'], size=9, _ontology=ont)
    >>> tags.format_as('The colour is {colour}.')
    'The colour is blue.'
    >>> # format a string about the tags showing some metadata about the colour
    >>> tags.format_as('Information about the colour may be found here: {colour:metadata.url}')
    'Information about the colour may be found here: https://en.wikipedia.org/wiki/Blue'

## Function `as_unixtime(*a, **kw)`

Convert a tag value to a UNIX timestamp.

This accepts `int`, `float` (already a timestamp)
and `date` or `datetime`
(use `datetime.timestamp() for a nonnaive `datetime`,
otherwise `time.mktime(tag_value.time_tuple())`,
which assumes the local time zone).

## Class `BaseTagSets(cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, collections.abc.MutableMapping, collections.abc.Mapping, collections.abc.Collection, collections.abc.Sized, collections.abc.Iterable, collections.abc.Container)`

Base class for collections of `TagSet` instances
such as `cs.fstags.FSTags` and `cs.sqltags.SQLTags`.

Examples of this include:
* `cs.fstags.FSTags`: a mapping of filesystem paths to their associated `TagSet`
* `cs.sqltags.SQLTags`: a mapping of names to `TagSet`s stored in an SQL database

Subclasses must implement:
* `get(name,default=None)`: return the `TagSet` associated
  with `name`, or `default`.
* `__setitem__(name,tagset)`: associate a `TagSet`with the key `name`;
  this is called by the `__missing__` method with a newly created `TagSet`.
* `keys(self)`: return an iterable of names

Subclasses may reasonably want to override the following:
* `startup_shutdown(self)`: context manager to allocate and release any
  needed resources such as database connections

Subclasses may implement:
* `__len__(self)`: return the number of names

The `TagSet` factory used to fetch or create a `TagSet` is
named `TagSetClass`. The default implementation honours two
class attributes:
* `TAGSETCLASS_DEFAULT`: initially `TagSet`
* `TAGSETCLASS_PREFIX_MAPPING`: a mapping of type names to `TagSet` subclasses

The type name of a `TagSet` name is the first dotted component.
For example, `artist.nick_cave` has the type name `artist`.
A subclass of `BaseTagSets` could utiliise an `ArtistTagSet` subclass of `TagSet`
and provide:

    TAGSETCLASS_PREFIX_MAPPING = {
      'artist': ArtistTagSet,
    }

in its class definition. Accesses to `artist.`* entities would
result in `ArtistTagSet` instances and access to other enitities
would result in ordinary `TagSet` instances.

*Method `BaseTagSets.__init__(self, *, ontology=None)`*:
Initialise the collection.

*`BaseTagSets.TAGSETCLASS_DEFAULT`*

*Method `BaseTagSets.TagSetClass(self, *a, **kw)`*:
Factory to create a new `TagSet` from `name`.

*Method `BaseTagSets.__contains__(self, name: str)`*:
Test whether `name` is present in the underlying mapping.

*Method `BaseTagSets.__getitem__(self, name: str)`*:
Obtain the `TagSet` associated with `name`.

If `name` is not presently mapped,
return `self.__missing__(name)`.

*Method `BaseTagSets.__iter__(self)`*:
Iteration returns the keys.

*Method `BaseTagSets.__len__(self)`*:
Return the length of the underlying mapping.

*Method `BaseTagSets.__missing__(self, *a, **kw)`*:
Like `dict`, the `__missing__` method may autocreate a new `TagSet`.

This is called from `__getitem__` if `name` is missing
and uses the factory `cls.default_factory`.
If that is `None` raise `KeyError`,
otherwise call `self.default_factory(name,**kw)`.
If that returns `None` raise `KeyError`,
otherwise save the entity under `name` and return the entity.

*Method `BaseTagSets.__setitem__(self, name, te)`*:
Save `te` in the backend under the key `name`.

*Method `BaseTagSets.add(self, name: str, **kw)`*:
Return a new `TagSet` associated with `name`,
which should not already be in use.

*Method `BaseTagSets.default_factory(self, name: str)`*:
Create a new `TagSet` named `name`.

*Method `BaseTagSets.edit(self, *, select_tagset=None, **kw)`*:
Edit the `TagSet`s.

Parameters:
* `select_tagset`: optional callable accepting a `TagSet`
  which tests whether it should be included in the `TagSet`s
  to be edited
Other keyword arguments are passed to `Tag.edit_tagsets`.

*Method `BaseTagSets.get(self, name: str, default=None)`*:
Return the `TagSet` associated with `name`,
or `default` if there is no such entity.

*Method `BaseTagSets.items(self, *, prefix=None)`*:
Generator yielding `(key,value)` pairs,
optionally constrained to keys starting with `prefix+'.'`.

*Method `BaseTagSets.keys(self, *, prefix=None)`*:
Return the keys starting with `prefix+'.'`
or all keys if `prefix` is `None`.

*Method `BaseTagSets.subdomain(self, subname: str)`*:
Return a proxy for this `BaseTagSets` for the `name`s
starting with `subname+'.'`.

*Method `BaseTagSets.values(self, *, prefix=None)`*:
Generator yielding the mapping values (`TagSet`s),
optionally constrained to keys starting with `prefix+'.'`.

## Class `MappingTagSets(BaseTagSets, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, collections.abc.MutableMapping, collections.abc.Mapping, collections.abc.Collection, collections.abc.Sized, collections.abc.Iterable, collections.abc.Container)`

A `BaseTagSets` subclass using an arbitrary mapping.

If no mapping is supplied, a `dict` is created for the purpose.

Example:

    >>> tagsets = MappingTagSets()
    >>> list(tagsets.keys())
    []
    >>> tagsets.get('foo')
    >>> tagsets['foo'] = TagSet(bah=1, zot=2)
    >>> list(tagsets.keys())
    ['foo']
    >>> tagsets.get('foo')
    TagSet:{'bah': 1, 'zot': 2}
    >>> list(tagsets.keys(prefix='foo'))
    ['foo']
    >>> list(tagsets.keys(prefix='bah'))
    []

*Method `MappingTagSets.__delitem__(self, name)`*:
Delete the `TagSet` named `name`.

*Method `MappingTagSets.__setitem__(self, name, te)`*:
Save `te` in the backend under the key `name`.

*Method `MappingTagSets.keys(self, *, prefix: Optional[str] = None)`*:
Return an iterable of the keys commencing with `prefix`
or all keys if `prefix` is `None`.

## Class `RegexpTagRule`

A regular expression based `Tag` rule.

This applies a regular expression to a string
and returns inferred `Tag`s.

*Method `RegexpTagRule.infer_tags(self, *a, **kw)`*:
Apply the rule to the string `s`, return a list of `Tag`s.

## Function `selftest(argv)`

Run some ad hoc self tests.

## Class `Tag(Tag, builtins.tuple, cs.lex.FormatableMixin, cs.lex.FormatableFormatter, string.Formatter)`

A `Tag` has a `.name` (`str`) and a `.value`
and an optional `.ontology`.

The `name` must be a dotted identifier.

Terminology:
* A "bare" `Tag` has a `value` of `None`.
* A "naive" `Tag` has an `ontology` of `None`.

The constructor for a `Tag` is unusual:
* both the `value` and `ontology` are optional,
  defaulting to `None`
* if `name` is a `str` then we always construct a new `Tag`
  with the suppplied values
* if `name` is not a `str`
  it should be a `Tag`like object to promote;
  it is an error if the `value` parameter is not `None`
  in this case
* an optional `prefix` may be supplied
  which is prepended to `name` with a dot (`'.'`) if not empty

The promotion process is as follows:
* if `name` is a `Tag` subinstance
  then if the supplied `ontology` is not `None`
  and is not the ontology associated with `name`
  then a new `Tag` is made,
  otherwise the original `Tag` is returned unchanged
* otherwise a new `Tag` is made from `name`
  using its `.value`
  and overriding its `.ontology`
  if the `ontology` parameter is not `None`

Examples:

    >>> ont = TagsOntology({'colour.blue': TagSet(wavelengths='450nm-495nm')})
    >>> tag0 = Tag('colour', 'blue')
    >>> tag0
    Tag(name='colour',value='blue')
    >>> tag = Tag(tag0)
    >>> tag
    Tag(name='colour',value='blue')
    >>> tag = Tag(tag0, ontology=ont)
    >>> tag # doctest: +ELLIPSIS
    Tag(name='colour',value='blue',ontology=...)
    >>> tag = Tag(tag0, prefix='surface')
    >>> tag
    Tag(name='surface.colour',value='blue')

*Method `Tag.__init__(self, *a, **kw)`*:
Dummy `__init__` to avoid `FormatableMixin.__init__`
because we subclass `namedtuple` which has no `__init__`.

*`Tag.__hash__`*

*Method `Tag.__str__(self)`*:
Encode `name` and `value`.

*Method `Tag.alt_values(self, value_tag_name=None)`*:
Return a list of alternative values for this `Tag`
on the premise that each has a metadata entry.

*Property `Tag.basetype`*:
The base type name for this tag.
Returns `None` if there is no ontology.

This calls `self.onotology.basetype(self.name)`.
The basetype is the endpoint of a cascade down the defined types.

For example, this might tell us that a `Tag` `role="Fred"`
has a basetype `"str"`
by cascading through a hypothetical chain `role`->`character`->`str`:

    type.role type=character
    type.character type=str

*Method `Tag.from_arg(arg, offset=0, ontology=None)`*:
Parse a `Tag` from the string `arg` at `offset` (default `0`).
where `arg` is known to be entirely composed of the value,
such as a command line argument.

This calls the `from_str` method with `fallback_parse` set
to gather then entire tail of the supplied string `arg`.

*Method `Tag.from_str(s, offset=0, ontology=None, fallback_parse=None)`*:
Parse a `Tag` definition from `s` at `offset` (default `0`).

*Method `Tag.from_str2(s, offset=0, *, ontology, extra_types=None, fallback_parse=None)`*:
Parse tag_name[=value], return `(Tag,offset)`.

*Method `Tag.is_valid_name(name)`*:
Test whether a tag name is valid: a dotted identifier.

*Method `Tag.key_metadata(self, *a, **kw)`*:
Return the metadata definition for `key`.

The metadata `TagSet` is obtained from the ontology entry
*type*`.`*key_tag_name*
where *type* is the `Tag`'s `key_type`
and *key_tag_name* is the key converted
into a dotted identifier by `TagsOntology.value_to_tag_name`.

*Property `Tag.key_type`*:
The type name for members of this tag.

This is required if `.value` is a mapping.

*Property `Tag.key_typedef`*:
The typedata definition for this `Tag`'s keys.

This is for `Tag`s which store mappings,
for example a movie cast, mapping actors to roles.

The name of the member type comes from
the `key_type` entry from `self.typedata`.
That name is then looked up in the ontology's types.

*Method `Tag.matches(self, name, value=None, *a, **kw)`*:
Test whether this `Tag` matches `(tag_name,value)`.

*Method `Tag.member_metadata(self, *a, **kw)`*:
Return the metadata definition for self[member_key].

The metadata `TagSet` is obtained from the ontology entry
*type*`.`*member_tag_name*
where *type* is the `Tag`'s `member_type`
and *member_tag_name* is the member value converted
into a dotted identifier by `TagsOntology.value_to_tag_name`.

*Property `Tag.member_type`*:
The type name for members of this tag.

This is required if `.value` is a sequence or mapping.

*Property `Tag.member_typedef`*:
The typedata definition for this `Tag`'s members.

This is for `Tag`s which store mappings or sequences,
for example a movie cast, mapping actors to roles,
or a list of scenes.

The name of the member type comes from
the `member_type` entry from `self.typedata`.
That name is then looked up in the ontology's types.

*Property `Tag.meta`*:
Shortcut property for the metadata `TagSet`.

*Method `Tag.metadata(self, *, ontology=None, convert=None)`*:
Fetch the metadata information about this specific tag value,
derived through the `ontology` from the tag name and value.
The default `ontology` is `self.ontology`.

For a scalar type (`int`, `float`, `str`) this is the ontology `TagSet`
for `self.value`.

For a sequence (`list`) this is a list of the metadata
for each member.

For a mapping (`dict`) this is mapping of `key->metadata`.

*Method `Tag.parse_name(s, offset=0)`*:
Parse a tag name from `s` at `offset`: a dotted identifier.

*Method `Tag.parse_value(s, offset=0, extra_types=None, fallback_parse=None)`*:
Parse a value from `s` at `offset` (default `0`).
Return the value, or `None` on no data.

The optional `extra_types` parameter may be an iterable of
`(type,from_str,to_str)` tuples where `from_str` is a
function which takes a string and returns a Python object
(expected to be an instance of `type`).
The default comes from `cls.EXTRA_TYPES`.
This supports storage of nonJSONable values in text form.

The optional `fallback_parse` parameter
specifies a parse function accepting `(s,offset)`
and returning `(parsed,new_offset)`
where `parsed` is text from `s[offset:]`
and `new_offset` is where the parse stopped.
The default is `cs.lex.get_nonwhite`
to gather nonwhitespace characters,
intended support *tag_name*`=`*bare_word*
in human edited tag files.

The core syntax for values is JSON;
value text commencing with any of `'"'`, `'['` or `'{'`
is treated as JSON and decoded directly,
leaving the offset at the end of the JSON parse.

Otherwise all the nonwhitespace at this point is collected
as the value text,
leaving the offset at the next whitespace character
or the end of the string.
The text so collected is then tried against the `from_str`
function of each `extra_types`;
the first successful parse is accepted as the value.
If no extra type match,
the text is tried against `int()` and `float()`;
if one of these parses the text and `str()` of the result round trips
to the original text
then that value is used.
Otherwise the text itself is kept as the value.

*Method `Tag.transcribe_value(value, extra_types=None, json_options=None)`*:
Transcribe `value` for use in `Tag` transcription.

The optional `extra_types` parameter may be an iterable of
`(type,from_str,to_str)` tuples where `to_str` is a
function which takes a string and returns a Python object
(expected to be an instance of `type`).
The default comes from `cls.EXTRA_TYPES`.

If `value` is an instance of `type`
then the `to_str` function is used to transcribe the value
as a `str`, which should not include any whitespace
(because of the implementation of `parse_value`).
If there is no matching `to_str` function,
`cls.JSON_ENCODER.encode` is used to transcribe `value`.

This supports storage of nonJSONable values in text form.

*Property `Tag.typedef`*:
The defining `TagSet` for this tag's name.

This is how its type is defined,
and is obtained from:
`self.ontology['type.'+self.name]`

Basic `Tag`s often do not need a type definition;
these are only needed for structured tag values
(example: a mapping of cast members)
or when a `Tag` name is an alias for another type
(example: a cast member name might be an `actor`
which in turn might be a `person`).

For example, a `Tag` `colour=blue`
gets its type information from the `type.colour` entry in an ontology;
that entry is just a `TagSet` with relevant information.

## Function `tag_or_tag_value(*da, **dkw)`

A decorator for functions or methods which may be called as:

    func(name[,value])

or as:

    func(Tag)

The optional decorator argument `no_self` (default `False`)
should be supplied for plain functions
as they have no leading `self` parameter to accomodate.

Example:

    @tag_or_tag_value
    def add(self, tag_name, value, *, verbose=None):

This defines a `.add()` method
which can be called with `name` and `value`
or with single `Tag`like object
(something with `.name` and `.value` attributes),
for example:

    tags = TagSet()
    ....
    tags.add('colour', 'blue')
    ....
    tag = Tag('size', 9)
    tags.add(tag)

## Class `TagBasedTest(TagBasedTest, builtins.tuple, TagSetCriterion)`

A test based on a `Tag`.

Attributes:
* `spec`: the source text from which this choice was parsed,
  possibly `None`
* `choice`: the apply/reject flag
* `tag`: the `Tag` representing the criterion
* `comparison`: an indication of the test comparison

The following comparison values are recognised:
* `None`: test for the presence of the `Tag`
* `'='`: test that the tag value equals `tag.value`
* `'<'`: test that the tag value is less than `tag.value`
* `'<='`: test that the tag value is less than or equal to `tag.value`
* `'>'`: test that the tag value is greater than `tag.value`
* `'>='`: test that the tag value is greater than or equal to `tag.value`
* `'~/'`: test if the tag value as a regexp is present in `tag.value`
* '~': test if a matching tag value is present in `tag.value`

*Method `TagBasedTest.by_tag_value(name, value=None, *a, **kw)`*:
Return a `TagBasedTest` based on a `Tag` or `tag_name,tag_value`.

*Method `TagBasedTest.match_tagged_entity(self, te: 'TagSet') -> bool`*:
Test against the `Tag`s in `tags`.

*Note*: comparisons when `self.tag.name` is not in `tags`
always return `False` (possibly inverted by `self.choice`).

*Method `TagBasedTest.parse(s, offset=0, delim=None)`*:
Parse *tag_name*[{`<`|`<=`|'='|'>='|`>`|'~'}*value*]
and return `(dict,offset)`
where the `dict` contains the following keys and values:
* `tag`: a `Tag` embodying the tag name and value
* `comparison`: an indication of the test comparison

## Class `TagFile(cs.fs.FSPathBasedSingleton, cs.obj.SingletonMixin, cs.fs.HasFSPath, BaseTagSets, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, collections.abc.MutableMapping, collections.abc.Mapping, collections.abc.Collection, collections.abc.Sized, collections.abc.Iterable, collections.abc.Container)`

A reference to a specific file containing tags.

This manages a mapping of `name` => `TagSet`,
itself a mapping of tag name => tag value.

*Method `TagFile.__setitem__(self, name, te)`*:
Set item `name` to `te`.

*Method `TagFile.get(self, name, default=None)`*:
Get from the tagsets.

*Method `TagFile.is_modified(self)`*:
Test whether this `TagSet` has been modified.

*Method `TagFile.keys(self, *, prefix=None)`*:
`tagsets.keys`

If the options `prefix` is supplied,
yield only those keys starting with `prefix`.

*Method `TagFile.load_tagsets(filepath, ontology, extra_types=None)`*:
Load `filepath` and return `(tagsets,unparsed)`.

The returned `tagsets` are a mapping of `name`=>`tag_name`=>`value`.
The returned `unparsed` is a list of `(lineno,line)`
for lines which failed the parse (excluding the trailing newline).

*Property `TagFile.names`*:
The names from this `FSTagsTagFile` as a list.

*Method `TagFile.parse_tags_line(*a, **kw)`*:
Parse a "name tags..." line as from a `.fstags` file,
return `(name,TagSet)`.

*Method `TagFile.save(self, extra_types=None)`*:
Save the tag map to the tag file if modified.

*Method `TagFile.save_tagsets(filepath, tagsets, unparsed, extra_types=None)`*:
Save `tagsets` and `unparsed` to `filepath`.

This method will create the required intermediate directories
if missing.

This method *does not* clear the `.modified` attribute of the `TagSet`s
because it does not know it is saving to the `Tagset`'s primary location.

*Method `TagFile.shutdown(self)`*:
Save the tagsets if modified.

*Method `TagFile.startup(self)`*:
No special startup.

*Method `TagFile.tags_line(name, tags, extra_types=None)`*:
Transcribe a `name` and its `tags` for use as a `.fstags` file line.

*Property `TagFile.tagsets`*:
The tag map from the tag file,
a mapping of name=>`TagSet`.

This is loaded on demand.

*Method `TagFile.update(self, name, tags, *, prefix=None, verbose=None)`*:
Update the tags for `name` from the supplied `tags`
as for `Tagset.update`.

## Class `TagsCommandMixin`

Utility methods for `cs.cmdutils.BaseCommand` classes working with tags.

Optional subclass attributes:
* `TAGSET_CRITERION_CLASS`: a `TagSetCriterion` duck class,
  default `TagSetCriterion`.
  For example, `cs.sqltags` has a subclass
  with an `.extend_query` method for computing an SQL JOIN
  used in searching for tagged entities.

*`TagsCommandMixin.TagAddRemove`*

*Method `TagsCommandMixin.parse_tag_addremove(arg, offset=0)`*:
Parse `arg` as an add/remove tag specification
of the form [`-`]*tag_name*[`=`*value*].
Return `(remove,Tag)`.

Examples:

    >>> TagsCommandMixin.parse_tag_addremove('a')
    TagAddRemove(remove=False, tag=Tag(name='a',value=None))
    >>> TagsCommandMixin.parse_tag_addremove('-a')
    TagAddRemove(remove=True, tag=Tag(name='a',value=None))
    >>> TagsCommandMixin.parse_tag_addremove('a=1')
    TagAddRemove(remove=False, tag=Tag(name='a',value=1))
    >>> TagsCommandMixin.parse_tag_addremove('-a=1')
    TagAddRemove(remove=True, tag=Tag(name='a',value=1))
    >>> TagsCommandMixin.parse_tag_addremove('-a="foo bah"')
    TagAddRemove(remove=True, tag=Tag(name='a',value='foo bah'))
    >>> TagsCommandMixin.parse_tag_addremove('-a=foo bah')
    TagAddRemove(remove=True, tag=Tag(name='a',value='foo bah'))

*Method `TagsCommandMixin.parse_tag_choices(argv)`*:
Parse `argv` as an iterable of [`!`]*tag_name*[`=`*tag_value`] `Tag`
additions/deletions.

*Method `TagsCommandMixin.parse_tagset_criteria(argv, tag_based_test_class=None)`*:
Parse tag specifications from `argv` until an unparseable item is found.
Return `(criteria,argv)`
where `criteria` is a list of the parsed criteria
and `argv` is the remaining unparsed items.

Each item is parsed via
`cls.parse_tagset_criterion(item,tag_based_test_class)`.

*Method `TagsCommandMixin.parse_tagset_criterion(arg, tag_based_test_class=None)`*:
Parse `arg` as a tag specification
and return a `tag_based_test_class` instance
via its `.from_str` factory method.
Raises `ValueError` in a misparse.
The default `tag_based_test_class`
comes from `cls.TAGSET_CRITERION_CLASS`,
which itself defaults to class `TagSetCriterion`.

The default `TagSetCriterion.from_str` recognises:
* `-`*tag_name*: a negative requirement for *tag_name*
* *tag_name*[`=`*value*]: a positive requirement for a *tag_name*
  with optional *value*.

## Class `TagSet(builtins.dict, cs.dateutils.UNIXTimeMixin, cs.lex.FormatableMixin, cs.lex.FormatableFormatter, string.Formatter, cs.mappings.AttrableMappingMixin)`

A setlike class associating a set of tag names with values.

This actually subclasses `dict`, so a `TagSet` is a direct
mapping of tag names to values.
It accepts attribute access to simple tag values when they
do not conflict with the class methods;
the reliable method is normal item access.

*NOTE*: iteration yields `Tag`s, not dict keys.

Also note that all the `Tags` from a `TagSet`
share its ontology.

Subclasses should override the `set` and `discard` methods;
the `dict` and mapping methods
are defined in terms of these two basic operations.

`TagSet`s have a few special properties:
* `id`: a domain specific identifier;
  this may reasonably be `None` for entities
  not associated with database rows;
  the `cs.sqltags.SQLTags` class associates this
  with the database row id.
* `name`: the entity's name;
  a read only alias for the `'name'` `Tag`.
  The `cs.sqltags.SQLTags` class defines "log entries"
  as `TagSet`s with no `name`.
* `unixtime`: a UNIX timestamp,
  a `float` holding seconds since the UNIX epoch
  (midnight, 1 January 1970 UTC).
  This is typically the row creation time
  for entities associated with database rows,
  but usually the event time for `TagSet`s describing an event.

Because ` TagSet` subclasses `cs.mappings.AttrableMappingMixin`
you can also access tag values as attributes
*provided* that they do not conflict with instance attributes
or class methods or properties.
The `TagSet` class defines the class attribute `ATTRABLE_MAPPING_DEFAULT`
as `None` which causes attribute access to return `None`
for missing tag names.
This supports code like:

    if tags.title:
        # use the title in something
    else:
        # handle a missing title tag

*Method `TagSet.__init__(self, *a, **kw)`*:
Initialise the `TagSet`.

Parameters:
* positional parameters initialise the `dict`
  and are passed to `dict.__init__`
* `_id`: optional identity value for databaselike implementations
* `_ontology`: optional `TagsOntology to use for this `TagSet`
* other alphabetic keyword parameters are also used to initialise the
  `dict` and are passed to `dict.__init__`

*Method `TagSet.__contains__(self, tag)`*:
Test for a tag being in this `TagSet`.

If the supplied `tag` is a `str` then this test
is for the presence of `tag` in the keys.

Otherwise,
for each tag `T` in the tagset
test `T.matches(tag)` and return `True` on success.
The default `Tag.matches` method compares the tag name
and if the same,
returns true if `tag.value` is `None` (basic "is the tag present" test)
and otherwise true if `tag.value==T.value` (basic "tag value equality" test).

Otherwise return `False`.

*Method `TagSet.__getattr__(self, attr)`*:
Support access to dotted name attributes.

The following attribute accesses are supported:

If `attr` is a key, return `self[attr]`.

If `self.auto_infer(attr)` does not raise `ValueError`,
return that value.

If this `TagSet` has an ontology
and `attr looks like *typename*`_`*fieldname*
and *typename* is a key,
look up the metadata for the `Tag` value
and return the metadata's *fieldname* key.
This also works for plural values.

For example if a `TagSet` has the tag `artists=["fred","joe"]`
and `attr` is `artist_names`
then the metadata entries for `"fred"` and `"joe"` looked up
and their `artist_name` tags are returned,
perhaps resulting in the list
`["Fred Thing","Joe Thang"]`.

If there are keys commencing with `attr+'.'`
then this returns a view of those keys
so that a subsequent attribute access can access one of those keys.

Otherwise, a superclass attribute access is performed.

Example:

    >>> tags=TagSet(a=1,b=2)
    >>> tags.a
    1
    >>> tags.c
    >>> tags['c.z']=9
    >>> tags['c.x']=8
    >>> tags
    TagSet:{'a': 1, 'b': 2, 'c.z': 9, 'c.x': 8}
    >>> tags.c
    TagSetPrefixView:c.{'z': 9, 'x': 8}
    >>> tags.c.z
    9

However, this is not supported when there is a tag named `'c'`
because `tags.c` has to return the `'c'` tag value:

    >>> tags=TagSet(a=1,b=2,c=3)
    >>> tags.a
    1
    >>> tags.c
    3
    >>> tags['c.z']=9
    >>> tags.c.z
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'int' object has no attribute 'z'

*Method `TagSet.__iter__(self, prefix=None, ontology=None)`*:
Yield the tag data as `Tag`s.

*Method `TagSet.__setattr__(self, attr, value)`*:
Attribute based `Tag` access.

If `attr` is private or is in `self.__dict__` then that is updated,
supporting "normal" attributes set on the instance.
Otherwise the `Tag` named `attr` is set to `value`.

The `__init__` methods of subclasses should do something like this
(from `TagSet.__init__`)
to set up the ordinary instance attributes
which are not to be treated as `Tag`s:

    self.__dict__.update(id=_id, ontology=_ontology, modified=False)

*Method `TagSet.__str__(self)`*:
The `TagSet` suitable for writing to a tag file.

*Method `TagSet.add(self, name, value=None, *a, **kw)`*:
Adding a `Tag` calls the class `set()` method.

*Method `TagSet.as_dict(self)`*:
Return a `dict` mapping tag name to value.

*Method `TagSet.as_tags(self, prefix=None, ontology=None)`*:
Yield the tag data as `Tag`s.

*Property `TagSet.auto`*:
The automatic namespace.
Here we can refer to dotted tag names directly as attributes.

*Method `TagSet.auto_infer(self, *a, **kw)`*:
The default inference implementation.

This should return a value if `attr` is inferrable
and raise `ValueError` if not.

The default implementation returns the direct tag value for `attr`
if present.

*Property `TagSet.csvrow`*:
This `TagSet` as a list useful to a `csv.writer`.
The inverse of `from_csvrow`.

*Method `TagSet.discard(self, name, value=None, *a, **kw)`*:
Discard the tag matching `(tag_name,value)`.
Return a `Tag` with the old value,
or `None` if there was no matching tag.

Note that if the tag value is `None`
then the tag is unconditionally discarded.
Otherwise the tag is only discarded
if its value matches.

*Method `TagSet.edit(self, editor=None, verbose=None, comments=())`*:
Edit this `TagSet`.

*Method `TagSet.edit_tagsets(*a, **kw)`*:
Edit a collection of `TagSet`s.
Return a list of `(old_name,new_name,TagSet)` for those which were modified.

This function supports modifying both `name` and `Tag`s.
The `Tag`s are updated directly.
The changed names are returning in the `old_name,new_name` above.

The collection `tes` may be either a mapping of name/key
to `TagSet` or an iterable of `TagSets`. If the latter, a
mapping is made based on `te.name or te.id` for each item
`te` in the iterable.

*Method `TagSet.from_csvrow(csvrow)`*:
Construct a `TagSet` from a CSV row like that from
`TagSet.csvrow`, being `unixtime,id,name,tags...`.

*Method `TagSet.from_ini(f, section: str, missing_ok=False)`*:
Load a `TagSet` from a section of a `.ini` file.

Parameters:
* `f`: the `.ini` format file to read;
  an iterable of lines (eg a file object)
  or the name of a file to open
* `section`: the name of the config section
  from which to load the `TagSet`
* `missing_ok`: optional flag, default `False`;
  if true a missing file will return an empty `TagSet`
  instead of raising `FileNotFoundError`

*Method `TagSet.from_line(line, offset=0, *, ontology=None, extra_types=None, verbose=None)`*:
Create a new `TagSet` from a line of text.

*Method `TagSet.from_tags(tags, _id=None, _ontology=None)`*:
Make a `TagSet` from an iterable of `Tag`s.

*Method `TagSet.get_arg_name(self, field_name)`*:
Override for `FormattableMixin.get_arg_name`:
return the leading dotted identifier,
which represents a tag or tag prefix.

*Method `TagSet.get_value(self, arg_name, a, kw)`*:
Override for `FormattableMixin.get_value`:
look up `arg_name` in `kw`, return a value.

The value is obtained as follows:
* `kw[arg_name]`: the `Tag` named `arg_name` if present
* `kw.get_format_attribute(arg_name)`:
  a formattable attribute named `arg_name`
otherwise raise `KeyError` if `self.format_mode.strict`
otherwise return the placeholder string `'{'+arg_name+'}'`.

*Property `TagSet.name`*:
Read only `name` property, `None` if there is no `'name'` tag.

*Method `TagSet.save_as_ini(self, f, section: str, config=None)`*:
Save this `TagSet` to the config file `f` as `section`.

If `f` is a string, read an existing config from that file
and update the section.

*Method `TagSet.set(self, name, value=None, *a, **kw)`*:
Set `self[tag_name]=value`.
If `verbose`, emit an info message if this changes the previous value.

*Method `TagSet.set_from(self, other, verbose=None)`*:
Completely replace the values in `self`
with the values from `other`,
a `TagSet` or any other `name`=>`value` dict.

This has the feature of logging changes
by calling `.set` and `.discard` to effect the changes.

*Method `TagSet.subtags(self, prefix, as_tagset=False)`*:
Return `TagSetPrefixView` of the tags commencing with `prefix+'.'`
with the key prefixes stripped off.

If `as_tagset` is true (default `False`)
return a new standalone `TagSet` containing the prefixed keys.

Example:

    >>> tags = TagSet({'a.b':1, 'a.d':2, 'c.e':3})
    >>> tags.subtags('a')
    TagSetPrefixView:a.{'b': 1, 'd': 2}
    >>> tags.subtags('a', as_tagset=True)
    TagSet:{'b': 1, 'd': 2}

*Method `TagSet.tag(self, tag_name, prefix=None, ontology=None)`*:
Return a `Tag` for `tag_name`, or `None` if missing.

Parameters:
* `tag_name`: the name of the `Tag` to create
* `prefix`: optional prefix;
  if supplied, prepend `prefix+'.'` to the `Tag` name
* `ontology`: optional ontology for the `Tag`,
  default `self.ontology`

*Method `TagSet.tag_metadata(self, tag_name, prefix=None, ontology=None, convert=None)`*:
Return a list of the metadata for the `Tag` named `tag_name`,
or an empty list if the `Tag` is missing.

*Property `TagSet.unixtime`*:
`unixtime` property, autosets to `time.time()` if accessed.

*Method `TagSet.update(self, other=None, *, prefix=None, verbose=None, **kw)`*:
Update this `TagSet` from `other`,
a dict of `{name:value}`
or an iterable of `Tag`like or `(name,value)` things.

## Class `TagSetCriterion`

A testable criterion for a `TagSet`.

*`TagSetCriterion.TAG_BASED_TEST_CLASS`*

*Method `TagSetCriterion.from_any(*a, **kw)`*:
Convert some suitable object `o` into a `TagSetCriterion`.

Various possibilities for `o` are:
* `TagSetCriterion`: returned unchanged
* `str`: a string tests for the presence
  of a tag with that name and optional value;
* an object with a `.choice` attribute;
  this is taken to be a `TagSetCriterion` ducktype and returned unchanged
* an object with `.name` and `.value` attributes;
  this is taken to be `Tag`-like and a positive test is constructed
* `Tag`: an object with a `.name` and `.value`
  is equivalent to a positive equality `TagBasedTest`
* `(name,value)`: a 2 element sequence
  is equivalent to a positive equality `TagBasedTest`

*Method `TagSetCriterion.from_arg(*a, **kw)`*:
Prepare a `TagSetCriterion` from the string `arg`
where `arg` is known to be entirely composed of the value,
such as a command line argument.

This calls the `from_str` method with `fallback_parse` set
to gather then entire tail of the supplied string `arg`.

*Method `TagSetCriterion.from_str(*a, **kw)`*:
Prepare a `TagSetCriterion` from the string `s`.

*Method `TagSetCriterion.from_str2(s, offset=0, delim=None, fallback_parse=None)`*:
Parse a criterion from `s` at `offset` and return `(TagSetCriterion,offset)`.

This method recognises an optional leading `'!'` or `'-'`
indicating negation of the test,
followed by a criterion recognised by the `.parse` method
of one of the classes in `cls.CRITERION_PARSE_CLASSES`.

*Method `TagSetCriterion.match_tagged_entity(self, te: 'TagSet') -> bool`*:
Apply this `TagSetCriterion` to a `TagSet`.

## Class `TagSetPrefixView(cs.lex.FormatableMixin, cs.lex.FormatableFormatter, string.Formatter)`

A view of a `TagSet` via a `prefix`.

Access to a key `k` accesses the `TagSet`
with the key `prefix+'.'+k`.

This is a kind of funny hybrid of a `Tag` and a `TagSet`
in that some things such as `__format__`
will format the `Tag` named `prefix` if it exists
in preference to the subtags.

Example:

    >>> tags = TagSet(a=1, b=2)
    >>> tags
    TagSet:{'a': 1, 'b': 2}
    >>> tags['sub.x'] = 3
    >>> tags['sub.y'] = 4
    >>> tags
    TagSet:{'a': 1, 'b': 2, 'sub.x': 3, 'sub.y': 4}
    >>> sub = tags.sub
    >>> sub
    TagSetPrefixView:sub.{'x': 3, 'y': 4}
    >>> sub.z = 5
    >>> sub
    TagSetPrefixView:sub.{'x': 3, 'y': 4, 'z': 5}
    >>> tags
    TagSet:{'a': 1, 'b': 2, 'sub.x': 3, 'sub.y': 4, 'sub.z': 5}

*Method `TagSetPrefixView.__getattr__(self, attr)`*:
Proxy other attributes through to the `TagSet`.

*Method `TagSetPrefixView.__setattr__(self, attr, value)`*:
Attribute based `Tag` access.

If `attr` is in `self.__dict__` then that is updated,
supporting "normal" attributes set on the instance.
Otherwise the `Tag` named `attr` is set to `value`.

The `__init__` methods of subclasses should do something like this
(from `TagSet.__init__`)
to set up the ordinary instance attributes
which are not to be treated as `Tag`s:

    self.__dict__.update(id=_id, ontology=_ontology, modified=False)

*Method `TagSetPrefixView.as_dict(self)`*:
Return a `dict` representation of this view.

*Method `TagSetPrefixView.get(self, k, default=None)`*:
Mapping `get` method.

*Method `TagSetPrefixView.get_format_attribute(self, attr)`*:
Fetch a formatting attribute from the proxied object.

*Method `TagSetPrefixView.items(self)`*:
Return an iterable of the items (`Tag` name, `Tag`).

*Method `TagSetPrefixView.keys(self)`*:
The keys of the subtags.

*Property `TagSetPrefixView.ontology`*:
The ontology of the references `TagSet`.

*Method `TagSetPrefixView.setdefault(self, k, v=None)`*:
Mapping `setdefault` method.

*Method `TagSetPrefixView.subtags(self, subprefix)`*:
Return a deeper view of the `TagSet`.

*Property `TagSetPrefixView.tag`*:
The `Tag` for the prefix, or `None` if there is no such `Tag`.

*Property `TagSetPrefixView.value`*:
Return the `Tag` value for the prefix, or `None` if there is no such `Tag`.

*Method `TagSetPrefixView.values(self)`*:
Return an iterable of the values (`Tag`s).

## Class `TagSetsSubdomain(cs.obj.SingletonMixin, cs.mappings.PrefixedMappingProxy, cs.mappings.RemappedMappingProxy)`

A view into a `BaseTagSets` for keys commencing with a prefix
being the subdomain plus a dot (`'.'`).

*Property `TagSetsSubdomain.TAGGED_ENTITY_FACTORY`*:
The entity factory comes from the parent collection.

## Class `TagsOntology(cs.obj.SingletonMixin, BaseTagSets, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, collections.abc.MutableMapping, collections.abc.Mapping, collections.abc.Collection, collections.abc.Sized, collections.abc.Iterable, collections.abc.Container)`

An ontology for tag names.
This is based around a mapping of names
to ontological information expressed as a `TagSet`.

Normally an object's tags are not a self contained repository of all the information;
instead a tag just names some information.

As a example, consider the tag `colour=blue`.
Meta information about `blue` is obtained via the ontology,
which has an entry for the colour `blue`.
We adopt the convention that the type is just the tag name,
so we obtain the metadata by calling `ontology.metadata(tag)`
or alternatively `ontology.metadata(tag.name,tag.value)`
being the type name and value respectively.

The ontology itself is based around `TagSets` and effectively the call
`ontology.metadata('colour','blue')`
would look up the `TagSet` named `colour.blue` in the underlying `Tagsets`.

For a self contained dataset this means that it can be its own ontology.
For tags associated with arbitrary objects
such as the filesystem tags maintained by `cs.fstags`
the ontology would be a separate tags collection stored in a central place.

There are two main categories of entries in an ontology:
* metadata: other entries named *typename*`.`*value_key*
  contains a `TagSet` holding metadata for a value of type *typename*
  whose value is mapped to *value_key*
* types: an optional entry named `type.`*typename* contains a `TagSet`
  describing the type named *typename*;
  really this is just more metadata where the "type name" is `type`

Metadata are `TagSets` instances describing particular values of a type.
For example, some metadata for the `Tag` `colour="blue"`:

    colour.blue url="https://en.wikipedia.org/wiki/Blue" wavelengths="450nm-495nm"

Some metadata associated with the `Tag` `actor="Scarlett Johansson"`:

    actor.scarlett_johansson role=["Black Widow (Marvel)"]
    character.marvel.black_widow fullname=["Natasha Romanov"]

The tag values are lists above because an actor might play many roles, etc.

There's a convention for converting human descriptions
such as the role string `"Black Widow (Marvel)"` to its metadata.
* the value `"Black Widow (Marvel)"` if converted to a key
  by the ontology method `value_to_tag_name`;
  it moves a bracket suffix such as `(Marvel)` to the front as a prefix
  `marvel.` and downcases the rest of the string and turns spaces into underscores.
  This yields the value key `marvel.black_widow`.
* the type is `role`, so the ontology entry for the metadata
  is `role.marvel.black_widow`

this requires type information about a `role`.
Here are some type definitions supporting the above metadata:

    type.person type=str description="A person."
    type.actor type=person description="An actor's stage name."
    type.character type=str description="A person in a story."
    type.role type_name=character description="A character role in a performance."
    type.cast type=dict key_type=actor member_type=role description="Cast members and their roles."

The basic types have their Python names: `int`, `float`, `str`, `list`,
`dict`, `date`, `datetime`.
You can define subtypes of these for your own purposes
as illustrated above.

For example:

    type.colour type=str description="A hue."

which subclasses `str`.

Subtypes of `list` include a `member_type`
specifying the type for members of a `Tag` value:

    type.scene type=list member_type=str description="A movie scene."

Subtypes of `dict` include a `key_type` and a `member_type`
specifying the type for keys and members of a `Tag` value:

Accessing type data and metadata:

A `TagSet` may have a reference to a `TagsOntology` as `.ontology`
and so also do any of its `Tag`s.

*Method `TagsOntology.__bool__(self)`*:
Support easy `ontology or some_default` tests,
since ontologies are broadly optional.

*Method `TagsOntology.__delitem__(self, name)`*:
Delete the entity named `name`.

*Method `TagsOntology.__getitem__(self, name)`*:
Fetch `tags` for the entity named `name`.

*Method `TagsOntology.__setitem__(self, name, tags)`*:
Apply `tags` to the entity named `name`.

*Method `TagsOntology.add_tagsets(self, *a, **kw)`*:
Insert a `_TagsOntology_SubTagSets` at `index`
in the list of `_TagsOntology_SubTagSets`es.

The new `_TagsOntology_SubTagSets` instance is initialised
from the supplied `tagsets`, `match`, `unmatch` parameters.

*Method `TagsOntology.as_dict(self)`*:
Return a `dict` containing a mapping of entry names to their `TagSet`s.

*Method `TagsOntology.basetype(self, typename)`*:
Infer the base type name from a type name.
The default type is `'str'`,
but any type which resolves to one in `self.BASE_TYPES`
may be returned.

*Method `TagsOntology.by_type(self, type_name, with_tagsets=False)`*:
Yield keys or (key,tagset) of type `type_name`
i.e. all keys commencing with *type_name*`.`.

*Method `TagsOntology.convert_tag(self, tag)`*:
Convert a `Tag`'s value accord to the ontology.
Return a new `Tag` with the converted value
or the original `Tag` unchanged.

This is primarily aimed at things like regexp based autotagging,
where the matches are all strings
but various fields have special types,
commonly `int`s or `date`s.

*Method `TagsOntology.edit_indices(self, *a, **kw)`*:
Edit the entries specified by indices.
Return `TagSet`s for the entries which were changed.

*Method `TagsOntology.from_match(*a, **kw)`*:
Initialise a `SubTagSets` from `tagsets`, `match` and optional `unmatch`.

Parameters:
* `tagsets`: a `TagSets` holding ontology information
* `match`: a match function used to choose entries based on a type name
* `unmatch`: an optional reverse for `match`, accepting a subtype
  name and returning its public name

If `match` is `None`
then `tagsets` will always be chosen if no prior entry matched.

Otherwise, `match` is resolved to a function `match-func(type_name)`
which returns a subtype name on a match and a false value on no match.

If `match` is a callable it is used as `match_func` directly.

if `match` is a list, tuple or set
then this method calls itself with `(tagsets,submatch)`
for each member `submatch` if `match`.

If `match` is a `str`,
if it ends in a dot '.', dash '-' or underscore '_'
then it is considered a prefix of `type_name` and the returned
subtype name is the text from `type_name` after the prefix
othwerwise it is considered a full match for the `type_name`
and the returns subtype name is `type_name` unchanged.
The `match` string is a simplistic shell style glob
supporting `*` but not `?` or `[`*seq*`]`.

The value of `unmatch` is constrained by `match`.
If `match` is `None`, `unmatch` must also be `None`;
the type name is used unchanged.
If `match` is callable`, `unmatch` must also be callable;
it is expected to reverse `match`.

Examples:

    >>> from cs.sqltags import SQLTags
    >>> from os.path import expanduser as u
    >>> # an initial empty ontology with a default in memory mapping
    >>> ont = TagsOntology()
    >>> # divert the types actor, role and series to my media ontology
    >>> ont.add_tagsets(
    ...     SQLTags(u('~/var/media-ontology.sqlite')),
    ...     ['actor', 'role', 'series'])
    >>> # divert type "musicbrainz.recording" to mbdb.sqlite
    >>> # mapping to the type "recording"
    >>> ont.add_tagsets(SQLTags(u('~/.cache/mbdb.sqlite')), 'musicbrainz.')
    >>> # divert type "tvdb.actor" to tvdb.sqlite
    >>> # mapping to the type "actor"
    >>> ont.add_tagsets(SQLTags(u('~/.cache/tvdb.sqlite')), 'tvdb.')

*Method `TagsOntology.get(self, name, default=None)`*:
Fetch the entity named `name` or `default`.

*Method `TagsOntology.items(self)`*:
Yield `(entity_name,tags)` for all the items in each subtagsets.

*Method `TagsOntology.keys(self)`*:
Yield entity names for all the entities.

*Method `TagsOntology.metadata(self, name, value=None, *a, **kw)`*:
Return the metadata `TagSet` for `type_name` and `value`.
This implements the mapping between a type's value and its semantics.

The optional parameter `convert`
may specify a function to use to convert `value` to a tag name component
to be used in place of `self.value_to_tag_name` (the default).

For example, if a `TagSet` had a list of characters such as:

    character=["Captain America (Marvel)","Black Widow (Marvel)"]

then these values could be converted to the dotted identifiers
`character.marvel.captain_america`
and `character.marvel.black_widow` respectively,
ready for lookup in the ontology
to obtain the "metadata" `TagSet` for each specific value.

*Method `TagsOntology.startup_shutdown(self)`*:
Open all the sub`TagSets` and close on exit.

*Method `TagsOntology.subtype_name(self, type_name)`*:
Return the type name for use within `self.tagsets` from `type_name`.
Returns `None` if this is not a supported `type_name`.

*Method `TagsOntology.type_name(self, subtype_name)`*:
Return the external type name from the internal `subtype_name`
which is used within `self.tagsets`.

*Method `TagsOntology.type_names(self)`*:
Return defined type names i.e. all entries starting `type.`.

*Method `TagsOntology.type_values(self, type_name, value_tag_name=None)`*:
Yield the various defined values for `type_name`.
This is useful for types with enumerated metadata entries.

For example, if metadata entries exist as `foo.bah` and `foo.baz`
for the `type_name` `'foo'`
then this yields `'bah'` and `'baz'`.`

Note that this looks for a `Tag` for the value,
falling back to the entry suffix if the tag is not present.
That tag is normally named `value`
(from DEFAULT_VALUE_TAG_NAME)
but may be overridden by the `value_tag_name` parameter.
Also note that normally it is desireable that the value
convert to the suffix via the `value_to_tag_name` method
so that the metadata entry can be located from the value.

*Method `TagsOntology.typedef(self, type_name)`*:
Return the `TagSet` defining the type named `type_name`.

*Method `TagsOntology.types(self)`*:
Generator yielding defined type names and their defining `TagSet`.

*Method `TagsOntology.value_to_tag_name(*a, **kw)`*:
Convert a tag value to a tagnamelike dotted identifierish string
for use in ontology lookup.
Raises `ValueError` for unconvertable values.

We are allowing dashes in the result (UUIDs, MusicBrainz discids, etc).

`int`s are converted to `str`.

Strings are converted as follows:
* a trailing `(.*)` is turned into a prefix with a dot,
  for example `"Captain America (Marvel)"`
  becomes `"Marvel.Captain America"`.
* the string is split into words (nonwhitespace),
  lowercased and joined with underscores,
  for example `"Marvel.Captain America"`
  becomes `"marvel.captain_america"`.

## Class `TagsOntologyCommand(cs.cmdutils.BaseCommand)`

A command line for working with ontology types.

Command line usage:

    Usage: tagsontology subcommand [...]
      Subcommands:
        edit [{/name-regexp | entity-name}]
          Edit entities.
          With no arguments, edit all the entities.
          With an argument starting with a slash, edit the entities
          whose names match the regexp.
          Otherwise the argument is expected to be an entity name;
          edit the tags of that entity.
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        meta tag=value
        type
            With no arguments, list the defined types.
          type type_name
            With a type name, print its `Tag`s.
          type type_name edit
            Edit the tags defining a type.
          type type_name edit meta_names_pattern...
            Edit the tags for the metadata names matching the
            meta_names_patterns.
          type type_name list
          type type_name ls
            List the metadata names for this type and their tags.
          type type_name + entity_name [tags...]
            Create type_name.entity_name and apply the tags.

*Method `TagsOntologyCommand.cmd_edit(self, argv)`*:
Usage: {cmd} [{{/name-regexp | entity-name}}]
Edit entities.
With no arguments, edit all the entities.
With an argument starting with a slash, edit the entities
whose names match the regexp.
Otherwise the argument is expected to be an entity name;
edit the tags of that entity.

*Method `TagsOntologyCommand.cmd_meta(self, argv)`*:
Usage: {cmd} tag=value

*Method `TagsOntologyCommand.cmd_type(self, argv)`*:
Usage:
{cmd}
  With no arguments, list the defined types.
{cmd} type_name
  With a type name, print its `Tag`s.
{cmd} type_name edit
  Edit the tags defining a type.
{cmd} type_name edit meta_names_pattern...
  Edit the tags for the metadata names matching the
  meta_names_patterns.
{cmd} type_name list
{cmd} type_name ls
  List the metadata names for this type and their tags.
{cmd} type_name + entity_name [tags...]
  Create type_name.entity_name and apply the tags.

# Release Log



*Release 20220606*:
* Tag.parse_value: bugfix parse of float.
* TagSet.edit: accept optional comments parameter with addition header comment lines, be more tolerant of errors, avoid losing data on error.

*Release 20220430*:
* TagSetPrefixView: new as_dict() method.
* TagSetPrefixView.__str__: behave like TagSet.__str__.
* TagFile.save_tagsets: do not try to save if the file is missing and the tagsets are empty.
* New TagSet.from_tags(tags) factory to make a new TagSet from an iterable of tags.
* TagSetPrefixView: add .get and .setdefault mapping methods.
* RegexpTagRule: accept optional tag_prefix parameter.
* Tagset: new from_ini() and save_as_ini() methods to support cs.timeseries config files, probably handy elsewhere.

*Release 20220311*:
Assorted internal changes.

*Release 20211212*:
* Tag: new fallback_parse parameter for value parsing, default get_nonwhite.
* Tag: new from_arg factory with fallback_parse grabbing the whole string for command line arguments, thus supporting unquoted strings for ease of use.
* TagSetCriterion: new optional fallback_parse parameter and from_arg method as for the Tag factories.
* Tag.transcribe_value: accept optional json_options to control the JSON encoder, used for human friendly multiline edits in cs.app.tagger.
* Rename edit_many to edit_tagsets for clarity.
* TagsOntology: new type_values method to return values for a type (derived from their metadata entries).
* Tag: new alt_values method returning its TagsOntology.type_values.
* (Internal) New _FormatStringTagProxy which proxies a Tag but uses str(self.__proxied.value) for __str__ to support format strings.
* (Internal) TagSet.get_value: if arg_name matches a Tag, return a _FormatStringTagProxy.
* Tag.__new__: accept (tag_name,value) or (Tag) as initialisation parameters.

*Release 20210913*:
* TagSet.get_value: raise KeyError in strict mode, leave placeholder otherwise.
* Other small changes.

*Release 20210906*:
Many many updates; some semantics have changed.

*Release 20210428*:
Bugfix TagSet.set: internal in place changes to a complex tag value were not noticed, causing TagFile to not update on shutdown.

*Release 20210420*:
* TagSet: also subclass cs.dateutils.UNIXTimeMixin.
* Various TagSetNamespace updates and bugfixes.

*Release 20210404*:
Bugfix TagBasedTest.COMPARISON_FUNCS["="]: if cmp_value is None, return true (the tag is present).

*Release 20210306*:
* ExtendedNamespace,TagSetNamespace: move the .[:alpha:]* attribute support from ExtendedNamespace to TagSetNamespace because it requires Tags.
* TagSetNamespace.__getattr__: new _i, _s, _f suffixes to return int, str or float tag values (or None); fold _lc in with these.
* Pull most of `TaggedEntity` out into `TaggedEntityMixin` for reuse by domain specific tagged entities.
* TaggedEntity: new .set and .discard methods.
* TaggedEntity: new as_editable_line, from_editable_line, edit and edit_entities methods to support editing entities using a text editor.
* ontologies: type entries are now prefixed with "type." and metadata entries are prefixed with "meta."; provide a worked ontology example in the introduction and improve related docstrings.
* TagsOntology: new .types(), .types_names(), .meta(type_name,value), .meta_names() methods.
* TagsOntology.__getitem__: create missing TagSets on demand.
* New TagsOntologyCommand, initially with a "type [type_name [{edit|list}]]" subcommand, ready for use as the cmd_ont subcommand of other tag related commands.
* TagSet: support initialisation like a dict including keywords, and move the `ontology` parameter to `_onotology`.
* TagSet: include AttrableMappingMixin to enable attribute access to values when there is no conflict with normal methods.
* UUID encode/decode support.
* Honour $TAGSET_EDITOR or $EDITOR as preferred interactive editor for tags.
* New TagSet.subtags(prefix) to extract a subset of the tags.
* TagsOntology.value_metadata: new optional convert parameter to override the default "convert human friendly name" algorithm, particularly to pass convert=str to things which are already the basic id.
* Rename TaggedEntity to TagSet.
* Rename TaggedEntities to TagSets.
* TagSet: new csvrow and from_csvrow methods imported from obsolete TaggedEntityMixin class.
* Move BaseTagFile from cs.fstags to TagFile in cs.tagset.
* TagSet: support access to the tag "c.x" via attributes provided there is no "c" tag in the way.
* TagSet.unixtime: implement the autoset-to-now semantics.
* New as_timestamp(): convert date, datetime, int or float to a UNIX timestamp.
* Assorted docstring updates and bugfixes.

*Release 20200716*:
* Update for changed cs.obj.SingletonMixin API.
* Pull in TaggedEntity from cs.sqltags and add the .csvrow property and the .from_csvrow factory.

*Release 20200521.1*:
Fix DISTINFO.install_requires, drop debug import.

*Release 20200521*:
* New ValueDetail and KeyValueDetail classes for returning ontology information; TagInfo.detail now returns a ValueDetail for scalar types, a list of ValueDetails for sequence types and a list of KeyValueDetails for mapping types; drop various TagInfo mapping/iterable style methods, too confusing to use.
* Plumb ontology parameter throughout, always optional.
* Drop TypedTag, Tags now use ontologies for this.
* New TagsCommandMixin to support BaseCommands which manipulate Tags.
* Many improvements and bugfixes.

*Release 20200318*:
* *Note that the TagsOntology stuff is in flux and totally alpha.*
* Tag.prefix_name factory returning a new tag if prefix is not empty, ptherwise self.
* TagSet.update: accept an optional prefix for inserting "foreign" tags with a distinguishing name prefix.
* Tag.as_json: turn sets and tuples into lists for encoding.
* Backport for Python < 3.7 (no fromisoformat functions).
* TagSet: drop unused and illplaced .titleify, .episode_title and .title methods.
* TagSet: remove "defaults", unused.
* Make TagSet a direct subclass of dict, adjust uses of .update etc.
* New ExtendedNamespace class which is a SimpleNamespace with some inferred attributes and a partial mapping API (keys and __getitem__).
* New TagSet.ns() returning the Tags as an ExtendedNamespace, which doubles as a mapping for str.format_map; TagSet.format_kwargs is now an alias for this.
* New Tag.from_string factory to parse a str into a Tag.
* New TagsOntology and TypedTag classes to provide type and value-detail information; very very alpha and subject to change.

*Release 20200229.1*:
Initial release: pull TagSet, Tag, TagChoice from cs.fstags for independent use.
