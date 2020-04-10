import websocket
import _thread
import api
import settings

def run():
    global ws
    ws = websocket.WebSocketApp('ws://127.0.0.1:20001/UtopiaWSS/?token='+settings.TOKEN,
                        on_message = on_message,
                        on_error = on_error,
                        on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"check_hostname": False})
    try:
        ws.send("Hi")
    except Exception as e:
        print(e)
    
    
def on_message(ws, message):
    print(message)    
def on_error(ws, error):
    print(error)
def on_close(ws):
    print("*** web socket closed")
def on_open(ws):
    def run():
        try:
            ws.send("ping")
            u = api.Utopia("http://127.0.0.1:"+settings.API_PORT+"/api/1.0",settings.TOKEN)
            print(u.getSystemInfo())
            del u
        except:
            print("*** WebSocket is not available")
    _thread.start_new_thread(run, ())

ws=''
run()
