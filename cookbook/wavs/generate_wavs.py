import komoog.audio as audio
import komoog.komoot as komoot
import komoog.io as io
import komoog.gpx as gpx


import matplotlib.pyplot as pl
import numpy as np

from bfmplot import colors

from tabulate import tabulate

col = "#0E1116"
pl.rcParams['axes.facecolor'] = col
pl.rcParams['figure.facecolor'] = col
pl.rcParams['savefig.facecolor'] = col

tours = io.read_tours()

colors[0] = '#aaaaaa'

al = 0.1

phases = 5

names = set()

table = []

url = 'https://github.com/benmaier/komoog/raw/main/cookbook/wavs/'

header = ['name','profile','constant audio', 'profile audio']

for itour, tour in enumerate(tours[:5]):

    row = []
    if tour['name'] in names:
        continue

    short_name = tour['name'].split('-')[0]
    short_name = short_name.split('–')[0]
    short_name = short_name.split('from')[0]
    row.append(short_name)

    #print(itour, tour['name'])
    fig, ax = pl.subplots(1,1,figsize=(4,1.))
    names.add(tour['name'])
    dst, alt = gpx.convert_gpx_tracks_to_arrays(gpx.convert_tour_to_gpx_tracks(tour))
    x, y = audio.convert_distance_and_elevation_to_signal(dst, alt, max_elevation_difference=0)
    zero = np.zeros_like(y)
    ytop = y.copy()
    ytop[ytop<0] = 0
    ybtt = y.copy()
    ybtt[ybtt>0] = 0
    for phase in range(2,phases+1):
        scale0 = (phase-1)/phases
        scale1 = phase/phases

        #pl.fill_between(x,zero,ytop,alpha=al,color=colors[0],ec='None')
        #pl.fill_between(x,zero,ybtt,alpha=al,color=colors[0],ec='None')
        pl.fill_between(x,y*scale0,y*scale1,alpha=al*scale1,color=colors[0],ec='None')
        #pl.fill_between(x,zero,y,alpha=al,color=colors[0],ec='None')
    pl.plot(x,y,color=colors[0])
    pl.xlim(0,1)
    pl.ylim(-1.05,1.05)
    pl.axis('off')
    #ax.set_position([0, 0, 1, 1])

    fig.tight_layout()

    pl.subplots_adjust(left=0,right=1,top=1,bottom=0)

    imgpath = 'imgs/{0:02d}.png'.format(itour)

    fig.savefig(imgpath,dpi=72)


    row.append('!['+tour['name']+']('+url+imgpath+')')

    for set_tune_to_follow_tour_profile, approximate_length_in_seconds in zip([False, True],[2,4]):
        audiod, sampling_rate = audio.convert_tour_to_audio(tour,
                                    set_tune_to_follow_tour_profile=set_tune_to_follow_tour_profile,
                                    approximate_length_in_seconds=approximate_length_in_seconds,
                )
        ndx = np.argmin(np.abs(audiod))
        audiod = np.roll(audiod,-ndx)
        if set_tune_to_follow_tour_profile:
            add = 'profile'
        else:
            add = 'constant'
        wavpath = 'wavs/{0:02d}_{1}.wav'.format(itour,add)
        row.append(url+wavpath+'.mp4')
        io.write_wav(wavpath,audiod,sampling_rate)

    table.append(row)

print(tabulate(table,headers=header,tablefmt='github'))

pl.show()
