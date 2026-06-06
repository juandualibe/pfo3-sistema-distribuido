import socket
import json
import time
from concurrent.futures import ThreadPoolExecutor

IP_LOCAL = '127.0.0.1'
PUERTO_ESCUCHA = 8081
MAX_HILOS = 3  # Tamaño de nuestro pool de hilos (Thread Pool)

def flujo_procesamiento_distribuido(tarea):
    """ Ejecuta la simulacion de la arquitectura dentro de un hilo del pool """
    id_t = tarea.get("id")
    tipo = tarea.get("tipo")
    
    print(f"[-] [Hilo-Pool] Iniciando procesamiento de tarea {id_t}...")
    time.sleep(1.5)  # Simula tiempo de trabajo concorrente
    
    # Simulación del camino que dibujaste en tu diagrama
    print(f"[-] [RabbitMQ] Tarea {id_t} enviada a la cola centralizada.")
    print(f"[-] [PostgreSQL] Registrando estado en la Base de Datos.")
    print(f"[-] [AWS S3] Guardando archivos estaticos en el almacenamiento.")
    
    return {
        "estado": "completado",
        "tarea_id": id_t,
        "camino_arquitectura": "ThreadPool -> RabbitMQ -> Persistido en Postgres y S3"
    }

def gestionar_peticion(conexion, direccion):
    try:
        peticion = conexion.recv(1024).decode('utf-8')
        if not peticion:
            return
            
        datos_tarea = json.loads(peticion)
        
        # El hilo del pool asignado procesa la tarea de punta a punta
        resultado = flujo_procesamiento_distribuido(datos_tarea)
        
        conexion.sendall(json.dumps(resultado).encode('utf-8'))
    except Exception as e:
        print(f"[!] Error en el procesamiento del worker: {e}")
    finally:
        conexion.close()

def iniciar_worker():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_LOCAL, PUERTO_ESCUCHA))
    servidor.listen()
    print(f"[*] Servidor Worker escuchando en el puerto {PUERTO_ESCUCHA}...")
    print(f"[*] Pool de hilos activo. Maximo {MAX_HILOS} tareas simultaneas.")

    # Inicializamos el Pool de hilos
    with ThreadPoolExecutor(max_workers=MAX_HILOS) as pool:
        try:
            while True:
                conexion, direccion = servidor.accept()
                # Delegamos la conexion al pool para que el servidor siga libre escuchando
                pool.submit(gestionar_peticion, conexion, direccion)
        except KeyboardInterrupt:
            print("\n[*] Apagando servidor Worker...")
        finally:
            servidor.close()

if __name__ == "__main__":
    iniciar_worker()