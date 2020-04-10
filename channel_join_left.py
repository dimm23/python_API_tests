import time
import api
import settings

import re
from timeit import default_timer as timer
import datetime
from array import array
import json

u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN, 0)
channel_id = '765A6FD1472AF2C1D6DEF82FE23CE3D8'
channel_pwd = ""

cicles_count = 100

while True:
    start = timer()  
    for i in range(1, cicles_count):  
        status, result = u.getSystemInfo()        
    end = timer()
    now = datetime.datetime.now()        
    print (now.strftime("%Y-%m-%d %H:%M:%S"),"  ", end - start)

    for i in range(1, cicles_count):        
        u.joinChannel(channel_id, channel_pwd)
        time.sleep(1)
        u.sendChannelMessage(channel_id, "Spammer message: current GMT-0 time is {}".format(time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime())))
        time.sleep(1)
        u.leaveChannel(channel_id)
        time.sleep(1)
    time.sleep(30)
    
