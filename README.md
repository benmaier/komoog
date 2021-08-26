# komoog

[![CircleCI](https://circleci.com/gh/benmaier/komoog.svg?style=svg)](https://circleci.com/gh/benmaier/komoog)

Convert your komoot tours to audio signals.

* repository: https://github.com/benmaier/komoog/
* documentation: http://komoog.benmaier.org/

```python
from komoog.komoot import download_all_komoot_tours, choose_downloaded_komoot_tour
from komoog.audio import convert_tour_to_audio, play_audio

download_all_komoot_tours()
tour = choose_downloaded_komoot_tour()
audio, sampling_rate = convert_tour_to_audio(tour,
                                             approximate_length_in_seconds=4,
                                             set_tune_to_follow_tour_profile=True,
                                            )
play_audio(audio, sampling_rate)
```

## Install

    pip install komoog

`komoog` was developed and tested for 

* Python 3.6
* Python 3.7
* Python 3.8

So far, the package's functionality was tested on Mac OS X and CentOS only.

## Dependencies

`komoog` directly depends on the following packages which will be installed by `pip` during the installation process

* `numpy>=1.17`
* `scipy>=1.5.0`
* `gpxpy>=1.4.2`
* `simplejson>=3.17.2`
* `simpleaudio=>=1.0.4`

## Documentation

The full documentation is available at [komoog.benmaier.org](http://komoog.benmaier.org).

## Changelog

Changes are logged in a [separate file](https://github.com/benmaier/komoog/blob/main/CHANGELOG.md).

## License

This project is licensed under the [MIT License](https://github.com/benmaier/komoog/blob/main/LICENSE).
Note that this excludes any images/pictures/figures shown here or in the documentation.

## Contributing

If you want to contribute to this project, please make sure to read the [code of conduct](https://github.com/benmaier/komoog/blob/main/CODE_OF_CONDUCT.md) and the [contributing guidelines](https://github.com/benmaier/komoog/blob/main/CONTRIBUTING.md). In case you're wondering about what to contribute, we're always collecting ideas of what we want to implement next in the [outlook notes](https://github.com/benmaier/komoog/blob/main/OUTLOOK.md).

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v1.4%20adopted-ff69b4.svg)](code-of-conduct.md)

## Dev notes

Fork this repository, clone it, and install it in dev mode.

```bash
git clone git@github.com:YOURUSERNAME/komoog.git
make
```

If you want to upload to PyPI, first convert the new `README.md` to `README.rst`

```bash
make readme
```

It will give you warnings about bad `.rst`-syntax. Fix those errors in `README.rst`. Then wrap the whole thing 

```bash
make pypi
```

It will probably give you more warnings about `.rst`-syntax. Fix those until the warnings disappear. Then do

```bash
make upload
```
