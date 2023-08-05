#!/usr/bin/env python
#
# fmrib.py - Custom loaders for FMRIB-speciifc files.
#
# Author: Paul McCarthy <pauldmccarthy@gmail.com>
#
"""This module contains custom loaders for data files used in FMRIB,
which contain data on imaged subjects.
"""


import functools as ft
import datetime  as dt

import pandas    as pd
import numpy     as np

import                      funpack
import funpack.datatable as datatable


@funpack.sniffer('FMRIBImaging')
@ft.lru_cache()
def columns_FMRIBImaging(infile):
    """Return a list of columns describing the contents of the
    ``FMRIB_internal_info.txt`` file.
    """

    names = ['eid',
             'acq_time',
             'acq_phase',
             'processing_phase',
             'flipped_SWI']

    return [funpack.Column(infile,
                           n,
                           i,
                           200000 + i,
                           0,
                           0) for i, n in enumerate(names)]


@funpack.loader('FMRIBImaging')
def load_FMRIBImaging(infile):
    """Load a file with the same format as the ``FMRIB_internal_info.txt``
    file.
    """

    def parse_acq_date(date):
        year  = int(date[ :4])
        month = int(date[4:6])
        day   = int(date[6:8])
        return dt.date(year, month, day)

    def parse_acq_time(time):
        hour       = int(time[ :2])
        minute     = int(time[2:4])
        second     = int(time[4:6])
        micro      = int(time[7:])
        return dt.time(hour, minute, second, micro,
                       dt.timezone(dt.timedelta(0)))

    def combine_datetime(date, time):
        date = date.to_pydatetime().date()
        time = time.to_pydatetime().timetz()
        return dt.datetime.combine(date, time)

    names = ['eid',
             'acq_date',
             'acq_time',
             'acq_phase',
             'processing_phase',
             'flipped_SWI']

    converters = {'acq_date' : parse_acq_date,
                  'acq_time' : parse_acq_time}

    df = pd.read_csv(infile,
                     header=None,
                     names=names,
                     index_col=0,
                     parse_dates=['acq_time', 'acq_date'],
                     converters=converters,
                     delim_whitespace=True)

    df['acq_time'] = df['acq_date'].combine(df['acq_time'], combine_datetime)
    df.drop('acq_date', axis=1, inplace=True)

    return df


@funpack.cleaner()
def normalisedDate(dtable : datatable.DataTable,
                   vid    : int):
    """Converts date values into a numeric fractional year representation.

    Converts a date into a single value x, where ``floor(x)`` is the calendar
    year and the ``x mod 1`` is the fractional day within the year. The
    conversion takes leap years into account.
    """

    for col in dtable.columns(vid):
        series    = dtable[:, col.name]
        datetimes = series.to_numpy()
        years     = datetimes.astype('datetime64[Y]')
        days      = datetimes.astype('datetime64[D]')

        # convert to day of year
        # calculate fraction of day
        days  = (days  - years).astype(np.float32)
        years = (years + 1970) .astype(np.float32)
        leaps = pd.DatetimeIndex(datetimes).is_leap_year + 365

        # make sure NaTs are preserved
        na        = series.isna()
        dates     = years + (days / leaps)
        dates[na] = np.nan

        # calculate fraction of year
        dtable[:, col.name] = dates


@funpack.cleaner()
def normalisedAcquisitionTime(dtable : datatable.DataTable,
                              vid    : int):
    """Converts timestamps into a numeric fractional year representation.

    Converts a date or date+time into a single value x, where `floor(x)` is the
    calendar year and the fraction day/time within the year *except* 'a day' is
    redefined as the time between 7am and 8pm (UK BioBank scanning only takes
    place within these hours).
    """
    for col in dtable.columns(vid):
        series    = dtable[:, col.name]
        datetimes = series.to_numpy()
        years     = datetimes.astype('datetime64[Y]')
        days      = datetimes.astype('datetime64[D]')
        hours     = datetimes.astype('datetime64[h]')
        mins      = datetimes.astype('datetime64[m]')
        secs      = datetimes.astype('datetime64[s]')

        # convert to day of year, hour
        # of day, second of hour, then
        # calculate fraction of day
        secs      = (secs  - mins) .astype(np.float32)
        mins      = (mins  - hours).astype(np.float32)
        hours     = (hours - days) .astype(np.float32)
        days      = (days  - years).astype(np.float32)
        years     = (years + 1970) .astype(np.float32)
        dayfracs  = ((hours - 7) + (mins / 60) + (secs / 3600)) / 13
        leaps     = pd.DatetimeIndex(datetimes).is_leap_year + 365

        # make sure NaTs are preserved
        na        = series.isna()
        times     = years + (days + dayfracs) / leaps
        times[na] = np.nan

        # calculate and return fraction of year
        dtable[:, col.name] = times
