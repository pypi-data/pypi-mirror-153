import time
from typing import Union


class Timer:

    @property
    def current_split_time(self) -> float:
        return time.time() - self.last_split_time

    @property
    def elapsed_time(self) -> float:
        return time.time() - self.start_time

    @staticmethod
    def print_list(messages):
        print("\n".join(messages))

    def display_message(self, message: str = "Time since started: {time_since_start}"):
        current_time = time.time()
        values = {"time_since_start": current_time - self.start_time,
                  "time_since_last_split": current_time - self.last_split_time,
                  "current_split": self.total_splits,
                  "average_time_per_split": (current_time - self.start_time) / max(self.total_splits, 1)}
        try:
            if self.prefix is not None:
                self.print_list(f"{self.prefix} {m}" for m in message.format(**values).split('\n'))
            else:
                print(message.format(**values))
        except KeyError:
            self.print_list("Only accepted keys are :",
                            "- time_since_start",
                            "- time_since_last_split",
                            "- current_split",
                            "- average_time_per_split")

    def split(self, message: Union[str, None] = "{current_split}: {time_since_last_split}"):
        self.total_splits += 1
        current_time = time.time()
        if message is not None:
            self.display_message(message)
        self.last_split_time = current_time

    def reset(self):
        self.start_time = time.time()
        self.last_split_time = self.start_time
        self.total_splits = 0

    def __enter__(self):
        """
        Initialize self.last_time
        Allows the usage of :
        with Converter(..) as ... :
            ...
        :return: self
        """
        return self

    def __exit__(self,
                 exc_type,
                 exc_val,
                 exc_tb):
        """
        More explications on __enter__ and __exit__ on :
        https://docs.python.org/2.5/whatsnew/pep-343.html#SECTION000910000000000000000
        :param exc_type: exception type
        :param exc_val: exception value
        :param exc_tb: exception stack trace
        :return: Boolean, do we suppress exceptions ?
        """
        message = ["Total elapsed time: {time_since_start:6.4f}"]
        if self.total_splits > 1:
            message += ["Number of splits: {current_split}",
                        "Average time per split: {average_time_per_split:6.4f}"]
        self.display_message("\n".join(message))
        return exc_type is None

    def __init__(self, prefix: Union[str, None] = None):
        self.start_time = time.time()
        self.last_split_time = self.start_time
        self.total_splits = 0
        self.prefix = prefix
