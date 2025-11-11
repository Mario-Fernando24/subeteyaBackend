import socketio
import json

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
)

@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")
    await sio.emit("message", {"data": "Conexión establecida"}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

@sio.event
async def message(sid, data):
   print(f'Datos del cliente en socket noooo: {sid}: {data}')
   await sio.emit('new_message', data, to=sid)


@sio.event
async def change_drivers_position(sid, data):
    try:
        # Si 'data' viene como string JSON -> lo convertimos a dict
        json_data = json.loads(data) if isinstance(data, str) else data

        print(f'Emitió nueva posición en sockets {sid}: {json_data}')

        await sio.emit(
            'new_drivers_position',
            {
                'id_socket': sid,
                'id': json_data["id"],
                'latitud': json_data["lat"],
                'longitud': json_data["lng"]
            }
        )

    except json.JSONDecodeError as e:
        print(f'ERROR al parsear JSON: {e}')
    except Exception as e:
        print(f'ERROR inesperado: {e}')

