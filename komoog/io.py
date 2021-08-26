# -*- coding: utf-8 -*-
"""
File I/O.
"""

import pathlib
from pathlib import Path
import simplejson as json
from komoog.paths import customdir
from scipy.io import wavfile
import gpxpy

tour_file = customdir / "tours.json"

def read_tours():
    """Read downloaded tours from ``~/.komoog/tours.json``"""

    if not tour_file.exists():
        raise FileNotFoundError("Couldn't find any downloaded tours. Please call komoog.komoot.download_all_komoot_tours() first.")

    with open(tour_file,'r') as f:
        tours = json.load(f)

    return tours

def write_tours(tours):
    """Write downloaded tours to ``~/.komoog/tours.json``"""

    with open(tour_file,'w') as f:
        json.dump(tours,f)


def write_wav(fn,audio_data,sampling_rate):
    """
    Write audio data to a wav file.
    """

    wavfile.write(fn,sampling_rate,audio_data)

def read_gpx(fn):
    """
    Read a gpx file. Returns a `gpxpy.GPX` object.
    Pass to :func:`komoog.gpx.convert_gpx_tracks_to_arrays`
    as

    .. code:: python

        gpx = read_gpx('Tour.gpx')
        convert_gpx_tracks_to_arrays(gpx.tracks)

    to retrieve distance and elevation profile.
    """

    with open(fn,'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    return gpx


if __name__ == "__main__":
    get_credentials()
