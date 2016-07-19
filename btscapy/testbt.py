from copy import copy
from time import *
from Queue import *
import Queue as queue
from ctypes import *
import ctypes
bc = cdll.LoadLibrary("csrbc01.dll")
q = queue.Queue()

bc.init()
def show(a,b,c):
  print("b:(", b, ")")
  print( repr(a) )
  pt = POINTER(c_byte * b)
  d = ctypes.cast(a, pt)
  ba = bytearray(d.contents)
  print(len(ba), ba)

CF = CFUNCTYPE(None, c_void_p, c_ulong, c_void_p)
cf = CF(show)
bc.set_event_callback(cf)

ret = bc.open_connection(b'\\\\.\\CSR0')

print ("open result : {}".format(ret))

if not ret:
    print ("open fail !!! exit ")
    exit()

a = (c_byte*256)()

a[0] = 0x03
a[1] = 0x0c
a[2] = 0x00

bc.send_hci_command( cast( a, POINTER(c_byte)), 3)

sleep(10)

a[0] = 0x14
a[1] = 0x0c
a[2] = 0x00

bc.send_hci_command( cast( a, POINTER(c_byte)), 3)


sleep(5)
print ("okay....", q.qsize())
for i in range(q.qsize()):
  print( q.get() ,)