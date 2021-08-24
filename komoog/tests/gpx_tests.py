import unittest

import numpy as np

from komoog.gpx import convert_gpx_tracks_to_arrays

import gpxpy

gpx_segment = gpxpy.gpx.GPXTrackSegment()

class GPXTest(unittest.TestCase):

    def test_conversion(self):

        segA = gpxpy.gpx.GPXTrackSegment()
        segB = gpxpy.gpx.GPXTrackSegment()

        segA.points.append(gpxpy.gpx.GPXTrackPoint(2.1234, 5.1234, elevation=1234))
        segA.points.append(gpxpy.gpx.GPXTrackPoint(2.1235, 5.1235, elevation=1235))

        segB.points.append(gpxpy.gpx.GPXTrackPoint(5.1234, 2.1234, elevation=1234))
        segB.points.append(gpxpy.gpx.GPXTrackPoint(5.1235, 2.1235, elevation=1235))

        gpx_track = gpxpy.gpx.GPXTrack()

        gpx_track.segments.append(segA)
        gpx_track.segments.append(segB)

        x = [0., 15.737549302052873, 15.737549302052873*2, 15.737549302052873*2 + 15.711535749181415]
        y = [1234., 1235., 1234., 1235.]

        dist, elev = convert_gpx_tracks_to_arrays([gpx_track])

        for a, b in zip(x, dist):
            assert(np.isclose(a, b))

        for a, b in zip(y, elev):
            assert(np.isclose(a, b))



if __name__ == "__main__":

    T = GPXTest()
    T.test_conversion()
