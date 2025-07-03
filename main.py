import modem
import numpy as np
from debug_interface import DebugInterface
import matplotlib.pyplot as plt
from pluto_interface import PlutoInterface
import time

def main():
    SAMP_RATE = int(1000e3)
    CARRIER = int(910e6) # 910mhz 
    mmodem = modem.Modem(SAMP_RATE, 500, CARRIER)

    payload = "Wee look at this packet".encode("utf-8")

    signal = mmodem.modulate(payload)

    # packetsf = mmodem.demodulate(signal[:len(signal)//2])

    # print(f"Demodulated {len(packetsf)} packets from first")

    # packets = mmodem.demodulate(signal[len(signal)//2:])

    # print(f"Demodulated {len(packets)} packets from second")

    # for packet in packets:
    #     print(packet)

    interface = PlutoInterface(SAMP_RATE, CARRIER)

    while True:
        interface.send(signal)
        time.sleep(3)


if __name__ == "__main__":
    main()