import adi

class PlutoInterface:
    def __init__(self, sample_rate: int, carrier_freq: int):
        self.sdr = adi.Pluto('ip:192.168.2.1')
        self.sdr.sample_rate = sample_rate
        self.sdr.rx_lo = carrier_freq
        self.sdr.rx_rf_bandwidth = sample_rate
        self.sdr.rx_buffer_size = 1024

        self.sdr.tx_hardwaregain_chan0 = -50
        self.sdr.tx_rf_bandwidth = sample_rate
        self.sdr.tx_lo = carrier_freq
    
    def receive(self):
        return self.sdr.rx()
    
    def send(self, samples: list[complex]):
        self.sdr.tx(samples)