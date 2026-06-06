import socket
import json

IP_DISTRIBUIDOR = '127.0.0.1'
PUERTO_DISTRIBUIDOR = 8080

def enviar_tarea(id_tarea, tipo_tarea, origen):
    # Creamos un socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        cliente.connect((IP_DISTRIBUIDOR, PUERTO_DISTRIBUIDOR))
        
        # Estructura de la tarea en español
        tarea = {
            "id": id_tarea,
            "tipo": tipo_tarea,
            "origen": origen,  # Puede ser 'web' o 'movil'
            "datos": "Informacion base para procesar"
        }
        
        print(f"[+] [{origen.upper()}] Enviando tarea {id_tarea} al distribuidor...")
        cliente.sendall(json.dumps(tarea).encode('utf-8'))
        
        # Esperamos la respuesta del sistema distribuido
        respuesta_cruda = cliente.recv(1024).decode('utf-8')
        resultado = json.loads(respuesta_cruda)
        
        print(f"[+] Respuesta del sistema: {resultado}\n")
        
    except ConnectionRefusedError:
        print("[!] Error: No se pudo conectar con el distribuidor. ¿Esta encendido?")
    finally:
        cliente.close()

if __name__ == "__main__":
    # Simulamos un cliente web y uno movil enviando tareas consecutivas
    enviar_tarea(id_tarea=101, tipo_tarea="PROCESAR_IMAGEN", origen="web")
    enviar_tarea(id_tarea=102, tipo_tarea="SUBIR_REPORTE", origen="movil")