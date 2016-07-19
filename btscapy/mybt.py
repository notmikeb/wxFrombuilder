from scapy.layers import bluetooth
from scapy.layers.bluetooth import *
#a = bluetooth.BluetoothHCISocket()
#a =bluetooth.BluetoothUserSocket(adapter = 0)

#BluetoothUserSocket(adapter = 0)
#import PyBT
#a = PyBT.roles.LE_Central(adapter=0)
a = bluetooth.BluetoothDaySocket()
p = HCI_Hdr()/HCI_Command_Hdr()/HCI_Cmd_Read_BD_Addr()
a.send(p)
k = a.recv()
for i, value  in enumerate(k):
    print (i, value)


