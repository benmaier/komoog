# -*- coding: utf-8 -*-
"""
Audio handling.
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

def _convert_distance_and_elevation_to_signal(distance,
                                              elevation,
                                              maximize_signal=True,
                                              max_elevation_diff=2000,
                                              ):
    # assert that data is sorted
    assert(np.all(np.diff(distance) >= 0))

    # assert that arrays have same length
    assert(len(distance) == len(elevation))

    mn = min(elevation)
    mx = max(elevation)
    elevation_diff = mx - mn

    if elevation_diff >= max_elevation_diff:
        maximize_signal = True

    mean = np.trapz(elevation,distance) / distance[-1]

    print(np.diff(distance))

    if maximize_signal:
        y = (elevation - mn) / elevation_diff * 2. - 1.
    else:
        y = (elevation - mean) / max_elevation_diff * 2.

    x = distance / np.max(distance)

    return x, y

def convert_distance_and_elevation_to_audio(distance,
                                            elevation,
                                            maximize_signal=True,
                                            max_elevation_diff=2000,
                                            tune=440,
                                            bitrate=44100):

    x, y = _convert_distance_and_elevation_to_signal(distance, elevation)

    dx = np.mean(np.diff(x))
    x = np.concatenate((
                        x - x[-1] - dx,
                        x,
                        x + x[-1] + dx,
                       ))

    y = np.concatenate((y,y,y))

    x /= tune

    sampling_t = np.linspace(0,1/tune,int(bitrate/tune))
    print(sampling_t)

    f = interp1d(x, y, kind='cubic')
    y = f(sampling_t)
    x = sampling_t
    audio = y * 32767
    # convert to 16-bit data
    audio = audio.astype(np.int16)

    savgol_filter

    return x, audio


if __name__=="__main__":

    from komoog.gpx import convert_gpx_tracks_to_arrays
    import gpxpy
    import simpleaudio as sa
    import matplotlib.pyplot as pl

    with open('/Users/bfmaier/Downloads/Tour.gpx','r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    distance, elevation = convert_gpx_tracks_to_arrays(gpx.tracks)

    bitrate = 44100

    x, y = _convert_distance_and_elevation_to_signal(distance, elevation, maximize_signal=False,max_elevation_diff=200)
    x, y = convert_distance_and_elevation_to_audio(distance, elevation, maximize_signal=False,max_elevation_diff=200,bitrate=bitrate,tune=220)

    pl.plot(x, y)
    #pl.ylim(-1,1)
    pl.show()

    y = np.array(y.tolist()*tune)
    # start playback
    play_obj = sa.play_buffer(y, 1, 2,bitrate)

    # wait for playback to finish before exiting
    play_obj.wait_done()





    pl.plot(x, y)
    pl.ylim(-1,1)
    pl.show()
