from komoog.komoot import download_all_komoot_tours, choose_downloaded_komoot_tour
from komoog.audio import convert_tour_to_audio, play_audio

download_all_komoot_tours()
tour = choose_downloaded_komoot_tour()
audio, sampling_rate = convert_tour_to_audio(tour,
                                             approximate_length_in_seconds=4,
                                             set_tune_to_follow_tour_profile=True,
                                            )
play_audio(audio, sampling_rate)
