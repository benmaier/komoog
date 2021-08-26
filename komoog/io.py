# -*- coding: utf-8 -*-
"""
File I/O.
"""

import pathlib
from pathlib import Path
import simplejson as json
from komoog.paths import customdir
from scipy.io import wavfile

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

    wavfile.write(fn,sampling_rate,audio_data)


if __name__ == "__main__":
    get_credentials()
