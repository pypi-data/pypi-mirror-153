# ADSR generator
from platform import release
from typing import Generator

from .utils import rescale


class ADSR:
    def __init__(
        self,
        attack: float = 0.2,
        decay: float = 0.2,
        sustain: float = 0.7,
        release: float = 0.3,
        samples: int = 20,
        attack_min_level: float = 0.0,
        attack_max_level: float = 1.0,
        sig_digits: int = 2,
        is_zero_indexed: bool = True,
    ):
        self.attack = (
            attack  # the percentage of samples it takes to reach the peak amplitude
        )
        self.decay = decay  # the percentage of samples it takes to descend to the sustain amplitude
        self.sustain_level = sustain  # the amplitude at the sustain level
        self.release = release  # the percentage of samples it takes to reach 0, from the end of the note
        self.sustain = 1.0 - (self.attack + self.decay + self.release)
        # the percentage of samples it stays at the sustain level.
        # this is calculated by subtracting the sum of attack, decay, and release from 1
        if self.sustain < 0:
            raise ValueError(
                "The sum of attack, decay, and release percentages are greater than 1"
            )
        self.samples = samples  # the number of samples in the note
        self.attack_min_level = attack_min_level
        self.attack_max_level = attack_max_level
        self.sig_digits = sig_digits  # what to round values to
        self.is_zero_indexed = is_zero_indexed
        self.idx = -1

    def get_value(self, sample: int):
        """
        Get value of envelope at sample i
        """
        # since we'll be using this with a list index, we'll have to handle cases
        # where the index is 0
        if not self.is_zero_indexed:
            sample += 1
        sample_per = float(sample) / float(self.samples)
        val = 0  # default

        # attack phase
        if sample_per <= self.attack:
            if self.attack == 0:
                val = 1
            else:
                val = rescale(
                    sample_per / self.attack,
                    range_x=[0, 1],
                    range_y=[self.attack_min_level, self.attack_max_level],
                )

        # decay phase
        elif (sample_per - self.attack) < self.decay:
            # descend from 1 to sustain level
            if self.decay > 0:
                decay_ratio = (sample_per - self.attack) / self.decay
            else:
                decay_ratio = 0
            val = 1 - (decay_ratio * (1 - self.sustain_level))

        # sustain phase
        elif (sample_per - self.attack - self.decay) < self.sustain:
            # remain at sustain level
            val = self.sustain_level

        # release phase
        else:
            # descend from sustain level to 0
            if self.release > 0:
                release_ratio = (
                    sample_per - self.attack - self.decay - self.sustain
                ) / self.release
            else:
                release_ratio = 0
            val = (1 - release_ratio) * self.sustain_level
        # never go below zero
        return max(0.0, round(val, self.sig_digits))

    def __iter__(self) -> Generator[float, None, None]:
        for i in range(0, self.samples):
            yield self.get_value(i)

    def __next__(self):
        self.idx += 1
        if self.idx > self.samples:
            raise StopIteration
        return self.get_value(self.idx)
