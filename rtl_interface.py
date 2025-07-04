from rtlsdr import RtlSdr

class RtlInterface:
    def __init__(self, sample_rate: int, carrier_freq: int):
        self.sdr = RtlSdr()
        self.sdr.sample_rate = sample_rate
        self.sdr.center_freq = carrier_freq
        self.sdr.gain = "auto"

    def receive(self, num_samples) -> list[complex]:
        return self.sdr.read_samples(num_samples) / 100.0

    def send(self, samples: list[complex]):
        # RTLSDR does not support transmitting
        return None