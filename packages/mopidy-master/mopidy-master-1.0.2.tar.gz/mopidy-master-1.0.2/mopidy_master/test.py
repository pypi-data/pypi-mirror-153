from websocket import create_connection
import json
def uri_to_master(uri):
        params = uri.split(':')
        params.pop(0)
        params.pop(0)
        uri = ":".join(params)
        return uri

#print(uri_to_master('mopidymopidy:track:yandexmusic:track:23602860'))

payload = {
  "method": "core.mixer.get_volume",
  "jsonrpc": "2.0",
  "params":{},
          "id": 8
}
#ws = create_connection("ws://192.168.2.238:6680/master/socketapi/ws")
ws = create_connection("ws://192.168.2.238:6680/mopidy/ws")
#ws.send(json.dumps({'message':'list'}))
ws.send(json.dumps(payload))
print(ws.recv())



