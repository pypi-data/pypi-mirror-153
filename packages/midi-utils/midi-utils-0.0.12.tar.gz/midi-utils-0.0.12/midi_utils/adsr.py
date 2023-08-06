# ADSR generator


class ADSR:
    def __init__(
        self,
        attack=0.2,
        decay=0.2,
        sustain=0.7,
        release=0.3,
        samples=20,
        sig_digits=2,
        is_zero_indexed=True,
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
        self.samples = samples  # the number of samples in the note
        self.sig_digits = sig_digits  # what to round values to
        self.is_zero_indexed = is_zero_indexed

    def get_value(self, i):
        """
        Get value of envelope at position i
        """
        # since we'll be using this with a list index, we'll have to handle cases
        # where the index is 0
        if self.is_zero_indexed:
            i += 1
        sample_per = float(i) / self.samples
        val = 0  #
        # attack phase
        if sample_per <= self.attack:
            # rise from 0 to 1
            val = sample_per / self.attack
        # decay phase
        elif (sample_per - self.attack) < self.decay:
            # descend from 1 to sustain level
            decay_ratio = (sample_per - self.attack) / self.decay
            val = 1 - (decay_ratio * (1 - self.sustain_level))
        # sustain phase
        elif (sample_per - self.attack - self.decay) < self.sustain:
            # remain at sustain level
            val = self.sustain_level
        # release phase
        else:
            # descend from sustain level to 0
            release_ratio = (
                sample_per - self.attack - self.decay - self.sustain
            ) / self.release
            val = (1 - release_ratio) * self.sustain_level
        return max(0.0, round(val, self.sig_digits))

    def __iter__(self):
        for i in range(0, self.samples):
            yield self.get_value(i)
