import time
import api
import settings

u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN)
channel_id = 'B9F17395202DDA7CBC0BF5A822A7720D'
channel_pwd = ""

cicles_count = 1000

for i in range(cicles_count):
    print("cicle: {}".format(i))
    u.joinChannel(channel_id, channel_pwd)
    #time.sleep(1)
    u.leaveChannel(channel_id)
    #time.sleep(1)