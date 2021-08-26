About
=====

Convert your `komoot <komoot.com>`__ hiking/cycling trips to audio
signals.

-  repository: https://github.com/benmaier/komoog/
-  documentation: http://komoog.readthedocs.io/

.. code:: python

   from komoog.komoot import download_all_komoot_tours, choose_downloaded_komoot_tour
   from komoog.audio import convert_tour_to_audio, play_audio

   download_all_komoot_tours()
   tour = choose_downloaded_komoot_tour()
   audio, sampling_rate = convert_tour_to_audio(tour,
                                                approximate_length_in_seconds=4,
                                                set_tune_to_follow_tour_profile=True,
                                               )
   play_audio(audio, sampling_rate)

After hiking I noticed that komoot comes with elevation profiles of tour
hiking trips:

.. image:: https://github.com/benmaier/komoog/blob/main/img/tour_profile.png
   :alt: Tour profile

This reminded me of wave tables I know from sound synthesis. Because I'm
always looking for sounds to use when making music, I decided to write
code that generates sounds from hiking profiles that can be used in
sound synthesis.

Note that I adapted code from
`js-on/medium_komoot <https://github.com/js-on/medium_komoot>`__ to
access trips on komoot.

Install
-------

.. code:: bash

   pip install komoog

``komoog`` was developed and tested for

-  Python 3.6
-  Python 3.7
-  Python 3.8

So far, the package's functionality was tested on macOS only.

Prerequisites
-------------

Save your komoot credentials in ``~/.komoog/komoot.json`` as

.. code:: json

   {
       "email" : "your@email.com",
       "password" : "yourpassword",
       "clientid" : "yourclientid"
   }

You can find your client id in the komoot url when you log in. Click on
your username, then on "Planned Tours" or "Completed Tours". The URL
will change to something like

.. code:: bash

   https://www.komoot.com/user/1851102841208/tours?type=planned

Here, ``1851102841208`` is your ``clientid``.

Dependencies
------------

``komoog`` directly depends on the following packages which will be
installed by ``pip`` during the installation process

-  ``numpy>=1.17``
-  ``scipy>=1.5.0``
-  ``gpxpy>=1.4.2``
-  ``simplejson>=3.17.2``
-  ``simpleaudio=>=1.0.4``

Documentation
-------------

The full documentation is available at
`komoog.readthedocs.io <http://komoog.readthedocs.io>`__.

Changelog
---------

Changes are logged in a `separate
file <https://github.com/benmaier/komoog/blob/main/CHANGELOG.md>`__.

License
-------

This project is licensed under the `MIT
License <https://github.com/benmaier/komoog/blob/main/LICENSE>`__. Note
that this excludes any images/pictures/figures shown here or in the
documentation.

Contributing
------------

If you want to contribute to this project, please make sure to read the
`code of
conduct <https://github.com/benmaier/komoog/blob/main/CODE_OF_CONDUCT.md>`__
and the `contributing
guidelines <https://github.com/benmaier/komoog/blob/main/CONTRIBUTING.md>`__.
In case you're wondering about what to contribute, we're always
collecting ideas of what we want to implement next in the `outlook
notes <https://github.com/benmaier/komoog/blob/main/OUTLOOK.md>`__.

|Contributor Covenant|

Dev notes
---------

Fork this repository, clone it, and install it in dev mode.

.. code:: bash

   git clone git@github.com:YOURUSERNAME/komoog.git
   make

If you want to upload to PyPI, first convert the new ``README.md`` to
``README.rst``

.. code:: bash

   make readme

It will give you warnings about bad ``.rst``-syntax. Fix those errors in
``README.rst``. Then wrap the whole thing

.. code:: bash

   make pypi

It will probably give you more warnings about ``.rst``-syntax. Fix those
until the warnings disappear. Then do

.. code:: bash

   make upload

.. |Contributor Covenant| image:: https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg
   :target: code-of-conduct.md
