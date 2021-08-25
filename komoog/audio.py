# -*- coding: utf-8 -*-
"""
Audio handling and conversion.
"""

import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter

_NOTES = {
            'C': -9,
            'C#': -8,
            'Db': -8,
            'D': -7,
            'D#': -6,
            'Eb': -6,
            'E' : -5,
            'F': -4,
            'F#': -3,
            'Gb': -3,
            'G': -2,
            'G#': -1,
            'Ab': -1,
            'A': 0,
            'A#': 1,
            'Bb': 1,
            'B': 2,
        }

_TUNE_A = 440 #Hz

def get_tune(tune):
    """
    Convert a tune value to a frequency.
    """

    if isinstance(tune,str):
        try:
            tune = _TUNE_A * 2.**(_NOTES[tune]/12.)
        except KeyError as e:
            raise ValueError("If `tune` is provided as a string, it has to be any of "+str(list(_NOTES.keys())))

    return tune


def convert_distance_and_elevation_to_signal(distance,
                                             elevation,
                                             max_elevation_difference=0,
                                             ):
    """
    Convert a distance/elevation profile to a signal, i.e. normalize distance
    to range [0,1] and y to range [-1,1].

    Parameters
    ==========
    distance : numpy.ndarray
        Contains the covered 2D distance in meters.
    elevation : numpy.ndarray
        Contains the corresponding elevation profile in meters
    max_elevation_difference : float, default = 0
        Used to control the level of the audio signal. If this
        value is ``<= 0``, the audio level will always be maximized.
        If given a positive value, this value will represent the maximum
        scale of the audio signal. If the elevation profile's elevation
        difference is larger than this value, the signal will simply be
        maximized. A good value is ``max_elevation_difference = 2000``.

    Returns
    =======
    x : numpy.ndarray
        covered distance in range [0,1]
    y : numpy.ndarray
        signal in range [-1,1]
    """

    # assert that data is sorted
    assert(np.all(np.diff(distance) >= 0))

    # assert that arrays have same length
    assert(len(distance) == len(elevation))

    mn = min(elevation)
    mx = max(elevation)
    elevation_diff = mx - mn

    maximize_signal = elevation_diff >= max_elevation_difference

    # position the signal such that the area under the curve is equal
    mean = np.trapz(elevation,distance) / distance[-1]

    if maximize_signal:
        y = (elevation - mn) / elevation_diff * 2. - 1.
    else:
        y = (elevation - mean) / max_elevation_difference * 2.

    x = distance / np.max(distance)

    return x, y

def convert_distance_and_elevation_to_audio(distance,
                                            elevation,
                                            max_elevation_difference=0,
                                            tune='C',
                                            sampling_rate=44100,
                                            approximate_length_in_seconds=1,
                                            ):
    """
    Convert a distance/elevation profile to an audio signal.

    Parameters
    ==========
    distance : numpy.ndarray
        Contains the covered 2D distance in meters.
    elevation : numpy.ndarray
        Contains the corresponding elevation profile in meters
    max_elevation_difference : float, default = 0
        Used to control the level of the audio signal. If this
        value is ``<= 0``, the audio level will always be maximized.
        If given a positive value, this value will represent the maximum
        scale of the audio signal. If the elevation profile's elevation
        difference is larger than this value, the signal will simply be
        maximized. A good value is ``max_elevation_difference = 2000``.
    tune : str or float
        Desired frequency of the sound. Can be any of

        .. code:: python

            [ 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#',
              'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B' ]

        where ``'A'`` corresponds to 440Hz.

        Can also be a frequency in Hz.
    sampling_rate : int, default = 44100
        Sampling rate in Hz
    approximate_length_in_seconds : float, default = 1.
        The desired length of the audio signal in seconds
        If equal to zero, will return a single loop.

    Returns
    =======
    audio : numpy.ndarray of numpy.int16
        The transformed audio signal
    sampling_rate : int
        The sampling rate of the audio signal.
    """

    x, y = convert_distance_and_elevation_to_signal(distance,
                                                    elevation,
                                                    max_elevation_difference=max_elevation_difference,
                                                    )

    return convert_signal_to_audio(x,
                                   y,
                                   tune=tune,
                                   sampling_rate=sampling_rate,
                                   approximate_length_in_seconds=approximate_length_in_seconds,
                                  )

def convert_signal_to_audio(x,
                            y,
                            tune='C',
                            sampling_rate=44100,
                            approximate_length_in_seconds=1,
                            ):
    """
    Convert a normalized distance/elevation signal to an audio signal.

    Parameters
    ==========
    distance : numpy.ndarray
        Contains the covered 2D distance in meters.
    elevation : numpy.ndarray
        Contains the corresponding elevation profile in meters
    tune : str or float
        Desired frequency of the sound. Can be any of

        .. code:: python

            [ 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#',
              'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B' ]

        where ``'A'`` corresponds to 440Hz.

        Can also be a frequency in Hz.
    sampling_rate : int, default = 44100
        Sampling rate in Hz
    approximate_length_in_seconds : float, default = 1.
        The desired length of the audio signal in seconds
        If equal to zero, will return a single loop.

    Returns
    =======
    audio : numpy.ndarray of numpy.int16
        The transformed audio signal
    sampling_rate : int
        The sampling rate of the audio signal.
    """

    tune = get_tune(tune)

    x_sample = np.linspace(0,1,len(x)*2+1)
    f = interp1d(x, y, kind='linear')
    y_sample = f(x_sample)

    if len(y_sample) > 400:
        window_length = 101
    else:
        window_length = int(len(y_sample) * 0.1)
        if window_length % 2 == 0:
            window_length += 1

    y_filtered = savgol_filter(y_sample, window_length, 2, mode='wrap')

    sampling_t = np.linspace(0,1/tune,int(sampling_rate/tune))

    f = interp1d(x_sample/tune, y_filtered, kind='cubic')
    y = f(sampling_t)

    ymax = np.max(np.abs(y))
    ymax = np.max([1.,ymax])

    # convert to 16-bit data
    audio = y * 32767 / ymax
    raw_audio = audio.astype(np.int16)

    if approximate_length_in_seconds > 0:
        necessary_samples = sampling_rate * approximate_length_in_seconds
        copies = int(np.ceil(necessary_samples/len(raw_audio)))
        audio = np.concatenate([raw_audio]*copies)
    else:
        audio = raw_audio

    return audio, sampling_rate


def convert_distance_and_elevation_to_profile_audio(
                                            distance,
                                            elevation,
                                            max_elevation_difference=0,
                                            tune='C',
                                            sampling_rate=44100,
                                            approximate_length_in_seconds=1,
                                            ):
    """
    Convert a distance/elevation profile to an audio signal that
    mimicks the elevation profile.

    Parameters
    ==========
    distance : numpy.ndarray
        Contains the covered 2D distance in meters.
    elevation : numpy.ndarray
        Contains the corresponding elevation profile in meters
    max_elevation_difference : float, default = 0
        Used to control the level of the audio signal. If this
        value is ``<= 0``, the audio level will always be maximized.
        If given a positive value, this value will represent the maximum
        scale of the audio signal. If the elevation profile's elevation
        difference is larger than this value, the signal will simply be
        maximized. A good value is ``max_elevation_difference = 2000``.
    tune : str or float
        Desired frequency of the sound. Can be any of

        .. code:: python

            [ 'C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#',
              'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B' ]

        where ``'A'`` corresponds to 440Hz.

        Can also be a frequency in Hz.
    sampling_rate : int, default = 44100
        Sampling rate in Hz
    approximate_length_in_seconds : float, default = 1.
        The desired length of the audio signal in seconds
        If equal to zero, will return a single loop.

    Returns
    =======
    audio : numpy.ndarray of numpy.int16
        The transformed audio signal
    sampling_rate : int
        The sampling rate of the audio signal.
    """

    x, y = convert_distance_and_elevation_to_signal(distance,
                                                    elevation,
                                                    max_elevation_difference=max_elevation_difference,
                                                   )

    frequency_scalar = 2**y

    # get length of audio signal
    single_audio, _ = convert_signal_to_audio(
                                   x,
                                   y,
                                   tune=tune,
                                   sampling_rate=sampling_rate,
                                   approximate_length_in_seconds=0,
                                  )

    full_audio, _ = convert_signal_to_audio(
                                   x,
                                   y,
                                   tune=tune,
                                   sampling_rate=sampling_rate,
                                   approximate_length_in_seconds=approximate_length_in_seconds,
                                  )

    copies = int(np.ceil(len(full_audio)/len(single_audio)))
    new_x = x * copies
    f = interp1d(new_x,frequency_scalar,kind='cubic')


    tune = get_tune(tune)

    audios = []
    for copy in range(copies):
        this_audio, _ = convert_signal_to_audio(
                                   x,
                                   y,
                                   tune=tune*f(copy),
                                   sampling_rate=sampling_rate,
                                   approximate_length_in_seconds=0,
                                  )
        audios.append(this_audio)

    return np.concatenate(audios).astype(np.int16), sampling_rate

if __name__=="__main__":

    from komoog.gpx import convert_gpx_tracks_to_arrays
    import gpxpy
    import simpleaudio as sa
    import matplotlib.pyplot as pl

    from scipy.io import wavfile

    fn = '/Users/bfmaier/Downloads/Tour.gpx'
    fn = '/Users/bfmaier/Downloads/Tour-2.gpx'
    fn = '/Users/bfmaier/Downloads/Tour-3.gpx'
    fn = '/Users/bfmaier/Downloads/Tour-4.gpx'
    fn = '/Users/bfmaier/Downloads/Tour-5.gpx'

    with open(fn,'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    print(gpx.name)

    distance, elevation = convert_gpx_tracks_to_arrays(gpx.tracks)

    sampling_rate = 44100

    x, y = convert_distance_and_elevation_to_signal(distance, elevation,max_elevation_difference=200)
    y, _ = convert_distance_and_elevation_to_audio(distance, elevation, max_elevation_difference=2000,sampling_rate=sampling_rate)

    x = np.arange(len(y)) / sampling_rate


    # start playback

    # wait for playback to finish before exiting

    #wavfile.write('./tour.wav',sampling_rate,y)

    play_obj = sa.play_buffer(y, 1, 2,sampling_rate)
    play_obj.wait_done()

    pl.plot(x, y)
    pl.show()
    y2, _ = convert_distance_and_elevation_to_profile_audio(distance, elevation, max_elevation_difference=2000,approximate_length_in_seconds=10)
    play_obj = sa.play_buffer(y2, 1, 2,sampling_rate)
    play_obj.wait_done()





    #pl.plot(x, y)
    #pl.ylim(-1,1)
    pl.show()
