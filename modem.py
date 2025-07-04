import utils
import binascii
import struct
import commpy.filters
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import scipy.signal

SYNC_SIZE = 256
MAGIC = "CAFEDOOD".encode("utf-8")

def interp_read(data, index):
    if index < 0:
        return data[0]
    elif index >= len(data):
        return data[-1]
    else:
        return data[int(index)] #np.interp(index, range(len(data)), data)

class Modem:
    def __init__(self, samp_rate: int, baud_rate: int, carrier_freq: int):
        self.samp_rate = samp_rate
        self.baud_rate = baud_rate
        self.carrier_freq = carrier_freq

        self.sps = self.samp_rate // self.baud_rate
        print(f"Configured modem with {self.sps} samples per symbol")

        self.bit_buf = []
        self.teds = []
        self.mus = []
        self.samp_points = []
        self.err_i = 0

        self.kp = 0.0005
        self.ki = 0.0

        self.last_raw_bit = 0

        self.bit_buf_max_size = 80e3
        
        self.filt_size = 8 * self.sps + 1
        _, self.rcc_taps = self._get_pulse_filt()
        self.rcc_filt_state = np.zeros(self.filt_size - 1, dtype=complex)

    # Wraps payload with a header and CRC, modulates frame into a BPSK signal
    def modulate(self, data: bytearray) -> list[complex]:
        # Create an MSB crc of the data
        crc = struct.pack(">I", binascii.crc32(data))

        # Pack the payload size
        payload_size = struct.pack(">I", len(data))

        # Convert payload into bits
        data = utils.as_bits(MAGIC + payload_size + data + crc)

        # Add the sync pattern (all 1's because 1 is encoded to a transition when diff encoded)
        data = ([1] * SYNC_SIZE) + data

        # Diff encode the payload bits
        data = utils.diff_encode(data)

        # Convert the bits into complex symbols
        data = [complex(b * 2 - 1,0) for b in data]

        # Make each sample a single impulse of SPS length, for pulse shaping
        symbols = []
        for s in data:
            symbols.append(s)
            for _ in range(self.sps - 1):
                symbols.append(complex(0,0))

        # Pulse shape
        symbols = scipy.signal.lfilter(self.rcc_taps, [1.0], symbols)

        symbols /= max(np.abs(symbols))

        return symbols


    # Maintains state between calls. If a frame was demodulated, it is returned in a list. Otherwise it returns None.
    # Keep calling with new samples to update the state machine
    def demodulate(self, signal: list[complex]) -> list[bytearray]:
        # Apply the second half of our pulse shaping filter
        signal, self.rcc_filt_state = scipy.signal.lfilter(
            self.rcc_taps,
            [1.0],
            signal,
            zi=self.rcc_filt_state
        )

        
        # Sync with our new samples
        raw_bits = []
        index = 0
        while index <= len(signal):
            # Read the samples we need
            prompt = interp_read(signal, index)
            self.samp_points.append(index)
            last = interp_read(signal, (index - self.sps))
            mid = interp_read(signal, (index - (self.sps / 2)))

            raw_bits.append(1 if mid.real > 0 else 0)

            ted = np.real(np.conj(mid) * (prompt - last))
            self.teds.append(ted)

            err_p = ted * self.kp
            self.err_i += ted * self.ki

            error = err_p + self.err_i

            period_update = self.sps - error

            self.mus.append(period_update % 1.0)

            if period_update < self.sps * 0.5:
                period_update = self.sps * 0.5
            elif period_update > self.sps * 1.5:
                period_update = self.sps * 1.5

            index += period_update


        # We've processed the new samples, now see if we can do something with the bits
        # Undo the differential encoding and save to our bit buffer
        # Also include the last raw bit from the last loop to make sure we don't break the differential encoding
        self.bit_buf += utils.diff_decode([self.last_raw_bit] + raw_bits)

        # Save the last bit from our raw bits array for the next loop
        self.last_raw_bit = raw_bits[-1]

        # Try to find a packet in our bit buffer
        magic_correlation = np.correlate((np.array(self.bit_buf) * 2) - 1, np.array(utils.as_bits(MAGIC)) * 2 - 1)

        # Find the indices that match the magic value
        magics = [i for i, corr in enumerate(magic_correlation) if corr >= len(MAGIC) * 8]
        payloads = []
        last_bit = 0

        # If we didn't find any magics, it should be safe to cull half of our bit buffer
        if len(self.bit_buf) >= self.bit_buf_max_size and len(magics) == 0:
            self.bit_buf = self.bit_buf[self.bit_buf_max_size // 2:]

        for packet_start in magics:
            try:
                # Decode the packet len field
                len_bytes = utils.as_bytes(self.bit_buf[packet_start + 8*8:packet_start + ((4 + 8) * 8)])
                packet_len = struct.unpack(">I", len_bytes)[0]

                # unpack our data
                payload = utils.as_bytes(self.bit_buf[packet_start + ((4 + 8) * 8):packet_start + ((4 + 8 + packet_len) * 8)])
                expected_crc = struct.unpack(">I", utils.as_bytes(self.bit_buf[packet_start + ((4 + 8 + packet_len) * 8):packet_start + ((4 + 8 + packet_len + 4) * 8)]))[0]
                calculated_crc = binascii.crc32(payload)

                if expected_crc == calculated_crc:
                    payloads.append(payload)

                last_bit = packet_start + ((4 + 8 + packet_len + 4) * 8)
            except:
                # If we failed to grab all the bits we need we are probably waiting for more data. Just break out for now
                break

        # Clear out the bits we just checked from our buffer
        self.bit_buf = self.bit_buf[last_bit:]

        return payloads


    def _get_pulse_filt(self):
        return commpy.filters.rcosfilter(self.filt_size, 0.3, 1/self.baud_rate, self.samp_rate)




