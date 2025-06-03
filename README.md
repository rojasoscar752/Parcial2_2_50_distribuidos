# Parcial2_2_50_distribuidos

SECCIÓN 1- Parte teórica: CONCEPTOS TEÓRICOS
1.1 RabbitMQ

¿Qué es RabbitMQ?
RabbitMQ es un message broker (intermediario de mensajes) que permite que aplicaciones se comuniquen de forma asincrónica mediante el envío y recepción de mensajes a través de colas.

¿Cuándo usar una cola frente a un exchange tipo fanout?

    Cola directa (direct): Se usa cuando se quiere que el mensaje llegue a un consumidor específico.

    Exchange tipo fanout: Se usa cuando queremos que el mensaje se reenvíe a todos los consumidores conectados (broadcast).

¿Qué es una Dead Letter Queue (DLQ)?
Es una cola especial a donde se redirigen mensajes que no pudieron ser entregados o procesados exitosamente. Se configura mediante políticas que definen una DLX (Dead Letter Exchange) y una cola de destino.

1.2 Docker y Docker Compose

Diferencia entre volumen y bind mount:

    Volumen: Administrado por Docker (docker volume create), persiste datos fuera del contenedor.

volumes:
  - data_volume:/app/data

Bind mount: Vincula una ruta del host directamente al contenedor.

    volumes:
      - ./datos:/app/data

¿Qué implica usar network_mode: host?
El contenedor compartirá la red del host directamente (sin aislamiento de red). No es compatible en todos los sistemas (no funciona en Docker Desktop para Windows/Mac).
1.3 Traefik

Función de Traefik:
Es un reverse proxy que enruta automáticamente el tráfico HTTP hacia los servicios correctos en una arquitectura de microservicios. Administra certificados, balanceo de carga y descubrimiento de servicios.

¿Cómo asegurar un endpoint con TLS automático?
Traefik puede usar Let's Encrypt para generar certificados TLS automáticamente si se configura con entrypoints para HTTPS y se activa ACME:

entrypoints:
  websecure:
    address: ":443"

certificatesResolvers:
  myresolver:
    acme:
      email: tu@email.com
      storage: acme.json
      httpChallenge:
        entryPoint: web
