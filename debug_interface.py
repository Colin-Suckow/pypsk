import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile

class DebugInterface:
    def __init__(self, sample_rate: int, carrier_freq: int):
        self.samp_rate = sample_rate
        self.carrier_freq = carrier_freq

    def send(self, samples: list[complex]):
        samples = np.array(samples)
        # Modulate the samples into a real signal
        t = np.linspace(0, (1.0/self.samp_rate) * len(samples), len(samples))
        sig = (samples.real * np.sin(t * 2.0 * np.pi * self.carrier_freq)) + (samples.imag * np.cos(t * 2.0 * np.pi * self.carrier_freq))

        # plt.plot(sig)
        # plt.show()

        scipy.io.wavfile.write("debugout.wav", self.samp_rate, sig)

    # Blocks until 'num_samples' are recieved. After which the samples are returned
    def receive(self, num_samples) -> list[complex]:
        pass