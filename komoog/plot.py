# -*- coding: utf-8 -*-
"""
Plotting signals.
"""

import matplotlib.pyplot as pl
import komoog.audio as audio
import komoog.gpx as gpx

def plot_tour(tour,gradientphases=5,alpha=0.2,figsize=(4,1),max_elevation_difference=0):
    """
    Plot a tour as a signal

    Parameters
    ==========
    tour : dict
        A downloaded tour
    gradientphases : int, default = 5
        How many shades the signal shadow will show
    alpha : float, default = 0.1
        Transparency of shade
    figsize : tuple of float, default = (4,1)
        figure size
    max_elevation_difference : float, default = 0
        for signal normlization

    Returns
    =======
    ax : matplotlib.Axes
        The axis on which the signal was plotted
    """

    dst, alt = gpx.convert_gpx_tracks_to_arrays(gpx.convert_tour_to_gpx_tracks(tour))
    x, y = audio.convert_distance_and_elevation_to_signal(dst, alt, max_elevation_difference=max_elevation_difference)

    return plot_signal(x,y,
                       gradientphases=gradientphases,
                       alpha=alpha,
                       figsize=figsize,
                       )

def plot_signal(x,y,gradientphases=5,alpha=0.2,figsize=(4,1)):
    """
    Plot a signal

    Parameters
    ==========
    x : numpy.ndarray
        signal x-values in range [0,1]
    y : numpy.ndarray
        signal y-values in range [-1,1]
    gradientphases : int, default = 5
        How many shades the signal shadow will show
    alpha : float, default = 0.1
        Transparency of shade
    figsize : tuple of float, default = (4,1)
        figure size

    Returns
    =======
    ax : matplotlib.Axes
        The axis on which the signal was plotted
    """

    bgcol = "#0E1116"
    col = '#aaaaaa'
    phases = gradientphases
    al = alpha

    axface = pl.rcParams['axes.facecolor']
    figface = pl.rcParams['figure.facecolor']
    savface = pl.rcParams['savefig.facecolor']

    pl.rcParams['axes.facecolor'] = bgcol
    pl.rcParams['figure.facecolor'] = bgcol
    pl.rcParams['savefig.facecolor'] = bgcol

    fig, ax = pl.subplots(1,1,figsize=figsize)

    for phase in range(2,phases+1):
        scale0 = (phase-1)/phases
        scale1 = phase/phases
        pl.fill_between(x,y*scale0,y*scale1,alpha=al*scale1,color=col,ec='None')

    pl.plot(x,y,color=col,lw=1.5)
    pl.xlim(0,1)
    pl.ylim(-1.05,1.05)
    pl.axis('off')
    #ax.set_position([0, 0, 1, 1])

    fig.tight_layout()

    pl.subplots_adjust(left=0,right=1,top=1,bottom=0)

    pl.rcParams['axes.facecolor'] = axface
    pl.rcParams['figure.facecolor'] = figface
    pl.rcParams['savefig.facecolor'] = savface

    return ax

if __name__=="__main__":
    import komoog.io as io

    tours = io.read_tours()

    plot_tour(tours[0])
    pl.show()
