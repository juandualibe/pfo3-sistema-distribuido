import socket
import json

IP_LOCAL = '127.0.0.1'
PUERTO_ESCUCHA = 8080
PUERTO_WORKER = 8081  # Puerto hacia donde derivamos la tarea

def desviar_a_worker(datos_tarea):
    """ Se conecta al Worker por socket para delegarle la tarea """
    socket_worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socket_worker.connect((IP_LOCAL, PUERTO_WORKER))
        socket_worker.sendall(json.dumps(datos_tarea).encode('utf-8'))
        
        respuesta = socket_worker.recv(1024).decode('utf-8')
        return json.loads(respuesta)
    except ConnectionRefusedError:
        return {"estado": "error", "mensaje": "El Worker no esta disponible."}
    finally:
        socket_worker.close()

def iniciar_distribuidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_LOCAL, PUERTO_ESCUCHA))
    servidor.listen()
    print(f"[*] Servidor Distribuidor escuchando en el puerto {PUERTO_ESCUCHA}...")

    try:
        while True:
            conexion, direccion = servidor.accept()
            peticion = conexion.recv(1024).decode('utf-8')
            if not peticion:
                conexion.close()
                continue
                
            datos_tarea = json.loads(peticion)
            print(f"[->] Tarea {datos_tarea['id']} recibida. Redirigiendo al Worker...")
            
            # Delegamos la tarea al puerto del Worker
            respuesta_worker = desviar_a_worker(datos_tarea)
            
            # Devolvemos la respuesta final que genero el worker hacia el cliente
            conexion.sendall(json.dumps(respuesta_worker).encode('utf-8'))
            conexion.close()
    except KeyboardInterrupt:
        print("\n[*] Apagando distribuidor...")
    finally:
        servidor.close()

if __name__ == "__main__":
    iniciar_distribuidor()