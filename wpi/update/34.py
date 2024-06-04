import win32api
import win32net
# import win32netcon, win32wnet
#
# username = 'eik\gurkin-vlv'
# password = '10-crysis-10'
#
# try:
#     win32wnet.WNetAddConnection2(win32netcon.RESOURCETYPE_DISK, 'Z:', '\\10.5.0.138\\electrolab', None, 'eik\\gurkin-vlv', '10-crysis-10',0)
#     print("connection established successfully")
# except:
#     print("connection not established")


import win32api
import win32net
ip = '10.5.0.138'
username = 'eik\\gurkin-vlv'
password = '10-crysis-10'
use_dict={}
use_dict['remote']= '\\\\10.5.0.138\\electrolab'
use_dict['password']=password
use_dict['username']=username
win32net.NetUseAdd(None, 2, use_dict)