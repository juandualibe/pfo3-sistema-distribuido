# PFO 3: Rediseño como Sistema Distribuido (Cliente-Servidor)

Este proyecto implementa una arquitectura distribuida y concurrente utilizando Sockets TCP en Python. El sistema refleja un modelo clásico de separación de responsabilidades, balanceo de carga, procesamiento multihilo y persistencia desacoplada basada en eventos, cumpliendo con las consignas solicitadas.

## 📌 Arquitectura del Sistema

El flujo de la información dentro de la infraestructura distribuida sigue el siguiente orden jerárquico:

1. **Clientes (Móvil y Web):** Envían peticiones simultáneas serializadas en formato JSON hacia el punto de entrada principal del sistema.
2. **Balanceador de Carga / Servidor Distribuidor:** Escucha en el puerto `8080`, recibe las tareas de los clientes y las deriva eficientemente al clúster de servidores backend (Workers).
3. **Servidores Workers (Procesamiento Concurrente):** Escuchan en el puerto `8081`. Al recibir una tarea, el hilo principal delega el procesamiento a un **Pool de Hilos interno (Thread Pool)**, liberando el socket de inmediato para mantener la alta disponibilidad.
4. **Cola de Mensajes (RabbitMQ):** Los hilos del pool envían las tareas procesadas a una cola centralizada para desacoplar el sistema y coordinar la comunicación asíncrona entre servidores.
5. **Almacenamiento Distribuido:** Desde la cola de mensajería, los datos se canalizan y persisten de forma persistente en la Base de Datos Relacional (**PostgreSQL**) y los archivos estáticos o logs se guardan en el Almacenamiento de Objetos (**AWS S3**).

### 📊 Diagrama Arquitectónico

A continuación se detalla el flujo de componentes interactuando de forma descentralizada:

![Diagrama de Arquitectura Distribuida](docs/diagrama.png)

---

## 📁 Estructura del Proyecto

```text
pfo3-sistema-distribuido/
│
├── docs/
│   └── diagrama.png                # Imagen exportada del diagrama de bloques
│
├── src/
│   ├── cliente.py                  # Emisor de tareas (Simula Web y Móvil)
│   ├── servidor_distribuidor.py    # Receptor central y ruteador de carga
│   └── worker.py                   # Servidor concurrente (Pool de hilos e Infraestructura)
│
└── README.md                       # Documentación del proyecto
```

---

## 🚀 Instrucciones de Ejecución (Local)

Para probar la comunicación de red y la concurrencia en tiempo real, se deben abrir 3 terminales independientes y ejecutar los scripts en el siguiente orden estricto:

### 1. Iniciar el Servidor Worker (Infraestructura interna)

En la primera terminal, levantar el proceso del Worker para habilitar el puerto de procesamiento y el Pool de hilos:

```bash
python src/worker.py
```

### 2. Iniciar el Servidor Distribuidor (Orquestador central)

En la segunda terminal, levantar el ruteador que recibirá las conexiones directas de los clientes:

```bash
python src/servidor_distribuidor.py
```

### 3. Ejecutar el Cliente (Emisor de carga)

En la tercera terminal, ejecutar el script que simula las peticiones concurrentes de la aplicación móvil y la interfaz web:

```bash
python src/cliente.py
```

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x (Módulos nativos `socket`, `json` y `concurrent.futures`)
- **Diseño Arquitectónico:** diagramas.net (Draw.io)