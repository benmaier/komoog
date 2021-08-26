from komoog.komoot import choose_downloaded_komoot_tour
from komoog.audio import convert_tour_to_audio, play_audio

tour = choose_downloaded_komoot_tour()
audio, sampling_rate = convert_tour_to_audio(tour,
                                             tune='C#',
                                             approximate_length_in_seconds=4,
                                             set_tune_to_follow_tour_profile=True,
                                            )
play_audio(audio, sampling_rate)
