# NTPmon

Copyright (c) 2015-2023 Paul D. Gear <https://libertysys.com.au/>

## License

GPLv3 - see COPYING.txt for details


## Introduction

NTPmon is a program which is designed to report on essential health metrics for
NTP.  It provides a Nagios check which can be used with many alerting systems,
including support for Nagios performance data.  NTPmon can also run as a daemon
for sending metrics to collectd or telegraf.  It supports both `ntpd` and
`chronyd`.


## Prerequisites

NTPmon is written in python, and requires python 3.3 or later.  It uses modules
from the standard python library, and also requires the `psutil` library, which
is available from pypi or your operating system repositories. NTPmon also
requires `ntpq` and `ntptrace` from the NTP distribution (or `chronyc` if you're
using chrony instead).

On Ubuntu (and probably other Debian-based Linux distributions), you can install
all the prerequisites by running:

    sudo apt-get install ntp python3-psutil

## Usage

To start running NTPmon, run:

    cd /opt
    git clone https://github.com/paulgear/ntpmon
    cd ntpmon
    ./src/ntpmon.py --help


## Metrics

NTPmon alerts on the following metrics of the local NTP server:

#### sync

Does NTP have a sync peer?  If not, return CRITICAL, otherwise return OK.

#### peers

Are there more than the minimum number of peers active?  The NTP algorithms
require a minimum of 3 peers for accurate clock management; to allow for failure
or maintenance of one peer at all times, NTPmon returns OK for 4 or more
configured peers, CRITICAL for 1 or 0, and WARNING for 2-3.

#### reach

Are the configured peers reliably reachable on the network?  Return CRITICAL for
less than 50% total reachability of all configured peers; return OK for greater
than 75% total reachability of all configured peers.

#### offset

Is the clock offset from its sync peer (or other peers, if the sync peer
is not available) acceptable?  Return CRITICAL for 50 milliseconds or more
average difference, WARNING for 10 ms or more average difference, and OK
for anything less.

#### traceloop

Is there a sync loop between the local server and the stratum 1 servers?
If so, return CRITICAL.  Most public NTP servers do not support tracing,
so for anything other than a loop (including a timeout), return OK.
Traceloop is disabled by default and may be deprecated in a future
release, since it produces additional NTP traffic which is not useful in
most cases.

### System metrics

In addition, NTPmon retrieves the following metrics directly from the local NTP
server (using `ntpq -nc readvar`):

- offset (as `sysoffset`, to distinguish it from `offset`)
- sys_jitter (as `sysjitter`, for grouping with `sysoffset`)
- frequency
- stratum
- rootdelay
- rootdisp

See the [NTP documentation](http://doc.ntp.org/current-stable/ntpq.html#system)
for the meaning of these metrics.

## Changes from previous version

NTPmon has been rewritten from version 1.0.0 of check_ntpmon.  Changes from
the original check_ntpmon are:

- Requires python 3.

- Removed dependency on GNU coreutils.

- Added support for detecting ntptrace loops.

- Added support for Nagios performance data:
  https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/3/en/perfdata.html

- Added collectd daemon.

- Added telegraf daemon.

- Removed support for changing thresholds; if the one person on the Internet
  who actually uses this really wants it, I might add it back. :-)


## Startup delay

By default, until ntpd has been running for 512 seconds (the minimum time for
8 polls at 64-second intervals), check_ntpmon will return OK (zero return code).
This is to prevent false positives on startup or for short-lived VMs.  To
ignore this safety precaution, use --run-time with a low number (e.g. 1 sec).


## To do

- Better/more documentation.
- Better/more unit tests.
- Create installer.
