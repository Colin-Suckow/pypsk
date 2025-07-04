import modem
import numpy as np
from debug_interface import DebugInterface
import matplotlib.pyplot as plt
from rtl_interface import RtlInterface
import time

def main():
    SAMP_RATE = int(1000e3)
    CARRIER = int(433.4e6) # 910mhz 
    mmodem = modem.Modem(SAMP_RATE, int(10e3), CARRIER)

    payload = "Wee look at this packet. Ok but here's an even longer one I guess. We need more data to make the message longer".encode("utf-8")

    signal = mmodem.modulate(payload)

    print(f"Signal time = {len(signal)/SAMP_RATE}s")

    #packetsf = mmodem.demodulate(signal[:len(signal)//2])

    #print(f"Demodulated {len(packetsf)} packets from first")

    # packets = mmodem.demodulate(signal[50:])

    # print(f"Demodulated {len(packets)} packets from second")

    # for packet in packets:
    #     print(packet)

    # plt.subplot(211)
    # plt.title("TEDs")
    # plt.plot(mmodem.teds)
    # plt.subplot(212)
    # plt.title("MU")
    # plt.plot(mmodem.mus)
    # plt.show()

    # plt.plot(signal[50:])
    # for i in mmodem.samp_points:
    #     plt.axvline(i, color="r")
    # plt.show()


    #interface = PlutoInterface(SAMP_RATE, CARRIER)
    interface = RtlInterface(SAMP_RATE, CARRIER)
    while True:
        interface.receive(8096)
        #interface.send(signal)
        #time.sleep(1)


if __name__ == "__main__":
    main()