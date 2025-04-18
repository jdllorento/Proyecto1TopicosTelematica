# Bienvenido al proyecto 1 de Tópicos de Telemática del periodo 2025-1

Este es un sistema de arquitectura distribuida, en la cual un cliente tiene la capacidad de hacer solicitudes para operaciones matemáticas a través de microservicios, a los cuales se accede con la redirección de un API gateway, así como soportar la comunicación entre microservicios y un sistema de failover donde se guardan los mensajes cuando un microservicio no está disponible para luego recuperarlos

## Guía de uso

### Requisitos: 
 * Tener instalado gRPC en las máquinas virtuales
 * Tener instalado python y el repositorio clonado
 * Tener instalado Docker

### ¿Cómo ejecutar?

### Primero, levantar Redis en el puerto 6379, a través del siguiente comando:

```console
  docker run -d --name redis-mom -p 6379:6379 redis
```

### Luego, poner a correr los microservicios de manera individual, estando en la carpeta raíz del proyecto ejecutar:

```console
  python -m microservices.sum_service.server
  
  python -m microservices.subtract_service.server
  
  python -m microservices.multiply_service.server
```

Luego de ejecutarlos debería retornarse que el microservicio está corriendo y el puerto correspondiente

### Luego ejecutar el API gateway, estando en la carpeta raíz del proyecto, ejecutar:

```console
  uvicorn api_gateway.main:app --host 0.0.0.0 --port 8000 --reload
```

Si es exitoso se va a dar el log del estado, así como los GET que haga el usuario

### Para ejecutar las solicitudes:

Estando en la carpeta raíz, usar el comando curl para especificar el servicio y los operandos:

```console
  curl http://localhost:8000/multiply/6/7  // Ejemplo para multiplicación de 6 y 7

  curl http://localhost:8000/add/6/7  // Ejemplo para suma de 6 y 7

  curl http://localhost:8000/subtract/6/7 // Ejemplo para resta de 6 y 7
```

### Para recuperar los resultados:

Este sistema funciona con Redis, este se ejecuta en un contenedor de Docker y cuando los servicios no están disponibles se guardan los mensajes, para que cuando el servicio vuelva a encenderse, recuperarlos y procesar las operaciones, luego el cliente puede acceder a los resultados de estas operaciones que fueron encoladas a través de la ruta:

```console
  http://localhost:8000/pending_results
```
