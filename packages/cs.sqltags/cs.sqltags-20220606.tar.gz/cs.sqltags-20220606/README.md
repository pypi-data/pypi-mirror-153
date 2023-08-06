Simple SQL based tagging
and the associated `sqltags` command line script,
supporting both tagged named objects and tagged timestamped log entries.

*Latest release 20220606*:
* New SQLTagsORM.Entities.add_new_tags method, use it in SQLTags.default_factory for bulk insert.
* SQTCriterion: new .from_equality(tag_name,tag_value) factory to make an equality criterion.
* SQLTags.find: accept criteria as positional parameters instead of a single iterable, accept new keyword parameters as equality criteria.
* SQLTags.__getitem__: accept a slice to index the .unixtime tag.
* SQLTagsORM: also turn on echo mode if "ECHO" in $SQLTAGS_MODES.

Compared to `cs.fstags` and its associated `fstags` command,
this is oriented towards large numbers of items
not naturally associated with filesystem objects.

My initial use case is an activity log
(unnamed timestamped tag sets)
but I'm also using it for ontologies
(named tag sets containing metadata).

Many basic tasks can be performed with the `sqltags` command line utility,
documented under the `SQLTagsCommand` class below.

See the `SQLTagsORM` documentation for details about how data
are stored in the database.
See the `SQLTagSet` documentation for details of how various
tag value types are supported.

## Class `BaseSQLTagsCommand(cs.cmdutils.BaseCommand, cs.tagset.TagsCommandMixin)`

Common features for commands oriented around an `SQLTags` database.

Command line usage:

    Usage: basesqltags [-f db_url] subcommand [...]
      -f db_url SQLAlchemy database URL or filename.
                Default from $SQLTAGS_DBURL (default '~/var/sqltags.sqlite').
      Subcommands:
        dbshell
          Start an interactive database shell.
        edit criteria...
          Edit the entities specified by criteria.
        export [-F format] [{tag[=value]|-tag}...]
          Export entities matching all the constraints.
          -F format Specify the export format, either CSV or FSTAGS.
        find [-o output_format] {tag[=value]|-tag}...
          List entities matching all the constraints.
          -o output_format
                      Use output_format as a Python format string to lay out
                      the listing.
                      Default: {datetime} {headline}
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        import [{-u|--update}] {-|srcpath}...
          Import CSV data in the format emitted by "export".
          Each argument is a file path or "-", indicating standard input.
          -u, --update  If a named entity already exists then update its tags.
                        Otherwise this will be seen as a conflict
                        and the import aborted.
        init
          Initialise the database.
          This includes defining the schema and making the root metanode.
        log [-c category,...] [-d when] [-D strptime] {-|headline} [tags...]
          Record entries into the database.
          If headline is '-', read headlines from standard input.
          -c categories
            Specify the categories for this log entry.
            The default is to recognise a leading CAT,CAT,...: prefix.
          -d when
            Use when, an ISO8601 date, as the log entry timestamp.
          -D strptime
            Read the time from the start of the headline
            according to the provided strptime specification.
        tag {-|entity-name} {tag[=value]|-tag}...
          Tag an entity with multiple tags.
          With the form "-tag", remove that tag from the direct tags.
          A entity-name named "-" indicates that entity-names should
          be read from the standard input.

*`BaseSQLTagsCommand.TAGSETS_CLASS`*

*`BaseSQLTagsCommand.TAGSET_CRITERION_CLASS`*

*`BaseSQLTagsCommand.TAG_BASED_TEST_CLASS`*

*Method `BaseSQLTagsCommand.apply_defaults(self)`*:
Set up the default values in `options`.

*Method `BaseSQLTagsCommand.apply_opt(self, opt, val)`*:
Apply a command line option.

*Method `BaseSQLTagsCommand.cmd_dbshell(self, argv)`*:
Usage: {cmd}
Start an interactive database shell.

*Method `BaseSQLTagsCommand.cmd_edit(self, argv)`*:
Usage: edit criteria...
Edit the entities specified by criteria.

*Method `BaseSQLTagsCommand.cmd_export(self, argv)`*:
Usage: {cmd} [-F format] [{{tag[=value]|-tag}}...]
Export entities matching all the constraints.
-F format Specify the export format, either CSV or FSTAGS.

The CSV export format is CSV data with the following columns:
* unixtime: the entity unixtime, a float
* id: the entity database row id, an integer
* name: the entity name
* tags: a column per Tag

*Method `BaseSQLTagsCommand.cmd_find(self, argv)`*:
Usage: {cmd} [-o output_format] {{tag[=value]|-tag}}...
List entities matching all the constraints.
-o output_format
            Use output_format as a Python format string to lay out
            the listing.
            Default: {FIND_OUTPUT_FORMAT_DEFAULT}

*Method `BaseSQLTagsCommand.cmd_import(self, argv)`*:
Usage: {cmd} [{{-u|--update}}] {{-|srcpath}}...
  Import CSV data in the format emitted by "export".
  Each argument is a file path or "-", indicating standard input.
  -u, --update  If a named entity already exists then update its tags.
                Otherwise this will be seen as a conflict
                and the import aborted.

TODO: should this be a transaction so that an import is all or nothing?

*Method `BaseSQLTagsCommand.cmd_init(self, argv)`*:
Usage: {cmd}
Initialise the database.
This includes defining the schema and making the root metanode.

*Method `BaseSQLTagsCommand.cmd_log(self, argv)`*:
Record a log entry.

Usage: {cmd} [-c category,...] [-d when] [-D strptime] {{-|headline}} [tags...]
  Record entries into the database.
  If headline is '-', read headlines from standard input.
  -c categories
    Specify the categories for this log entry.
    The default is to recognise a leading CAT,CAT,...: prefix.
  -d when
    Use when, an ISO8601 date, as the log entry timestamp.
  -D strptime
    Read the time from the start of the headline
    according to the provided strptime specification.

*Method `BaseSQLTagsCommand.cmd_tag(self, argv)`*:
Usage: {cmd} {{-|entity-name}} {{tag[=value]|-tag}}...
Tag an entity with multiple tags.
With the form "-tag", remove that tag from the direct tags.
A entity-name named "-" indicates that entity-names should
be read from the standard input.

*Method `BaseSQLTagsCommand.parse_categories(categories)`*:
Extract "category" words from the `str` `categories`,
return a list of category names.

Splits on commas, strips leading and trailing whitespace, downcases.

*Method `BaseSQLTagsCommand.parse_tagset_criterion(arg, tag_based_test_class=None)`*:
Parse tag criteria from `argv`.

The criteria may be either:
* an integer specifying a `Tag` id
* a sequence of tag criteria

*Method `BaseSQLTagsCommand.run_context(self)`*:
Prepare the `SQLTags` around each command invocation.

## Function `glob2like(glob: str) -> str`

Convert a filename glob to an SQL LIKE pattern.

## Function `main(argv=None)`

Command line mode.

## Class `PolyValue(PolyValue, builtins.tuple)`

A `namedtuple` for the polyvalues used in an `SQLTagsORM`.

We express various types in SQL as one of 3 columns:
* `float_value`: for `float`s and `int`s which round trip with `float`
* `string_value`: for `str`
* `structured_value`: a JSON transcription of any other type

This allows SQL indexing of basic types.

Note that because `str` gets stored in `string_value`
this leaves us free to use "bare string" JSON to serialise
various nonJSONable types.

The `SQLTagSets` class has a `to_polyvalue` factory
which produces a `PolyValue` suitable for the SQL rows.
NonJSONable types such as `datetime`
are converted to a `str` but stored in the `structured_value` column.
This should be overridden by subclasses as necessary.

On retrieval from the database
the tag rows are converted to Python values
by the `SQLTagSets.from_polyvalue` method,
reversing the process above.

*Method `PolyValue.is_valid(self)`*:
Test that at most one attribute is non-`None`.

## Class `PolyValueColumnMixin`

A mixin for classes with `(float_value,string_value,structured_value)` columns.
This is used by the `Tags` and `TagMultiValues` relations inside `SQLTagsORM`.

*Method `PolyValueColumnMixin.as_polyvalue(self)`*:
Return this row's value as a `PolyValue`.

*Method `PolyValueColumnMixin.set_polyvalue(self, pv: cs.sqltags.PolyValue)`*:
Set all the value fields.

*Method `PolyValueColumnMixin.value_test(other_value)`*:
Return `(column,test_value)` for constructing tests against
`other_value` where `column` if the appropriate SQLAlchemy column
and `test_value` is the comparison value for testing.

For most `other_value`s the `test_value`
will just be `other_value`,
but for certain types the `test_value` will be:
* `NoneType`: `None`, and the column will also be `None`
* `datetime`: `datetime2unixtime(other_value)`

## Function `prefix2like(prefix: str, esc='\\') -> str`

Convert a prefix string to an SQL LIKE pattern.

## Class `SQLParameters(SQLParameters, builtins.tuple)`

The parameters required for constructing queries
or extending queries with JOINs.

Attributes:
* `criterion`: the source criterion, usually an `SQTCriterion` subinstance
* `alias`: an alias of the source table for use in queries
* `entity_id_column`: the `entities` id column,
  `alias.id` if the alias is of `entities`,
  `alias.entity_id` if the alias is of `tags`
* `constraint`: a filter query based on `alias`

## Class `SQLTagBasedTest(cs.tagset.TagBasedTest, cs.tagset.TagBasedTest, builtins.tuple, SQTCriterion, cs.tagset.TagSetCriterion)`

A `cs.tagset.TagBasedTest` extended with a `.sql_parameters` method.

*Method `SQLTagBasedTest.match_tagged_entity(self, te: cs.tagset.TagSet) -> bool`*:
Match this criterion against `te`.

## Class `SQLTagProxies`

A proxy for the tags supporting Python comparison => `SQLParameters`.

Example:

    sqltags.tags.dotted.name.here == 'foo'

## Class `SQLTagProxy`

An object based on a `Tag` name
which produces an `SQLParameters` when compared with some value.

Example:

    >>> sqltags = SQLTags('sqlite://')
    >>> sqltags.init()
    >>> # make a SQLParameters for testing the tag 'name.thing'==5
    >>> sqlp = sqltags.tags.name.thing == 5
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.float_value = :float_value_1'
    >>> sqlp = sqltags.tags.name.thing == 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value = :string_value_1'

*Method `SQLTagProxy.__eq__(self, other, alias=None) -> cs.sqltags.SQLParameters`*:
Return an SQL `=` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing == 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value = :string_value_1'

*Method `SQLTagProxy.__ge__(self, other)`*:
Return an SQL `>=` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing >= 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value >= :string_value_1'

*Method `SQLTagProxy.__getattr__(self, sub_tag_name)`*:
Magic access to dotted tag names: produce a new `SQLTagProxy` from ourself.

*Method `SQLTagProxy.__gt__(self, other)`*:
Return an SQL `>` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing > 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value > :string_value_1'

*Method `SQLTagProxy.__le__(self, other)`*:
Return an SQL `<=` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing <= 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value <= :string_value_1'

*Method `SQLTagProxy.__lt__(self, other)`*:
Return an SQL `<` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing < 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value < :string_value_1'

*Method `SQLTagProxy.__ne__(self, other, alias=None) -> cs.sqltags.SQLParameters`*:
Return an SQL `<>` test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing != 'foo'
    >>> str(sqlp.constraint)
    'tags_1.name = :name_1 AND tags_1.string_value != :string_value_1'

*Method `SQLTagProxy.by_op_text(self, op_text, other, alias=None)`*:
Return an `SQLParameters` based on the comparison's text representation.

Parameters:
* `op_text`: the comparsion operation text, one of:
  `'='`, `'<='`, `'<'`, `'>='`, `'>'`, `'~'`.
* `other`: the other value for the comparison,
  used to infer the SQL column name
  and kept to provide the SQL value parameter
* `alias`: optional SQLAlchemy table alias

*Method `SQLTagProxy.likeglob(self, globptn: str) -> cs.sqltags.SQLParameters`*:
Return an SQL LIKE test approximating a glob as an `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing.likeglob('foo*')
    >>> str(sqlp.constraint)
    "tags_1.name = :name_1 AND tags_1.string_value LIKE :string_value_1 ESCAPE '\\'"

*Method `SQLTagProxy.startswith(self, prefix: str) -> cs.sqltags.SQLParameters`*:
Return an SQL LIKE prefix test `SQLParameters`.

Example:

    >>> sqlp = SQLTags('sqlite://').tags.name.thing.startswith('foo')
    >>> str(sqlp.constraint)
    "tags_1.name = :name_1 AND tags_1.string_value LIKE :string_value_1 ESCAPE '\\'"

## Class `SQLTags(cs.tagset.BaseTagSets, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, collections.abc.MutableMapping, collections.abc.Mapping, collections.abc.Collection, collections.abc.Sized, collections.abc.Iterable, collections.abc.Container)`

A class using an SQL database to store its `TagSet`s.

*Method `SQLTags.TAGSETCLASS_DEFAULT(self, *a, _sqltags=None, **kw)`*:
Factory to return a suitable `TagSet` subclass instance.
This produces an `SQLTagSet` instance correctly associated with this `SQLTags`.

*Method `SQLTags.TagSetClass(self, *a, **kw)`*:
Local implementation of `TagSetClass`
so that we can annotate it with a `.singleton_also_by` attribute.

*Method `SQLTags.__getitem__(self, *a, **kw)`*:
Return an `SQLTagSet` for `index` (an `int` or `str`).

*Method `SQLTags.__setitem__(self, *a, **kw)`*:
Dummy `__setitem__` which checks `te` against the db by type
because the factory inserts it into the database.

*Method `SQLTags.db_entity(self, index)`*:
Return the `Entities` instance for `index` or `None`.

*Method `SQLTags.db_session(self, *, new=False)`*:
Context manager to obtain a db session if required
(or if `new` is true).

*Property `SQLTags.default_db_session`*:
The current per-`Thread` SQLAlchemy Session.

*Method `SQLTags.default_factory(self, name: Optional[str] = None, *, unixtime=None, tags=None)`*:
Fetch or create an `SQLTagSet` for `name`.

Note that `name` may be `None` to create a new "log" entry.

*Method `SQLTags.find(self, *criteria, **crit_kw)`*:
Generate and run a query derived from `criteria`
yielding `SQLTagSet` instances.

Parameters:
* `criteria`: positional arguments which should be
  `SQTCriterion`s or a `str` suitable for `SQTCriterion.from_str`
* `crit_kw`: keyword parameters are appended to the criteria
  as further tag equality tests

*Method `SQLTags.flush(self)`*:
Flush the current session state to the database.

*Method `SQLTags.get(self, index, default=None)`*:
Return an `SQLTagSet` matching `index`, or `None` if there is no such entity.

*Method `SQLTags.import_csv_file(self, f, *, update_mode=False)`*:
Import CSV data from the file `f`.

If `update_mode` is true
named records which already exist will update from the data,
otherwise the conflict will raise a `ValueError`.

*Method `SQLTags.import_tagged_entity(self, te, *, update_mode=False) -> None`*:
Import the `TagSet` `te`.

This updates the database with the contents of the supplied `TagSet`,
which has no inherent relationship to the database.

If `update_mode` is true
named records which already exist will update from `te`,
otherwise the conflict will raise a `ValueError`.

*Method `SQLTags.infer_db_url(envvar=None, default_path=None)`*:
Infer the database URL.

Parameters:
* `envvar`: environment variable to specify a default,
  default from `DBURL_ENVVAR` (`SQLTAGS_DBURL`).

*Method `SQLTags.init(self)`*:
Initialise the database.

*Method `SQLTags.items(self, *, prefix=None)`*:
Return an iterable of `(tagset_name,TagSet)`.
Excludes unnamed `TagSet`s.

Constrain the names to those starting with `prefix`
if not `None`.

*Method `SQLTags.keys(self, *, prefix=None)`*:
Yield all the nonNULL names.

Constrain the names to those starting with `prefix`
if not `None`.

*Property `SQLTags.metanode`*:
The metadata node.

*Method `SQLTags.startup_shutdown(self)`*:
Stub startup/shutdown since we use autosessions.
Particularly, we do not want to keep SQLite dbs open.

*Method `SQLTags.values(self, *, prefix=None)`*:
Return an iterable of the named `TagSet`s.
Excludes unnamed `TagSet`s.

Constrain the names to those starting with `prefix`
if not `None`.

## Class `SQLTagsCommand(BaseSQLTagsCommand, cs.cmdutils.BaseCommand, cs.tagset.TagsCommandMixin)`

`sqltags` main command line utility.

Command line usage:

    Usage: sqltags [-f db_url] subcommand [...]
      -f db_url SQLAlchemy database URL or filename.
                Default from $SQLTAGS_DBURL (default '~/var/sqltags.sqlite').
      Subcommands:
        dbshell
          Start an interactive database shell.
        edit criteria...
          Edit the entities specified by criteria.
        export [-F format] [{tag[=value]|-tag}...]
          Export entities matching all the constraints.
          -F format Specify the export format, either CSV or FSTAGS.
        find [-o output_format] {tag[=value]|-tag}...
          List entities matching all the constraints.
          -o output_format
                      Use output_format as a Python format string to lay out
                      the listing.
                      Default: {datetime} {headline}
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        import [{-u|--update}] {-|srcpath}...
          Import CSV data in the format emitted by "export".
          Each argument is a file path or "-", indicating standard input.
          -u, --update  If a named entity already exists then update its tags.
                        Otherwise this will be seen as a conflict
                        and the import aborted.
        init
          Initialise the database.
          This includes defining the schema and making the root metanode.
        list [entity-names...]
          List entities and their tags.
        log [-c category,...] [-d when] [-D strptime] {-|headline} [tags...]
          Record entries into the database.
          If headline is '-', read headlines from standard input.
          -c categories
            Specify the categories for this log entry.
            The default is to recognise a leading CAT,CAT,...: prefix.
          -d when
            Use when, an ISO8601 date, as the log entry timestamp.
          -D strptime
            Read the time from the start of the headline
            according to the provided strptime specification.
        ls [entity-names...]
          List entities and their tags.
        tag {-|entity-name} {tag[=value]|-tag}...
          Tag an entity with multiple tags.
          With the form "-tag", remove that tag from the direct tags.
          A entity-name named "-" indicates that entity-names should
          be read from the standard input.

*Method `SQLTagsCommand.cmd_list(self, argv)`*:
Usage: {cmd} [entity-names...]
List entities and their tags.

*Method `SQLTagsCommand.cmd_ls(self, argv)`*:
Usage: {cmd} [entity-names...]
List entities and their tags.

## Class `SQLTagSet(cs.obj.SingletonMixin, cs.tagset.TagSet, builtins.dict, cs.dateutils.UNIXTimeMixin, cs.lex.FormatableMixin, cs.lex.FormatableFormatter, string.Formatter, cs.mappings.AttrableMappingMixin)`

A singleton `TagSet` attached to an `SQLTags` instance.

As with the `TagSet` superclass,
tag values can be any Python type.
However, because we are storing these values in an SQL database
it is necessary to provide a conversion facility
to prepare those values for storage.

The database schema is described in the `SQLTagsORM` class;
in short we directly support `None`, `float` and `str`,
`int`s which round trip with `float`,
and `list`, `tuple` and `dict` whose contents transcribe to JSON.

`int`s which are too large to round trip with `float`
are treated as an extended `"bigint"` type
using the scheme described below.

Because the ORM has distinct `float` and `str` columns to support indexing,
there will be no plain strings in the remaining JSON blob column.
Therefore we support other types by providing functions
to convert each type to a `str` and back,
and an associated "type label" which will be prefixed to the string;
the resulting string is stored in the JSON blob.

The default mechanism is based on the following class attributes and methods:
* `TYPE_JS_MAPPING`: a mapping of a type label string
  to a 3 tuple of `(type,to_str,from_str)`
  being the extended type,
  a function to convert an instance to `str`
  and a function to convert a `str` to an instance of this type
* `to_js_str`: a method accepting `(tag_name,tag_value)`
  and returning `tag_value` as a `str`;
  the default implementation looks up the type of `tag_value`
  in `TYPE_JS_MAPPING` to locate the corresponding `to_str` function
* `from_js_str`: a method accepting `(tag_name,js)`
  which uses the leading type label prefix from the `js`
  to look up the corresponding `from_str` function
  from `TYPE_JS_MAPPING` and use it on the tail of `js`

The default `TYPE_JS_MAPPING` has mappings for:
* `"bigint"`: conversions for `int`
* `"date"`: conversions for `datetime.date`
* `"datetime"`: conversions for `datetime.datetime`

Subclasses wanting to augument the `TYPE_JS_MAPPING`
should prepare their own with code such as:

    class SubSQLTagSet(SQLTagSet,....):
        ....
        TYPE_JS_MAPPING=dict(SQLTagSet.TYPE_JS_MAPPING)
        TYPE_JS_MAPPING.update(
          typelabel=(type, to_str, from_str),
          ....
        )

*Method `SQLTagSet.add_db_tag(self, *a, **kw)`*:
Add a tag to the database.

*Method `SQLTagSet.child_tagsets(self, tag_name='parent')`*:
Return the child `TagSet`s as defined by their parent `Tag`,
by default the `Tag` named `'parent'`.

*Method `SQLTagSet.db_session(self, new=False)`*:
Context manager to obtain a new session if required,
just a shim for `self.sqltags.db_session`.

*Method `SQLTagSet.discard_db_tag(self, tag_name: str, pv: Optional[cs.sqltags.PolyValue] = None)`*:
Discard a tag from the database.

*Method `SQLTagSet.from_js_str(tag_name: str, js: str)`*:
Convert the `str` `js` to a `Tag` value.
This is the reverse of `as_js_str`.

Subclasses wanting extra type support
should either:
(usual approach) provide their own `TYPE_JS_MAPPING` class attribute
as described at the top of this class
or (for unusual requirements) override this method and also `to_js_str`.

*Method `SQLTagSet.from_polyvalue(tag_name: str, pv: cs.sqltags.PolyValue)`*:
Convert an SQL `PolyValue` to a tag value.

This can be overridden by subclasses along with `to_polyvalue`.
The `tag_name` is provided for context
in case it should influence the normalisation.

*Property `SQLTagSet.name`*:
Return the `.name`.

*Method `SQLTagSet.parent_tagset(self, tag_name='parent')`*:
Return the parent `TagSet` as defined by a `Tag`,
by default the `Tag` named `'parent'`.

*Method `SQLTagSet.to_js_str(tag_name: str, tag_value) -> str`*:
Convert `tag_value` to a `str` suitable for storage in `structure_value`.
This can be reversed by `from_js_str`.

Subclasses wanting extra type support
should either:
(usual approach) provide their own `TYPE_JS_MAPPING` class attribute
as described at the top of this class
or (for unusual requirements) override this method and also `from_js_str`.

*Method `SQLTagSet.to_polyvalue(tag_name: str, tag_value) -> cs.sqltags.PolyValue`*:
Normalise `Tag` values for storage via SQL.
Preserve things directly expressable in JSON.
Convert other values via `to_js_str`.
Return `PolyValue` for use with the SQL rows.

## Class `SQLTagsORM(cs.sqlalchemy_utils.ORM, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, cs.dateutils.UNIXTimeMixin)`

The ORM for an `SQLTags`.

The current implementation uses 3 tables:
* `entities`: this has a NULLable `name`
  and `unixtime` UNIX timestamp;
  this is unique per `name` if the name is not NULL
* `tags`: this has an `entity_id`, `name` and a value stored
  in one of three columns: `float_value`, `string_value` and
  `structured_value` which is a JSON blob;
  this is unique per `(entity_id,name)`
* `tag_subvalues`: this is a broken out version of `tags`
  when `structured_value` is a sequence or mapping,
  breaking out the values one per row;
  this exists to support "tag contains value" lookups

Tag values are stored as follows:
* `None`: all 3 columns are set to `NULL`
* `float`: stored in `float_value`
* `int`: if the `int` round trips to `float`
  then it is stored in `float_value`,
  otherwise it is stored in `structured_value`
  with the type label `"bigint"`
* `str`: stored in `string_value`
* `list`, `tuple`, `dict`: stored in `structured_value`;
  if these containers contain unJSONable content there will be trouble
* other types, such as `datetime`:
  these are converted to strings with identifying type label prefixes
  and stored in `structured_value`

The `float_value` and `string_value` columns
allow us to provide indices for these kinds of tag values.

The type label scheme takes advantage of the fact that actual `str`s
are stored in the `string_value` column.
Because of this, there will be no actual strings in `structured_value`.
Therefore, we can convert nonJSONable types to `str` and store them here.

The scheme used is to provide conversion functions to convert types
to `str` and back, and an associated "type label" prefix.
For example, we store a `datetime` as the ISO format of the `datetime`
with `"datetime:"` prefixed to it.

The actual conversions are kept with the `SQLTagSet` class
(or any subclass).
This ORM receives the 3-tuples of SQL ready values
from that class as the `PolyValue` `namedtuple`
and does not perform any conversion itself.
The conversion process is described in `SQLTagSet`.

*Method `SQLTagsORM.declare_schema(self)`*:
Define the database schema / ORM mapping.

*Method `SQLTagsORM.define_schema(self)`*:
Instantiate the schema and define the root metanode.

*Method `SQLTagsORM.prepare_metanode(self, *, session)`*:
Ensure row id 0, the metanode, exists.

*Method `SQLTagsORM.search(self, *a, **kw)`*:
Construct a query to match `Entity` rows
matching the supplied `criteria` iterable.
Return an SQLAlchemy `Query`.

The `mode` parameter has the following values:
* `'id'`: the query only yields entity ids
* `'entity'`: (default) the query yields entities without tags
* `'tagged'`: (default) the query yields entities left
outer joined with their matching tags

Note that the `'tagged'` result produces multiple rows for any
entity with multiple tags, and that this requires the caller to
fold entities with multiple tags together.

*Note*:
due to implementation limitations
the SQL query itself may not apply all the criteria,
so every criterion must still be applied
to the results
using its `.match_entity` method.

If `name` is omitted or `None` the query will match log entities
otherwise the entity with the specified `name`.

The `criteria` should be an iterable of `SQTCriterion` instances
used to construct the query.

## Class `SQTCriterion(cs.tagset.TagSetCriterion)`

Subclass of `TagSetCriterion` requiring an `.sql_parameters` method
which returns an `SQLParameters` providing the information required
to construct an sqlalchemy query.
It also resets `.CRITERION_PARSE_CLASSES`, which will pick up
the SQL capable criterion classes below.

*`SQTCriterion.TAG_BASED_TEST_CLASS`*

*Method `SQTCriterion.from_equality(tag_name, tag_value)`*:
Return an `SQTCriterion` instance based on `tag_name==tag_value`.
This supports `SQLTags.find`'s keyword parameters.

*Method `SQTCriterion.match_tagged_entity(self, te: cs.tagset.TagSet) -> bool`*:
Perform the criterion test on the Python object directly.
This is used at the end of a query to implement tests which
cannot be sufficiently implemented in SQL.
If `self.SQL_COMPLETE` it is not necessary to call this method.

*Method `SQTCriterion.sql_parameters(self, orm) -> cs.sqltags.SQLParameters`*:
Subclasses must return am `SQLParameters` instance
parameterising the SQL queries that follow.

## Class `SQTEntityIdTest(SQTCriterion, cs.tagset.TagSetCriterion)`

A test on `entity.id`.

*Method `SQTEntityIdTest.match_tagged_entity(self, te: cs.tagset.TagSet) -> bool`*:
Test the `TagSet` `te` against `self.entity_ids`.

*Method `SQTEntityIdTest.parse(s, offset=0, delim=None)`*:
Parse a decimal entity id from `s`.

## Function `verbose(msg, *a)`

Emit message if in verbose mode.

# Release Log



*Release 20220606*:
* New SQLTagsORM.Entities.add_new_tags method, use it in SQLTags.default_factory for bulk insert.
* SQTCriterion: new .from_equality(tag_name,tag_value) factory to make an equality criterion.
* SQLTags.find: accept criteria as positional parameters instead of a single iterable, accept new keyword parameters as equality criteria.
* SQLTags.__getitem__: accept a slice to index the .unixtime tag.
* SQLTagsORM: also turn on echo mode if "ECHO" in $SQLTAGS_MODES.

*Release 20220311*:
Assorted updates.

*Release 20211212*:
* Rename edit_many to edit_tagsets for clarity.
* Small bugfixes.

*Release 20210913*:
* SQLTagsCommand: rename cmd_ns to cmd_list,cmd_ls.
* SQLTagsCommand.cmd_export: accept "-F export_format" for csv or fstags export, accept no criteria to mean all tagsets.
* Encoding schema for nonJSONable types.
* Rename the TagSets abstract base class to BaseTagSets.
* BaseSQLTagsCommand.cmd_edit: implement rename.
* Many other internal small changes.

*Release 20210420*:
* New PolyValueMixin pulled out of Tags for common support of the (float_value,string_value,structured_value).
* SQLTagsORM: new TagSubValues relation containing broken out values for values which are sequences, to support efficient lookup if sequence values such as log entry categories.
* New BaseSQLTagsCommand.parse_categories static method to parse FOO,BAH into ['foo','bah'].
* sqltags find: change default format to "{datetime} {headline}".
* Assorted small changes.

*Release 20210404*:
* SQLTags.__getitem__: when autocreating an entity, do it in a new session so that the entity is commited to the database before any further use.
* SQLTagsCommand: new cmd_dbshell to drop you into the database.

*Release 20210321*:
Drop logic now merged with cs.sqlalchemy_utils, use the new default session stuff.

*Release 20210306.1*:
Docstring updates.

*Release 20210306*:
Initial release.
