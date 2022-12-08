from bluepy.btle import Scanner

while True:
    ble_list = Scanner().scan(3)
    for dev in ble_list:
        print("rssi: {} ; mac: {}".format(dev.rssi,dev.addr))