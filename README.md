# komoog


Convert your [komoot](komoot.com) hiking/cycling trips to audio signals.

* repository: https://github.com/benmaier/komoog/
* documentation: http://komoog.readthedocs.io/

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

After hiking I noticed that komoot comes with elevation profiles of tour hiking
trips:

![Tour profile](https://github.com/benmaier/komoog/raw/main/img/tour_profile.png)

This reminded me of wave tables I know from sound synthesis. Because I'm always
looking for sounds to use when making music, I decided to write code that
generates sounds from hiking profiles that can be used in sound synthesis.

Note that I adapted code from
[js-on/medium\_komoot](https://github.com/js-on/medium_komoot)
to access trips on komoot.

## Examples

### Colorado Provencale in Rustrel – La Doa Loop from Rustrel


https://user-images.githubusercontent.com/10728380/131221697-8f5ff1b5-5fae-47a4-b36b-ad8c39992718.mp4


https://user-images.githubusercontent.com/10728380/131221699-a9dd5741-3ae5-4d16-ad44-9ce8642bbecb.mp4

### Lookout – L´Aiguebrun Loop from Buoux



https://user-images.githubusercontent.com/10728380/131221700-085da556-614a-4b9d-8f7d-c88e0d9f172c.mp4



https://user-images.githubusercontent.com/10728380/131221701-85fcb6ed-eadc-453b-a32c-98c5008c945b.mp4

### Gorges de Régalon – Vue de la Gorge Loop from Quartier Gardet




https://user-images.githubusercontent.com/10728380/131221702-36af7891-9089-45a8-8b7f-262bf29d4383.mp4



https://user-images.githubusercontent.com/10728380/131221704-131734e1-d82c-4fe3-a6d4-749c69fdd34e.mp4

### Forêt des Cèdres - Vue au sud – Belvédère Loop from Lacoste




https://user-images.githubusercontent.com/10728380/131221705-95615790-45c3-4266-9f46-8c287c6cb167.mp4



https://user-images.githubusercontent.com/10728380/131221707-3add51cb-ad1e-49a0-9801-9f69086f5f62.mp4

### Crête du Grand luberon – Le Mourre Nègre (1125m) Loop from Rue de l'Église



https://user-images.githubusercontent.com/10728380/131221708-f209abdd-3a57-4bca-b0ae-c726e25064c5.mp4


https://user-images.githubusercontent.com/10728380/131221709-8add9296-b7a6-46ff-97f5-520e854e0041.mp4


## Install

    pip install komoog

`komoog` was developed and tested for 

* Python 3.6
* Python 3.7
* Python 3.8

So far, the package's functionality was tested on macOS only.

## Prerequisites

Save your komoot credentials in `~/.komoog/komoot.json` as

```json
{
    "email" : "your@email.com",
    "password" : "yourpassword",
    "clientid" : "yourclientid"
}
```

You can find your client id in the komoot url when you log in. Click on your username, then
on "Planned Tours" or "Completed Tours". The URL will change to something like

```
https://www.komoot.com/user/1851102841208/tours?type=planned
```

Here, `1851102841208` is your `clientid`.

## Dependencies

`komoog` directly depends on the following packages which will be installed by `pip` during the installation process

* `numpy>=1.17`
* `scipy>=1.5.0`
* `gpxpy>=1.4.2`
* `simplejson>=3.17.2`
* `simpleaudio=>=1.0.4`

## Documentation

The full documentation is available at [komoog.readthedocs.io](http://komoog.readthedocs.io).

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
