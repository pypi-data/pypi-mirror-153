Assorted utility functions for working with data
downloaded from Selectronics' SP-LINK programme
which communicates with their controllers.

*Latest release 20220606*:
Initial PyPI release.

I use this to gather and plot data from my solar inverter.

## Function `main(argv=None)`

SP-Link command line mode.

## Class `SPLinkCommand(cs.timeseries.TimeSeriesBaseCommand, cs.cmdutils.BaseCommand)`

Command line to work with SP-Link data downloads.

Command line usage:

    Usage: splink [-d spdpath] [-n] subcommand...
        -d spdpath  Specify the directory containing the SP-LInk downloads
                    and time series. Default from $SPLINK_DATADIR,
                    or '.'
        -n          No action; recite planned actions.
      Subcommands:
        fetch [-F rsync-source] [-nx] [-- [rsync-options...]]
          Rsync everything from rsync-source into the downloads area.
          -F    Fetch rsync source, default from $SPLINK_FETCH_SOURCE.
          -n    Passed to rsync. Just more convenient than putting it at the end.
          -x    Delete source files.
        help [-l] [subcommand-names...]
          Print the full help for the named subcommands,
          or for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        import [-d dataset,...] [-n] [sp-link-download...]
          Import CSV data from the downloads area into the time series data.
          -d datasets       Comma separated list of datasets to import.
                            Default datasets: DailySummaryData DetailedData EventData
          -f                Force. Import datasets even if already marked as
                            imported.
          -n                No action. Recite planned imports.
          sp-link-download  Specify specific individual downloads to import.
                            The default is any download not tagged as already
                            imported.
        info
          Report infomation about the time series stored at tspath.
        plot [--show] [-f] [-o imagepath] days {mode|[dataset:]{glob|field}}...

*Method `SPLinkCommand.apply_defaults(self)`*:
Set the default `spdpath`.

*Method `SPLinkCommand.apply_opt(self, opt, val)`*:
Handle an individual global command line option.

*Method `SPLinkCommand.cmd_fetch(self, argv)`*:
Usage: {cmd} [-F rsync-source] [-nx] [-- [rsync-options...]]
Rsync everything from rsync-source into the downloads area.
-F    Fetch rsync source, default from ${DEFAULT_FETCH_SOURCE_ENVVAR}.
-n    Passed to rsync. Just more convenient than putting it at the end.
-x    Delete source files.

*Method `SPLinkCommand.cmd_import(self, argv)`*:
Usage: {cmd} [-d dataset,...] [-n] [sp-link-download...]
Import CSV data from the downloads area into the time series data.
-d datasets       Comma separated list of datasets to import.
                  Default datasets: {ALL_DATASETS}
-f                Force. Import datasets even if already marked as
                  imported.
-n                No action. Recite planned imports.
sp-link-download  Specify specific individual downloads to import.
                  The default is any download not tagged as already
                  imported.

*Method `SPLinkCommand.cmd_info(self, argv)`*:
Usage: {cmd}
Report infomation about the time series stored at tspath.

*Method `SPLinkCommand.cmd_plot(self, argv)`*:
Usage: {cmd} [--show] [-f] [-o imagepath] days {{mode|[dataset:]{{glob|field}}}}...

*Method `SPLinkCommand.run_context(self)`*:
Define `self.options.spd`.

## Class `SPLinkCSVDir(cs.fs.HasFSPath)`

A class for working with SP-Link data downloads,
referring to a particular `PerformanceData*` download directory.

*Method `SPLinkCSVDir.csv_tagsets(csvpath)`*:
Yield `(unixtime,TagSet)` 2-tuples from the CSV file `csvpath`.

*Method `SPLinkCSVDir.csvfilename(*a, **kw)`*:
Return the CSV filename specified by `dataset`.

Example:

    self.csvpath('DetailedData')

*Method `SPLinkCSVDir.csvpath(self, dataset: str) -> str`*:
Return the CSV pathname specified by `dataset`.

Example:

    self.csvpath('DetailedData')

*Method `SPLinkCSVDir.dataset_tagsets(self, dataset: str)`*:
Yield `(unixtime,TagSet)` 2-tuples from the CSV file
associated with `dataset`.

*Method `SPLinkCSVDir.export_csv_to_timeseries(self, csvpath, tsd: cs.timeseries.TimeSeriesDataDir, tzname=None)`*:
Read the CSV file specified by `cvspath`
and export its contents into the `tsd:TimeSeriesDataDir.

*Method `SPLinkCSVDir.export_to_timeseries(self, dataset: str, tsd: cs.timeseries.TimeSeriesDataDir, tzname=None)`*:
Read the CSV file in `self.fspath` specified by `dataset`
and export its contents into the `tsd:TimeSeriesDataDir.

*Property `SPLinkCSVDir.sitename`*:
The site name inferred from a CSV data filename.

## Class `SPLinkData(cs.fs.HasFSPath, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin)`

A directory containing SP-LInk data.

This contains:
- `downloads`: a directory containing copies of various SP-Link
  downloads i.e. this contains directories named `PerformanceData_*`.
- `events.db`: accrued event data from the `EventData` CSV files
- `DailySummaryData`: an `SPLinkDataDir` containing accrued
  data from the `DailySummaryData` CSV files
- `DetailedData`: an `SPLinkDataDir` containing accrued data
  from the `DetailedData` CSV files

*Method `SPLinkData.__getattr__(self, tsname)`*:
Autodefine attributes for the known time series.

*Method `SPLinkData.datasetpath(self, perfdirpath, dataset)`*:
Return the filesystem path to the named `dataset`
from the SP-Link download subdirectory `perfdirpath`.

*Method `SPLinkData.download_subdirs(self)`*:
Return an iterable of the paths of the top level `PerformanceData_*`
subdirectories in the downloads subdirectory.

*Property `SPLinkData.downloadspath`*:
The filesystem path of the downloads subdirectory.

*Property `SPLinkData.eventsdb`*:
The events `SQLTags` database.

*Method `SPLinkData.info_dict(self, d=None)`*:
Return an informational `dict` containing salient information
about this `SPLinkData`, handy for use with `pformat()` or `pprint()`.

*Method `SPLinkData.parse_dataset_filename(path)`*:
Parse the filename part of `path` and derive an `SPLinkDataFileInfo`.
Raises `ValueError` if the filename cannot be recognised.

*Method `SPLinkData.plot(self, start, stop, *, key_specs, mode=None, figsize=None, dpi=None, event_labels=None)`*:
The core logic of the `SPLinkCommand.cmd_plot` method
to plot arbitrary parameters against a time range.

*Method `SPLinkData.resolve(self, spec)`*:
Resolve a field spec into an iterable of `(timeseries,key)`.

*Method `SPLinkData.startup_shutdown(self)`*:
Close the subsidiary time series on exit.

## Class `SPLinkDataDir(cs.timeseries.TimeSeriesDataDir, cs.timeseries.TimeSeriesMapping, builtins.dict, cs.resources.MultiOpenMixin, cs.context.ContextManagerMixin, cs.fs.HasFSPath, cs.configutils.HasConfigIni, cs.timeseries.HasEpochMixin, cs.timeseries.TimeStepsMixin)`

A `TimeSeriesDataDir` to hold log data from an SP-Link CSV data download.
This holds the data from a particular CSV log such as `'DetailedData'`.
The `SPLinkData` class manages a couple of these and a downloads
subdirectory and an events `SQLTags`.

*Method `SPLinkDataDir.__init__(self, dirpath, dataset: str, step: int, policy=None, **kw)`*:
Initialise the `SPLinkDataDir`.

Parameters:
* `dirpath`: the pathname of the directory holding the downloaded CSV files
* `dataset`: which CSV file populates this time series, eg `'DetailedData'`
* `step`: optional time series step size,
  default `SPLinkDataDir.DEFAULT_LOG_FREQUENCY`,
  which comes from `SPLinkCSVDir.DEFAULT_LOG_FREQUENCY`
* `policy`: optional TimespanPolicy` instance;
  if omitted an `TimespanPolicyYearly` instance will be made
Other keyword arguments are passed to the `TimeSeriesDataDir`
initialiser.

*`SPLinkDataDir.DEFAULT_POLICY_CLASS`*

*Method `SPLinkDataDir.import_from(self, csv, tzname=None)`*:
Import the CSV data from `csv` specified by `self.dataset`.

Parameters:
* `csv`: an `SPLinkCSVDir` instance or the pathname of a directory
  containing SP-Link CSV download data, or the pathname of a CSV file.

Example:

    spd = SPLinkDataDir('spdata/DetailedData')
    spd.import_from(
        'spl/PerformanceData_2021-07-04_13-02-38',
        'DetailedData',
    )

## Class `SPLinkDataFileInfo(builtins.tuple)`

SPLinkDataFileInfo(fspath, sitename, dataset, unixtime, dotext)

*Property `SPLinkDataFileInfo.dataset`*:
Alias for field number 2

*Property `SPLinkDataFileInfo.dotext`*:
Alias for field number 4

*Property `SPLinkDataFileInfo.fspath`*:
Alias for field number 0

*Property `SPLinkDataFileInfo.sitename`*:
Alias for field number 1

*Property `SPLinkDataFileInfo.unixtime`*:
Alias for field number 3

## Function `ts2001_unixtime(tzname=None)`

Convert an SP-Link seconds-since-2001-01-01-local-time offset
into a UNIX time.

# Release Log



*Release 20220606*:
Initial PyPI release.
