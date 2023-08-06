Efficient portable machine native columnar storage of time series data
for double float and signed 64-bit integers.

*Latest release 20220606*:
Initial PyPI release.

The core purpose is to provide time series data storage; there
are assorted convenience methods to export arbitrary subsets
of the data for use by other libraries in common forms, such
as dataframes or series, numpy arrays and simple lists.
There are also some simple plot methods for plotting graphs.

Three levels of storage are defined here:
- `TimeSeriesFile`: a single file containing a binary list of
  float64 or signed int64 values
- `TimeSeriesPartitioned`: a directory containing multiple
  `TimeSeriesFile` files, each covering a separate time span
  according to a supplied policy, for example a calendar month
- `TimeSeriesDataDir`: a directory containing multiple
  `TimeSeriesPartitioned` subdirectories, each for a different
  time series, for example one subdirectory for grid voltage
  and another for grid power

Together these provide a hierarchy for finite sized files storing
unbounded time series data for multiple parameters.

On a personal basis, I use this as efficient storage of time
series data from my solar inverter, which reports in a slightly
clunky time limited CSV format; I import those CSVs into
time series data directories which contain the overall accrued
data; see my `cs.splink` module which is built on this module.

## Function `array_byteswapped(ary)`

Context manager to byteswap the `array.array` `ary` temporarily.

## Class `ArrowBasedTimespanPolicy(TimespanPolicy, icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A `TimespanPolicy` based on an Arrow format string.

See the `raw_edges` method for the specifics of how these are defined.

*Method `ArrowBasedTimespanPolicy.Arrow(self, when)`*:
Return an `arrow.Arrow` instance for the UNIX time `when`
in the policy timezone.

*Method `ArrowBasedTimespanPolicy.make(name, partition_format, shift)`*:
Create and register a simple `ArrowBasedTimespanPolicy`.
Return the new policy.

Parameters:
* `name`: the name for the policy; this can also be a sequence of names
* `partition_format`: the Arrow format string for naming time partitions
* `shift`: a mapping of parameter values for `Arrow.shift()`
  defining the time step from one partition to the next

*Method `ArrowBasedTimespanPolicy.name_for_time(self, when)`*:
Return a time span name for the UNIX time `when`.

*Method `ArrowBasedTimespanPolicy.partition_format_cononical(self, txt)`*:
Modify the formatted text derived from `self.PARTITION_FORMAT`.

The driving example is the 'weekly' policy, which uses
Arrow's 'W' ISO week format but trims the sub-week day
suffix.  This is sufficient if Arrow can parse the trimmed
result, which it can for 'W'. If not, a subclass might need
to override this method.

*Method `ArrowBasedTimespanPolicy.raw_edges(self, when: Union[int, float])`*:
Return the _raw_ start and end UNIX times
(inclusive and exclusive respectively)
bracketing the UNIX time `when`.

This implementation performs the following steps:
* get an `Arrow` instance in the policy timezone from the
  UNIX time `when`
* format that instance using `self.PARTITION_FORMAT`,
  modified by `self.partition_format_cononical`
* parse that string into a new `Arrow` instance which is
  the raw start time
* compute the raw end time as `calendar_start.shift(**self.ARROW_SHIFT_PARAMS)`
* return the UNIX timestamps for the raw start and end times

*Method `ArrowBasedTimespanPolicy.span_for_name(self, *a, **kw)`*:
Return a `TimePartition` derived from the `span_name`.

## Function `deduce_type_bigendianness(typecode: str) -> bool`

Deduce the native endianness for `typecode`,
an array/struct typecode character.

## Class `Epoch(Epoch, builtins.tuple, TimeStepsMixin)`

The basis of time references with a starting UNIX time, the
`epoch` and the `step` defining the width of a time slot.

*Method `Epoch.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `Epoch`, handy for use with `pformat()` or `pprint()`.

*Method `Epoch.promote(epochy)`*:
Promote `epochy` to an `Epoch` (except for `None`).

`None` remains `None`.

An `Epoch` remains unchanged.

An `int` or `float` argument will be used as the `step` in
an `Epoch` starting at `0`.

A 2-tuple of `(start,step)` will be used to construct a new `Epoch` directly.

*Property `Epoch.typecode`*:
The `array` typecode for the times from this `Epoch`.
This returns `typecode_of(type(self.start))`.

## Function `get_default_timezone_name()`

Return the default timezone name.

## Class `HasEpochMixin(TimeStepsMixin)`

A `TimeStepsMixin` with `.start` and `.step` derive from `self.epoch`.

*Method `HasEpochMixin.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `HasEpochMixin`, handy for use with `pformat()` or `pprint()`.

*Property `HasEpochMixin.start`*:
The start UNIX time from `self.epoch.start`.

*Property `HasEpochMixin.step`*:
The time slot width from `self.epoch.step`.

*Property `HasEpochMixin.time_typecode`*:
The `array` typecode for times from `self.epoch`.

## Function `main(argv=None)`

Run the command line tool for `TimeSeries` data.

## Function `plot_events(ax, events, value_func, *, start=None, stop=None, **scatter_kw)`

Plot `events`, an iterable of objects with `.unixtime` attributes
such as an `SQLTagSet`, on an existing set of axes `ax`.

Parameters:
* `ax`: axes on which to plot
* `events`: an iterable of objects with `.unixtime` attributes
* `value_func`: a callable to compute the y-axis value from an event
* `start`: optional start UNIX time, used to crop the events plotted
* `stop`: optional stop UNIX time, used to crop the events plotted
Other keyword parameters are passed to `Axes.scatter`.

## Function `plotrange(*da, **dkw)`

A decorator for plotting methods with optional `start` and `stop`
leading positional parameters and an optional `figure` keyword parameter.

The decorator parameters `needs_start` and `needs_stop`
may be set to require non-`None` values for `start` and `stop`.

If `start` is `None` its value is set to `self.start`.
If `stop` is `None` its value is set to `self.stop`.

The decorated method is then called as:

    func(self, start, stop, *a, **kw)

where `*a` and `**kw` are the additional positional and keyword
parameters respectively, if any.

## Function `print_figure(figure_or_ax, imgformat=None, file=None)`

Print `figure_or_ax` to a file.

Parameters:
* `figure_or_ax`: a `matplotlib.figure.Figure` or an object
  with a `.figure` attribute such as a set of `Axes`
* `imgformat`: optional output format; if omitted use `'sixel'`
  if `file` is a terminal, otherwise `'png'`
* `file`: the output file, default `sys.stdout`

## Function `save_figure(figure_or_ax, imgpath: str, force=False)`

Save a `Figure` to the file `imgpath`.

Parameters:
* `figure_or_ax`: a `matplotlib.figure.Figure` or an object
  with a `.figure` attribute such as a set of `Axes`
* `imgpath`: the filesystem path to which to save the image
* `force`: optional flag, default `False`: if true the `imgpath`
  will be written to even if it exists

## Function `saved_figure(figure_or_ax, dir=None, ext=None)`

Context manager to save a `Figure` to a file and yield the file path.

Parameters:
* `figure_or_ax`: a `matplotlib.figure.Figure` or an object
  with a `.figure` attribute such as a set of `Axes`
* `dir`: passed to `tempfile.TemporaryDirectory`
* `ext`: optional file extension, default `'png'`

## Function `struct_format(typecode, bigendian)`

Return a `struct` format string for the supplied `typecode` and big endianness.

## Class `TimePartition(TimePartition, builtins.tuple, TimeStepsMixin)`

A `namedtuple` for a slice of time with the following attributes:
* `epoch`: the reference `Epoch`
* `name`: the name for this slice
* `offset0`: the epoch offset of the start time (`self.start`)
* `steps`: the number of time slots in this partition

These are used by `TimespanPolicy` instances to express the partitions
into which they divide time.

*Method `TimePartition.__contains__(self, when: Union[int, float]) -> bool`*:
Test whether the UNIX timestamp `when` lies in this partition.

*Method `TimePartition.__iter__(self)`*:
A generator yielding times from this partition from
`self.start` to `self.stop` by `self.step`.

*Method `TimePartition.offsets(self)`*:
Return an iterable of the epoch offsets from `self.start` to `self.stop`.

*Property `TimePartition.start`*:
The start UNIX time derived from `self.epoch` and `self.offset0`.

*Property `TimePartition.step`*:
The epoch step size.

*Property `TimePartition.stop`*:
The start UNIX time derived from `self.epoch` and `self.offset0` and `self.steps`.

## Class `TimeSeries(cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, HasEpochMixin, TimeStepsMixin)`

Common base class of any time series.

*Method `TimeSeries.__getitem__(self, index)`*:
Return a datum or list of data.

*Method `TimeSeries.as_np_array(*a, **kw)`*:
Return a `numpy.array` 1xN array containing the data from `start` to `stop`,
default from `self.start` and `self.stop` respectively.

*Method `TimeSeries.as_pd_series(*a, **kw)`*:
Return a `pandas.Series` containing the data from `start` to `stop`,
default from `self.start` and `self.stop` respectively.

*Method `TimeSeries.data(self, start, stop)`*:
Return an iterable of `(when,datum)` tuples for each time `when`
from `start` to `stop`.

*Method `TimeSeries.data2(self, start, stop)`*:
Like `data(start,stop)` but returning 2 lists: one of time and one of data.

*Method `TimeSeries.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `TimeSeries`, handy for use with `pformat()` or `pprint()`.

*Property `TimeSeries.np_type`*:
The `numpy` type corresponding to `self.typecode`.

*Method `TimeSeries.plot(self, start=None, stop=None, *a, **kw)`*:
Convenience shim for `DataFrame.plot` to plot data from
`start` to `stop`.  Return the plot `Axes`.

Parameters:
* `start`,`stop`: the time range
* `runstate`: optional `RunState`, ignored in this implementation
* `label`: optional label for the graph
Other keyword parameters are passed to `DataFrame.plot`.

*Method `TimeSeries.startup_shutdown(self)`*:
This is required, even if empty.

## Function `timeseries_from_path(tspath: str, epoch: Union[cs.timeseries.Epoch, Tuple[Union[int, float], Union[int, float]], int, float, NoneType] = None, typecode=None)`

Turn a time series filesystem path into a time series:
* a file: a `TimeSeriesFile`
* a directory holding `.csts` files: a `TimeSeriesPartitioned`
* a directory: a `TimeSeriesDataDir`

## Class `TimeSeriesBaseCommand(cs.cmdutils.BaseCommand)`

Abstract base class for command line interfaces to `TimeSeries` data files.

Command line usage:

    Usage: timeseriesbase subcommand [...]
      Subcommands:
        fetch ...
          Fetch raw data files from the primary source to a local spool.
          To be implemented in subclasses.
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        import ...
          Import data into the time series.
          To be implemented in subclasses.
        info
          Report information.
        plot [-f] [-o imgpath.png] [--show] days [{glob|fields}...]
          Plot the most recent days of data from the time series at tspath.
          Options:
          -f              Force. -o will overwrite an existing image file.
          -o imgpath.png  File system path to which to save the plot.
          --show          Show the image in the GUI.
          --stacked       Stack the plot lines/areas.
          glob|fields     If glob is supplied, constrain the keys of
                          a TimeSeriesDataDir by the glob.

*Method `TimeSeriesBaseCommand.cmd_fetch(self, argv)`*:
Usage: {cmd} ...
Fetch raw data files from the primary source to a local spool.
To be implemented in subclasses.

*Method `TimeSeriesBaseCommand.cmd_import(self, argv)`*:
Usage: {cmd} ...
Import data into the time series.
To be implemented in subclasses.

*Method `TimeSeriesBaseCommand.cmd_info(self, argv)`*:
Usage: {cmd}
Report information.

*Method `TimeSeriesBaseCommand.cmd_plot(self, argv)`*:
Usage: {cmd} [-f] [-o imgpath.png] [--show] days [{{glob|fields}}...]
Plot the most recent days of data from the time series at tspath.
Options:
-f              Force. -o will overwrite an existing image file.
-o imgpath.png  File system path to which to save the plot.
--show          Show the image in the GUI.
--stacked       Stack the plot lines/areas.
glob|fields     If glob is supplied, constrain the keys of
                a TimeSeriesDataDir by the glob.

## Class `TimeSeriesCommand(TimeSeriesBaseCommand, cs.cmdutils.BaseCommand)`

Command line interface to `TimeSeries` data files.

Command line usage:

    Usage: timeseries [-s ts-step] tspath subcommand...
        -s ts-step  Specify the UNIX time step for the time series,
                    used if the time series is new and checked otherwise.
        tspath      The filesystem path to the time series;
                    this may refer to a single .csts TimeSeriesFile, a
                    TimeSeriesPartitioned directory of such files, or
                    a TimeSeriesDataDir containing partitions for
                    multiple keys.
      Subcommands:
        dump
          Dump the contents of tspath.
        fetch ...
          Fetch raw data files from the primary source to a local spool.
          To be implemented in subclasses.
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        import csvpath datecol[:conv] [import_columns...]
          Import data into the time series.
          csvpath   The CSV file to import.
          datecol[:conv]
                    Specify the timestamp column and optional
                    conversion function.
                    "datecol" can be either the column header name
                    or a numeric column index counting from 0.
                    If "conv" is omitted, the column should contain
                    a UNIX seconds timestamp.  Otherwise "conv"
                    should be either an identifier naming one of
                    the known conversion functions or an "arrow.get"
                    compatible time format string.
          import_columns
                    An optional list of column names or their derived
                    attribute names. The default is to import every
                    numeric column except for the datecol.
        info
          Report infomation about the time series stored at tspath.
        plot [-f] [-o imgpath.png] [--show] days [{glob|fields}...]
          Plot the most recent days of data from the time series at tspath.
          Options:
          -f              Force. -o will overwrite an existing image file.
          -o imgpath.png  File system path to which to save the plot.
          --show          Show the image in the GUI.
          --stacked       Stack the plot lines/areas.
          glob|fields     If glob is supplied, constrain the keys of
                          a TimeSeriesDataDir by the glob.
        test [testnames...]
          Run some tests of functionality.

*Method `TimeSeriesCommand.apply_preargv(self, argv)`*:
Parse a leading time series filesystem path from `argv`,
set `self.options.ts` to the time series,
return modified `argv`.

*Method `TimeSeriesCommand.cmd_dump(self, argv)`*:
Usage: {cmd}
Dump the contents of tspath.

*Method `TimeSeriesCommand.cmd_import(self, argv)`*:
Usage: {cmd} csvpath datecol[:conv] [import_columns...]
Import data into the time series.
csvpath   The CSV file to import.
datecol[:conv]
          Specify the timestamp column and optional
          conversion function.
          "datecol" can be either the column header name
          or a numeric column index counting from 0.
          If "conv" is omitted, the column should contain
          a UNIX seconds timestamp.  Otherwise "conv"
          should be either an identifier naming one of
          the known conversion functions or an "arrow.get"
          compatible time format string.
import_columns
          An optional list of column names or their derived
          attribute names. The default is to import every
          numeric column except for the datecol.

*Method `TimeSeriesCommand.cmd_info(self, argv)`*:
Usage: {cmd}
Report infomation about the time series stored at tspath.

*Method `TimeSeriesCommand.cmd_test(self, argv)`*:
Usage: {cmd} [testnames...]
Run some tests of functionality.

## Class `TimeSeriesDataDir(TimeSeriesMapping, builtins.dict, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, cs.fs.HasFSPath, cs.configutils.HasConfigIni, HasEpochMixin, TimeStepsMixin)`

A directory containing a collection of `TimeSeriesPartitioned` subdirectories.

*Method `TimeSeriesDataDir.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `TimeSeriesDataDir`, handy for use with `pformat()` or `pprint()`.

*Method `TimeSeriesDataDir.keys(self, fnglobs: Union[str, List[str], NoneType] = None)`*:
Return a list of the known keys, derived from the subdirectories,
optionally constrained by `fnglobs`.
If provided, `fnglobs` may be a glob string or list of glob strings
suitable for `fnmatch`.

*Method `TimeSeriesDataDir.make_ts(self, key)`*:
Create a `TimeSeriesPartitioned` for `key`.

*Property `TimeSeriesDataDir.policy_name`*:
The `policy.name` config value, usually a key from
`TimespanPolicy.FACTORIES`.

*Method `TimeSeriesDataDir.startup_shutdown(self)`*:
Context manager for `MultiOpenMixin`.
Close the sub time series and save the config if modified.

*Property `TimeSeriesDataDir.tzinfo`*:
The `policy.tzinfo` config value, a timezone name.

## Class `TimeSeriesFile(TimeSeries, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, HasEpochMixin, TimeStepsMixin, cs.fs.HasFSPath)`

A file containing a single time series for a single data field.

This provides easy access to a time series data file.
The instance can be indexed by UNIX time stamp for time based access
or its `.array` property can be accessed for the raw data.

Read only users can just instantiate an instance.
Read/write users should use the instance as a context manager,
which will automatically rewrite the file with the array data
on exit.

Note that the save-on-close is done with `TimeSeries.flush()`
which ony saves if `self.modified`.
Use of the `__setitem__` or `pad_to` methods set this flag automatically.
Direct access via the `.array` will not set it,
so users working that way for performance should update the flag themselves.

The data file itself has a header indicating the file data big endianness,
the datum type and the time type (both `array.array` type codes).
Following these are the start and step sizes in the time type format.
This is automatically honoured on load and save.

*Method `TimeSeriesFile.__init__(self, fspath: str, typecode: Optional[str] = None, *, epoch: Union[cs.timeseries.Epoch, Tuple[Union[int, float], Union[int, float]], int, float, NoneType] = None, fill=None, fstags=None)`*:
Prepare a new time series stored in the file at `fspath`
containing machine data for the time series values.

Parameters:
* `fspath`: the filename of the data file
* `typecode` optional expected `array.typecode` value of the data;
  if specified and the data file exists, they must match;
  if not specified then the data file must exist
  and the `typecode` will be obtained from its header
* `start`: the UNIX epoch time for the first datum
* `step`: the increment between data times
* `time_typecode`: the type of the start and step times;
  inferred from the type of the start time value if unspecified
* `fill`: optional default fill values for `pad_to`;
  if unspecified, fill with `0` for `'q'`
  and `float('nan') for `'d'`

If `start` or `step` are omitted the file's fstags will be
consulted for their values.
This class does not set these tags (that would presume write
access to the parent directory or its `.fstags` file)
when a `TimeSeriesFile` is made by a `TimeSeriesPartitioned` instance
it sets these flags.

*Method `TimeSeriesFile.__getitem__(self, when: Union[int, float, slice])`*:
Return the datum for the UNIX time `when`.

If `when` is a slice, return a list of the data
for the times in the range `start:stop`
as given by `self.range(start,stop)`.
This will raise an `IndexError` if `start` corresponds to
an offset before the beginning of the array.

*Method `TimeSeriesFile.__setitem__(self, when, value)`*:
Set the datum for the UNIX time `when`.

*Property `TimeSeriesFile.array`*:
The time series as an `array.array` object.
This loads the array data from `self.fspath` on first use.

*Method `TimeSeriesFile.array_index(self, when) -> int`*:
Return the array index corresponding the time UNIX time `when`.

*Method `TimeSeriesFile.array_index_bounds(self, start, stop) -> (<class 'int'>, <class 'int'>)`*:
Return a `(array_start,array_stop)` pair for the array indices
between the UNIX times `start` and `stop`.

Example:

   >>> ts = TimeSeriesFile('tsfile.csts', 'd', epoch=(19.1, 1.2))
   >>> ts.array_index_bounds(20,30)
   (0, 9)

*Method `TimeSeriesFile.array_indices(self, start, stop)`*:
Return an iterable of the array indices for the UNIX times
from `start` to `stop` from this `TimeSeries`.

Example:

   >>> ts = TimeSeriesFile('tsfile.csts', 'd', epoch=(19.1, 1.2))
   >>> list(ts.array_indices(20,30))
   [0, 1, 2, 3, 4, 5, 6, 7, 8]

*Method `TimeSeriesFile.array_length(self)`*:
The length of the time series data,
from `len(self.array)`.

*Method `TimeSeriesFile.file_offset(self, offset)`*:
Return the file position for the data with position `offset`.

*Method `TimeSeriesFile.flush(self, keep_array=False)`*:
Save the data file if `self.modified`.

*Method `TimeSeriesFile.index_when(self, index: int)`*:
Return the UNIX time corresponding to the array index `index`.

*Method `TimeSeriesFile.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `TimeSeriesFile`, handy for use with `pformat()` or `pprint()`.

*Method `TimeSeriesFile.offset_slice(self, astart, astop)`*:
Return a slice of the underlying array
for the array indices `astart:astop`.

*Method `TimeSeriesFile.pad_to(self, when, fill=None)`*:
Pad the time series to store values up to the UNIX time `when`.

The `fill` value is optional and defaults to the `fill` value
supplied when the `TimeSeries` was initialised.

*Method `TimeSeriesFile.peek(self, when: Union[int, float])`*:
Read a single data value for the UNIX time `when`.

This method uses the `mmap` interface if the array is not already loaded.

*Method `TimeSeriesFile.peek_offset(self, offset)`*:
Read a single data value from `offset`.

This method uses the `mmap` interface if the array is not already loaded.

*Method `TimeSeriesFile.poke(self, when: Union[int, float], value: Union[int, float])`*:
Write a single data value for the UNIX time `when`.

This method uses the `mmap` interface if the array is not already loaded.

*Method `TimeSeriesFile.poke_offset(self, offset: int, value: Union[int, float])`*:
Write a single data value at `offset`.

This method uses the `mmap` interface if the array is not already loaded.

*Method `TimeSeriesFile.save(self, fspath=None)`*:
Save the time series to `fspath`, default `self.fspath`.

*Method `TimeSeriesFile.save_to(self, fspath: str)`*:
Save the time series to `fspath`.

*Warning*:
if the file endianness is not the native endianness,
the array will be byte swapped temporarily
during the file write operation.
Concurrent users should avoid using the array during this function.

*Method `TimeSeriesFile.slice(self, start, stop, pad=False, prepad=False)`*:
Return a slice of the underlying array
for the times `start:stop`.

If `stop` implies values beyond the end of the array
and `pad` is true, pad the resulting list with `self.fill`
to the expected length.

If `start` corresponds to an offset before the start of the array
raise an `IndexError` unless `prepad` is true,
in which case the list of values will be prepended
with enough of `self.fill` to reach the array start.
If `prepad` is true, pad the resulting list at the beginning

*Property `TimeSeriesFile.stop`*:
The end time of this array;
the UNIX time of the first time slot beyond the end of the array.

*Property `TimeSeriesFile.tags`*:
The `TagSet` associated with this `TimeSeriesFile` instance.

## Class `TimeSeriesFileHeader(cs.binary.SimpleBinary, types.SimpleNamespace, cs.binary.AbstractBinary, cs.binary.BinaryMixin, HasEpochMixin, TimeStepsMixin)`

The binary data structure of the `TimeSeriesFile` file header.

This is 24 bytes long and consists of:
* the 4 byte magic number, `b'csts'`
* the file bigendian marker, a `struct` byte order indicator
  with a value of `b'>'` for big endian data
  or `b'<'` for little endian data
* the datum typecode, `b'd'` for double float
  or `b'q'` for signed 64 bit integer
* the time typecode, `b'd'` for double float
  or `b'q'` for signed 64 bit integer
* a pad byte, value `b'_'`
* the start UNIX time, a double float or signed 64 bit integer
  according to the time typecode and bigendian flag
* the step size, a double float or signed 64 bit integer
  according to the time typecode and bigendian flag

In addition to the header values tnd methods this also presents:
* `datum_type`: a `BinarySingleStruct` for the binary form of a data value
* `time_type`:  a `BinarySingleStruct` for the binary form of a time value

*Method `TimeSeriesFileHeader.parse(bfr)`*:
Parse the header record, return a `TimeSeriesFileHeader`.

*Property `TimeSeriesFileHeader.struct_endian_marker`*:
The endianness indicatoe for a `struct` format string.

*Method `TimeSeriesFileHeader.transcribe(self)`*:
Transcribe the header record.

## Class `TimeSeriesMapping(builtins.dict, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, HasEpochMixin, TimeStepsMixin)`

A group of named `TimeSeries` instances, indexed by a key.

This is the basis for `TimeSeriesDataDir`.

*Method `TimeSeriesMapping.__missing__(self, key)`*:
Create a new entry for `key` if missing.
This implementation looks up the rules.

*Method `TimeSeriesMapping.__setitem__(self, key: str, ts)`*:
Insert a time series into this `TimeSeriesMapping`.
`key` may not already be present.

*Method `TimeSeriesMapping.as_pd_dataframe(*a, **kw)`*:
Return a `numpy.DataFrame` containing the specified data.

Parameters:
* `start`: start time of the data
* `stop`: end time of the data
* `keys`: optional iterable of keys, default from `self.keys()`

*Method `TimeSeriesMapping.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `TimeSeriesMapping`, handy for use with `pformat()` or `pprint()`.

*Method `TimeSeriesMapping.key_typecode(self, key)`*:
The `array` type code for `key`.
This default method returns `'d'` (float64).

*Method `TimeSeriesMapping.plot(self, start=None, stop=None, *a, **kw)`*:
Convenience shim for `DataFrame.plot` to plot data from
`start` to `stop` for each key in `keys`.
Return the plot `Axes`.

Parameters:
* `start`: optional start, default `self.start`
* `stop`: optional stop, default `self.stop`
* `keys`: optional list of keys, default all keys
* `label`: optional label for the graph
Other keyword parameters are passed to `DataFrame.plot`.

*Method `TimeSeriesMapping.startup_shutdown(self)`*:
Context manager for `MultiOpenMixin`.
Close the sub time series.

*Method `TimeSeriesMapping.validate_key(key)`*:
Check that `key` is a valid key, raise `valueError` if not.
This implementation requires that `key` is an identifier.

## Class `TimeSeriesPartitioned(TimeSeries, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, HasEpochMixin, TimeStepsMixin, cs.fs.HasFSPath)`

A collection of `TimeSeries` files in a subdirectory.
We have one of these for each `TimeSeriesDataDir` key.

This class manages a collection of files
named by the partition from a `TimespanPolicy`,
which dictates which partition holds the datum for a UNIX time.

*Method `TimeSeriesPartitioned.__init__(self, dirpath: str, typecode: str, *, epoch: Union[cs.timeseries.Epoch, Tuple[Union[int, float], Union[int, float]], int, float, NoneType] = None, policy, fstags: Optional[cs.fstags.FSTags] = None)`*:
Initialise the `TimeSeriesPartitioned` instance.

Parameters:
* `dirpath`: the directory filesystem path,
  known as `.fspath` within the instance
* `typecode`: the `array` type code for the data
* `epoch`: the time series `Epoch`
* `policy`: the partitioning `TimespanPolicy`

The instance requires a reference epoch
because the `policy` start times will almost always
not fall on exact multiples of `epoch.step`.
The reference allows for reliable placement of times
which fall within `epoch.step` of a partition boundary.
For example, if `epoch.start==0` and `epoch.step==6` and a
partition boundary came at `19` due to some calendar based
policy then a time of `20` would fall in the partion left
of the boundary because it belongs to the time slot commencing
at `18`.

If `epoch` or `typecode` are omitted the file's
fstags will be consulted for their values.
The `start` parameter will further fall back to `0`.
This class does not set these tags (that would presume write
access to the parent directory or its `.fstags` file)
when a `TimeSeriesPartitioned` is made by a `TimeSeriesDataDir`
instance it sets these flags.

*Method `TimeSeriesPartitioned.__getitem__(self, index: Union[int, float, slice, str])`*:
Obtain various things from this `TimeSeriesPartitioned`
according to the type of `index`:
* `int` or `float`: the value for the UNIX timestamp `index`
* `slice`: a list of the values for the UNIX timestamp slice `index`
* `*.csts`: the `TimeSeriesFile` named `index` within this
  `TimeSeriesPartitioned`
* partition name: the `TimeSeriesFile` for the policy time partition

*Method `TimeSeriesPartitioned.data(self, start, stop)`*:
Return a list of `(when,datum)` tuples for the slot times from `start` to `stop`.

*Method `TimeSeriesPartitioned.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `TimeSeriesPartitioned`, handy for use with `pformat()` or `pprint()`.

*Method `TimeSeriesPartitioned.partition(self, start, stop)`*:
Return an iterable of `(when,subseries)` for each time `when`
from `start` to `stop`.

*Method `TimeSeriesPartitioned.partition_name_from_filename(tsfilename: str) -> str`*:
Return the time span name from a `TimeSeriesFile` filename.

*Method `TimeSeriesPartitioned.partitioned_spans(self, start, stop)`*:
Generator yielding a sequence of `TimePartition`s covering
the range `start:stop` such that `start` falls within the first
partition via `self.policy`.

*Method `TimeSeriesPartitioned.plot(self, start=None, stop=None, *a, **kw)`*:
Convenience shim for `DataFrame.plot` to plot data from
`start` to `stop`.  Return the plot `Axes`.

Parameters:
* `start`,`stop`: the time range
* `ax`: optional `Axes`; new `Axes` will be made if not specified
* `label`: optional label for the graph
Other keyword parameters are passed to `Axes.plot`
or `DataFrame.plot` for new axes.

*Method `TimeSeriesPartitioned.setitems(self, whens, values, *, skipNone=False)`*:
Store `values` against the UNIX times `whens`.

This is most efficient if `whens` are ordered.

*Property `TimeSeriesPartitioned.start`*:
The earliest time in any component `TimeSeriesFile`.

*Method `TimeSeriesPartitioned.startup_shutdown(self)`*:
Close the subsidiary `TimeSeries` instances.

*Property `TimeSeriesPartitioned.stop`*:
The latest time in any component `TimeSeriesFile`.

*Method `TimeSeriesPartitioned.subseries(self, spec: Union[str, int, float])`*:
Return the `TimeSeries` for `spec`,
which may be a partition name or a UNIX time.

*Property `TimeSeriesPartitioned.tags`*:
The `TagSet` associated with this `TimeSeriesPartitioned` instance.

*Method `TimeSeriesPartitioned.timeseriesfile_from_partition_name(self, partition_name)`*:
Return the `TimeSeriesFile` associated with the supplied partition_name.

*Method `TimeSeriesPartitioned.timeseriesfiles(self)`*:
Return a mapping of partition name to associated `TimeSeriesFile`
for the existing time series data files.

*Method `TimeSeriesPartitioned.tsfilenames(self)`*:
Return a list of the time series data filenames.

## Class `TimespanPolicy(icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A class implementing a policy allocating times to named time spans.

The `TimeSeriesPartitioned` uses these policies
to partition data among multiple `TimeSeries` data files.

Probably the most important methods are:
* `span_for_time`: return a `TimePartition` from a UNIX time
* `span_for_name`: return a `TimePartition` a partition name

*Method `TimespanPolicy.__init__(self, epoch: Union[cs.timeseries.Epoch, Tuple[Union[int, float], Union[int, float]], int, float])`*:
Initialise the policy.

*Method `TimespanPolicy.from_name(policy_name: str, epoch: Union[cs.timeseries.Epoch, Tuple[Union[int, float], Union[int, float]], int, float, NoneType] = None, **policy_kw)`*:
Factory method to return a new `TimespanPolicy` instance
from the policy name,
which indexes `TimespanPolicy.FACTORIES`.

*Method `TimespanPolicy.name_for_time(self, when)`*:
Return a time span name for the UNIX time `when`.

*Method `TimespanPolicy.partitioned_spans(self, start, stop)`*:
Generator yielding a sequence of `TimePartition`s covering
the range `start:stop` such that `start` falls within the first
partition.

Note that these partitions fall in the policy partitions,
but are bracketed by `[round_down(start):stop]`.
As such they will have the correct policy partition names
but the boundaries of the first and last spans
start at `round_down(start)` and end at `stop` respectively.
This makes the returned spans useful for time ranges from a subseries.

*Method `TimespanPolicy.promote(*a, **kw)`*:
Factory to promote `policy` to a `TimespanPolicy` instance.

The supplied `policy` may be:
* `str`: return an instance of the named policy
* `TimespanPolicy` subclass: return an instance of the subclass
* `TimespanPolicy` instance: return the instance

*Method `TimespanPolicy.raw_edges(self, when: Union[int, float])`*:
Return the _raw_ start and end UNIX times
(inclusive and exclusive respectively)
bracketing the UNIX time `when`.
This is the core method that a policy must implement.

These are the direct times implied by the policy.
For example, with a policy for a calendar month
this would return the start second of that month
and the start second of the following month.

These times are used as the basis for the time slots allocated
to a particular partition by the `span_for_time(when)` method.

*Method `TimespanPolicy.register_factory(factory: Callable, name: str)`*:
Register a new policy `factory` under then supplied `name`.

*Method `TimespanPolicy.span_for_name(self, span_name)`*:
Return a `TimePartition` derived from the `span_name`.

*Method `TimespanPolicy.span_for_time(self, when)`*:
Return a `TimePartition` enclosing `when`, a UNIX timestamp.

The boundaries of the partition are derived from the "raw"
start and end times returned by the `raw_edges(when)` method,
but fall on time slot boundaries defined by `self.epoch`.

Because the raw start/end times will usually fall within a
time slot instead of exactly on an edge a decision must be
made as to which partition a boundary slot falls.

This implementation chooses that the time slot spanning the
"raw" start second of the partition belongs to that partition.
As a consequence, the last "raw" seconds of the partition
will belong to the next partition
as their time slot overlaps the "raw" start of the next partition.

*Method `TimespanPolicy.spans_for_times(self, whens)`*:
Generator yielding `(when,TimePartition)` for each UNIX
time in the iterabe `whens`.
This is most efficient if times for a particular span are adjacent,
trivially so if the times are ordered.

## Class `TimespanPolicyAnnual(ArrowBasedTimespanPolicy, TimespanPolicy, icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A annual time policy.
PARTITION_FORMAT = 'YYYY'
ARROW_SHIFT_PARAMS = {'years': 1}

## Class `TimespanPolicyDaily(ArrowBasedTimespanPolicy, TimespanPolicy, icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A daily time policy.
PARTITION_FORMAT = 'YYYY-MM-DD'
ARROW_SHIFT_PARAMS = {'days': 1}

## Class `TimespanPolicyMonthly(ArrowBasedTimespanPolicy, TimespanPolicy, icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A monthly time policy.
PARTITION_FORMAT = 'YYYY-MM'
ARROW_SHIFT_PARAMS = {'months': 1}

## Class `TimespanPolicyWeekly(ArrowBasedTimespanPolicy, TimespanPolicy, icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A weekly time policy.
PARTITION_FORMAT = 'W'
ARROW_SHIFT_PARAMS = {'weeks': 1}

*Method `TimespanPolicyWeekly.partition_format_cononical(self, txt)`*:
Modify the formatted text derived from `self.PARTITION_FORMAT`.

The driving example is the 'weekly' policy, which uses
Arrow's 'W' ISO week format but trims the sub-week day
suffix.  This is sufficient if Arrow can parse the trimmed
result, which it can for 'W'. If not, a subclass might need
to override this method.

## Class `TimespanPolicyYearly(ArrowBasedTimespanPolicy, TimespanPolicy, icontract._metaclass.DBC, HasEpochMixin, TimeStepsMixin)`

A annual time policy.
PARTITION_FORMAT = 'YYYY'
ARROW_SHIFT_PARAMS = {'years': 1}

## Class `TimeStepsMixin`

Methods for an object with `start` and `step` attributes.

*Method `TimeStepsMixin.offset(self, when: Union[int, float]) -> int`*:
Return the step offset for the UNIX time `when` from `self.start`.

Example in a `TimeSeries`:

   >>> ts = TimeSeriesFile('tsfile.csts', 'd', epoch=(19.1, 1.2))
   >>> ts.offset(19.1)
   0
   >>> ts.offset(20)
   0
   >>> ts.offset(22)
   2

*Method `TimeStepsMixin.offset_bounds(self, start, stop) -> (<class 'int'>, <class 'int'>)`*:
Return the bounds of `(start,stop)` as offsets
(`self.start` plus multiples of `self.step`).

*Method `TimeStepsMixin.offset_range(self, start, stop)`*:
Return an iterable of the offsets from `start` to `stop`
in units of `self.step`
i.e. `offset(start) == 0`.

Example in a `TimeSeries`:

   >>> ts = TimeSeriesFile('tsfile.csts', 'd', epoch=(19.1, 1.2))
   >>> list(ts.offset_range(20,30))
   [0, 1, 2, 3, 4, 5, 6, 7, 8]

*Method `TimeStepsMixin.range(self, start, stop)`*:
Return an iterable of the times from `start` to `stop`.

Eample in a `TimeSeries`:

   >>> ts = TimeSeriesFile('tsfile.csts', 'd', epoch=(19.1, 1.2))
   >>> list(ts.range(20,30))
   [19.1, 20.3, 21.5, 22.700000000000003, 23.900000000000002, 25.1, 26.3, 27.5, 28.700000000000003]


Note that if the `TimeSeries` uses `float` values for `start` and `step`
then the values returned here will not necessarily round trip
to array indicies because of rounding.

As such, these times are useful for supplying the index to
a time series as might be wanted for a graph, but are not
reliably useful to _obtain_ the values from the time series.
So this is reliable:

    # works well: pair up values with their times
    graph_data = zip(ts.range(20,30), ts[20:30])

but this is unreliable because of rounding:

    # unreliable: pair up values with their times
    times = list(ts.range(20, 30))
    graph_data = zip(times, [ts[t] for t in times])

The reliable form is available as the `data(start,stop)` method.

Instead, the reliable way to obtain the values between the
UNIX times `start` and `stop` is to directly fetch them
from the `array` underlying the `TimeSeries`.
This can be done using the `offset_bounds`
or `array_indices` methods to obtain the `array` indices,
for example:

    astart, astop = ts.offset_bounds(start, stop)
    return ts.array[astart:astop]

or more conveniently by slicing the `TimeSeries`:

    values = ts[start:stop]

*Method `TimeStepsMixin.round_down(self, when)`*:
Return `when` rounded down to the start of its time slot.

*Method `TimeStepsMixin.round_up(self, when)`*:
Return `when` rounded up to the start of the next time slot.

*Method `TimeStepsMixin.when(self, offset)`*:
Return `self.start+offset*self.step`.

## Function `type_of(typecode: str) -> type`

Return the type associated with `array` `typecode`.
This supports the types in `SUPPORTED_TYPECODES`: `int` and `float`.

## Function `typecode_of(type_) -> str`

Return the `array` typecode for the type `type_`.
This supports the types in `SUPPORTED_TYPECODES`: `int` and `float`.

# Release Log



*Release 20220606*:
Initial PyPI release.
