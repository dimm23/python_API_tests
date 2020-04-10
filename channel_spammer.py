import time
import api
import settings

u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN)
channelid = '49B12FECF93F5A1815202B76E35E6A76' # Channel for sending spam messages
msgs_count = 5000
timeout = 5             # Time in minutes
sending_by = "count"     # 'time' or 'count'
long_text = "тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый текст тестовый тестовый текст тестовый текст"

current_time = time.strftime("%H:%M:%S", time.gmtime()).split(":")
end_time = "{}:{:>02}:{}".format(current_time[0], int(current_time[1])+timeout, current_time[2])

if (sending_by == "time"):
    while(time.strftime("%H:%M:%S", time.gmtime()) != end_time):
        print(u.sendChannelMessage(channelid, "Spammer message: current GMT-0 time is {}; end time is {}".format(time.strftime("%d.%m.%Y %H:%M:%S", time.gmtime()), end_time)))
        time.sleep(0.5)
else:
    for i in range(msgs_count):
        start_time = time.strftime("%H:%M:%S", time.gmtime()).split(":")
        current_time = "{} {}:{:>02}:{}".format(time.strftime("%d.%m.%Y", time.gmtime()), int(start_time[0]) + 7, int(start_time[1]), start_time[2])
        u.sendChannelMessage(channelid, "Spammer message #{}, Date: {} \n {}".format(i+1, current_time, long_text))
        time.sleep(0.5)

