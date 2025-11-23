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
    await sio.emit('drivers_desconectado', { 'id_socket': sid })


@sio.event
async def message(sid, data):
   print(f'Datos del cliente en socket noooo: {sid}: {data}')
   await sio.emit('new_message', data, to=sid)

@sio.event
async def change_drivers_position(sid, data):
    try:
        #  Convertimos la data a diccionario
       # Verificamos en qué formato llegó la información
        if isinstance(data, dict):
            # Si ya viene como diccionario → se usa tal cual
            json_data = data

        elif isinstance(data, str):
            # Si viene como texto JSON → lo convertimos a diccionario
            json_data = json.loads(data)

        else:
            # Si no es dict ni string, no sabemos procesarlo
            print(f"Tipo de dato no válido: {type(data)}")
            return

        # Mostramos lo recibido
        print(f"Nueva posición recibida de {sid}: {json_data}")

        #  Enviamos la posición a todos los clientes
        await sio.emit(
            'new_drivers_position',
            {
                'id_socket': sid,
                'id': json_data["id"],
                'latitud': json_data["latitud"],
                'longitud': json_data["longitud"]
            }
        )

    except json.JSONDecodeError:
        print("Error al convertir JSON")

    except Exception as e:
        print(f"Error inesperado: {e}")
