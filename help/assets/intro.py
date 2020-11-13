from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.event
async def connect(sid, environ):
    print('{} just joined'.format(sid))

@sio.event
async def disconnect(sid):
    print('{} just left'.format(sid))

@sio.event()
async def vvvv_message(sid, message):
    print('Received "{}" from vvvv, from sid {}. Replying...'.format(message, sid))
    await sio.emit("python", "this is python speaking")

if __name__ == '__main__':
    web.run_app(app)
