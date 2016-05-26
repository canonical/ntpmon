#!/usr/bin/env python3
#
# Copyright:    (c) 2016 Paul D. Gear
# License:      GPLv3 <http://www.gnu.org/licenses/gpl.html>
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
#


def _add_alias(metrics, name, alias):
    """
    Add an alias for a single named metric
    """
    if name in metrics:
        metrics[alias] = metrics[name]
        return True
    else:
        return False


def _find_alias(metrics, alias, names):
    """
    If a single name is given, find the named metric and add its alias to the hash.
    If names is a list, find the first matching one and add its alias to the hash.
    """
    if names is None:
        names = alias
    if isinstance(names, str):
        # it's a single string; add it
        _add_alias(metrics, names, alias)
    else:
        # it's a list; try each one in order
        for n in names:
            if _add_alias(metrics, n, alias):
                return


def addaliases(metrics, aliases):
    """
    Add all defined aliases to metrics
    """
    for a in aliases:
        _find_alias(metrics, a, aliases[a])


def filter(metrics, names):
    """
    Return a new hash containing only the metrics in the list of names.
    This could just be a lambda.
    """
    filtered = {}
    for n in names:
        if n in metrics:
            filtered[n] = metrics[n]
    return filtered
