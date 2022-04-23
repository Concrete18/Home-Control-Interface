from pydub.playback import play
from pydub import AudioSegment
import time


class Helper:
    def benchmark(func):
        """
        Prints `func` name and its benchmark time.
        """

        def wrapped(*args, **kwargs):
            start = time.perf_counter()
            value = func(*args, **kwargs)
            end = time.perf_counter()
            elapsed = round(end - start, 2)
            print(f"{func.__name__} Completion Time: {elapsed}")
            return value

        return wrapped

    @staticmethod
    def play_sound(song_path):
        """
        WIP
        """
        song = AudioSegment.from_mp3(song_path)
        quieter_song = song - 3
        play(quieter_song)
        # quieter_song.export("quieter_song.mp3", format="mp3")
