import time
import api
import settings

u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN)
channelid = '81B8CA0B8E2A5C87C468927953BEB674' # Channel for sending spam messages
msgs_count = 500
timeout = 1             # Time in minutes
sending_by = "time"     # 'time' or 'count'

current_time = time.strftime("%H:%M:%S", time.gmtime()).split(":")
end_time = "{}:{:>02}:{}".format(current_time[0], int(current_time[1])+timeout, current_time[2])

if (sending_by == "time"):
    while(time.strftime("%H:%M:%S", time.gmtime()) != end_time):
        print(u.sendChannelMessage(channelid, "Spammer message: current GMT-0 time is {}; end time is {}".format(time.strftime("%H:%M:%S", time.gmtime()), end_time)))
        time.sleep(0.5)
else:
    for i in range(msgs_count):
        u.sendChannelMessage(channelid, "Spammer message #{} from {}".format(i+1, msgs_count))
        time.sleep(1)

