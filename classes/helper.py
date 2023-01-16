import winsound, time, sys
from threading import Thread


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


class Helper:
    @staticmethod
    def warning_sound():
        """
        Makes a sound denoting a task warning.
        """

        def threaded_sound():
            """
            Function defined so it can be run in a new thread.
            """
            if sys.platform == "win32":
                winsound.PlaySound("SystemHand", winsound.SND_ALIAS)

        Thread(target=threaded_sound).start()
        print("warning sound was played")
