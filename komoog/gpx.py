# -*- coding: utf-8 -*-
"""
GPX file handling.
"""

import numpy as np
import gpxpy

def convert_gpx_tracks_to_arrays(gpx_tracks):
    """
    Take a list of gpx Track objects and convert them
    to two arrays, one containing the two-dimensional distance
    covered on the globe, the second containing the elevation.

    Parameters
    ==========
    gpx_tracks : list of gpx.Track
        list of tracks to convert

    Returns
    =======
    distance : numpy.ndarray
        Contains the covered 2D distance in meters.
    elevation : numpy.ndarray
        Contains the corresponding elevation profile in meters
    """

    all_points = []

    for track in gpx_tracks:
        for segment in track.segments:
            these_points = []
            for point in segment.points:
                these_points.append(point)
            all_points.append(these_points)

    distance = []
    elevation = []

    for points in all_points:

        this_distance = [0.]
        this_elevation = [points[0].elevation]

        for A, B in zip(points[:-1], points[1:]):
            d = A.distance_2d(B)
            this_distance.append(d+this_distance[-1])
            this_elevation.append(B.elevation)

        this_distance = np.array(this_distance)
        this_elevation = np.array(this_elevation)

        if len(distance) > 0:
            d = np.array(distance[-1])
            offset = d[-1] + np.mean(d[1:]-d[:-1])
        else:
            offset = 0.

        distance.append(this_distance + offset)
        elevation.append(this_elevation)


    if len(distance) > 1:
        distance = np.concatenate(distance)
        elevation = np.concatenate(elevation)
    else:
        distance = distance[0]
        elevation = elevation[0]

    return distance, elevation

def convert_tour_to_gpx_tracks(tour):

    seg = gpxpy.gpx.GPXTrackSegment()

    for point in tour['coordinates']
        seg.points.append(gpxpy.gpx.GPXTrackPoint(point['lat'], point['lng'], elevation=point['alt']))

    gpx_track = gpxpy.gpx.GPXTrack()
    gpx_track.segments.append(seg)

    return [gpx_track]

if __name__=="__main__":

    with open('/Users/bfmaier/Downloads/Tour.gpx','r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    distance, elevation = convert_gpx_track_to_arrays(gpx.tracks)

    import matplotlib.pyplot as pl

    pl.plot(distance, elevation)
    pl.show()
