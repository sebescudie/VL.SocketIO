from aiohttp import web
import socketio
import logging
import os, inspect

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

# serve the web page
async def index(request):
    working_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    with open(working_dir + '\index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

# connection event
@sio.event
async def connect(sid, environ):
    print('{} just joined'.format(sid))

# events from vvvv
@sio.event
async def framerate(sid, message):
    print('VVVV framerate is {}'.format(message))

@sio.event()
async def circle_position(sid, message):
    print('Circle\'s position is {}'.format(message))
    await sio.emit('update_circle_position', message)

# webpage controls to vvvv
@sio.on('setBackgroundColor')
async def set_background_color(sid, message):
    print("Webpage sets background color to {}".format(message))
    await sio.emit('set_background_color', message)

@sio.on('setDrawingMode')
async def set_drawing_mode(sid, message):
    print('Webpage sets drawing mode to {}'.format(message))
    await sio.emit('set_drawing_mode', message)

@sio.on('setEffects')
async def set_effects(sid, message):
    print('Webpage sets effects to {}'.format(message))
    await sio.emit('set_effects', message)

@sio.on('setRadius')
async def set_radius(sid, message):
    print('Webpage sets circle radius to {}'.format(message))
    await sio.emit('set_radius', message)

@sio.on('set_framerate')
async def set_framerate(sid, message):
    await sio.emit('update_framerate', message)

app.router.add_get('/', index)
app.router.add_get('/index', index)

if __name__ == '__main__':
    web.run_app(app)