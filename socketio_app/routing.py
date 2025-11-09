from socketio import ASGIApp    
from .sio import sio

socketio_routing = [
    ASGIApp(sio),
]