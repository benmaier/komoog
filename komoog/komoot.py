# -*- coding: utf-8 -*-
"""
Obtaining tours and tour data from komoot.
Adapted from https://github.com/js-on/medium_komoot.
"""


import requests
import json
from komoog.paths import get_credentials, customdir
from komoog.io import write_tours, read_tours

import simplejson as json

def get_tours_and_session():
    """
    Returns a list of the user's tours on komoot and
    a ``requests.Session`` object.
    """

    cred = get_credentials()
    email = cred['email']
    password = cred['password']
    client_id = cred['clientid']
    login_url = "https://account.komoot.com/v1/signin"
    tour_url = f"https://www.komoot.de/user/{client_id}/tours"

    session = requests.Session()

    res = requests.get(login_url)
    cookies = res.cookies.get_dict()

    headers = {
        "Content-Type": "application/json"
    }

    payload = json.dumps({
        "email": email,
        "password": password,
        "reason": "null"
    })

    session.post(login_url,
           headers=headers,
           data=payload,
           cookies=cookies,
           )

    url = "https://account.komoot.com/actions/transfer?type=signin"
    session.get(url)

    headers = {"onlyprops": "true"}

    response = session.get(tour_url, headers=headers)
    if response.status_code != 200:
        print("Something went wrong in the request...")
        print(response.text)
        exit(1)

    data = response.json()

    tours = data["user"]["_embedded"]["tours"]["_embedded"]["items"]

    return tours, session

def get_tour(tours,tour_id,session):
    """
    Returns a tour including coordinates given a
    `tour_id` (position of the tour in `tours`).
    """

    tour = tours[tour_id]
    tour_url = tour["_links"]["coordinates"]["href"]
    headers = {"onlyprops": "true"}
    response = session.get(tour_url, headers=headers)
    tour_data = json.loads(response.text)

    tour['coordinates'] = tour_data['items']

    return tour

def download_all_komoot_tours():
    """
    Login with user credentials, download tour information
    and all tours. Tours will be saved in a custom directory.
    Tours can be passed to :func:`komoog.gpx.convert_tour_to_gpx_tracks`
    afterwards.
    """

    tours, session = get_tours_and_session()

    tours = [ get_tour(tours, i, session) for i in range(len(tours)) ]

    write_tours(tours)

    return tours


def choose_komoot_tour_live():
    """
    Login with user credentials, download tour information,
    choose a tour, and download it. Can be passed to
    :func:`komoog.gpx.convert_tour_to_gpx_tracks`
    afterwards.
    """

    tours, session = get_tours_and_session()

    for idx in range(len(tours)):
        print(f"({idx+1}) {tours[idx]['name']}")

    tour_id = int(input("Tour ID: "))
    tour_id -= 1

    tour = get_tour(tours,tour_id,session)

    return tour

def choose_downloaded_komoot_tour():
    """
    Choose a previously downloaded tour. Tour can be passed to
    :func:`komoog.gpx.convert_tour_to_gpx_tracks`
    afterwards.
    """

    tours = read_tours()

    for idx in range(len(tours)):
        print(f"({idx+1}) {tours[idx]['name']}")

    tour_id = int(input("Tour ID: "))
    tour_id -= 1

    return tours[tour_id]


if __name__=="__main__":

    #choose_komoot_tour_live()
    download_all_komoot_tours()
    tour = choose_downloaded_komoot_tour()

