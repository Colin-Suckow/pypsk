import modem
import numpy as np
from debug_interface import DebugInterface
import matplotlib.pyplot as plt

def main():
    SAMP_RATE = 44100
    CARRIER = 1000
    mmodem = modem.Modem(SAMP_RATE, 500, CARRIER)

    payload = "Wee look at this packet".encode("utf-8")

    signal = mmodem.modulate(payload)

    packetsf = mmodem.demodulate(signal[:len(signal)//2])

    print(f"Demodulated {len(packetsf)} packets from first")

    packets = mmodem.demodulate(signal[len(signal)//2:])

    print(f"Demodulated {len(packets)} packets from second")

    for packet in packets:
        print(packet)

    interface = DebugInterface(SAMP_RATE, CARRIER)

    interface.send(signal)


if __name__ == "__main__":
    main()