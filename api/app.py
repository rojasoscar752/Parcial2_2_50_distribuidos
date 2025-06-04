from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pika, json

app = FastAPI(root_path="/api")  # <- ESTA LÍNEA ES CLAVE

security = HTTPBasic()
USERNAME = "oscar"
PASSWORD = "oscar123"

def validar_usuario(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="No autorizado")
    return credentials.username

@app.get("/health")
def estado():
    return {"estado": "ok"}

@app.post("/message")
async def enviar_mensaje(request: Request, user: str = Depends(validar_usuario)):
    cuerpo = await request.json()
    conexion = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    canal = conexion.channel()
    canal.queue_declare(queue="messages", durable=True)
    canal.basic_publish(exchange='', routing_key='messages', body=json.dumps(cuerpo))
    conexion.close()
    return {"resultado": "Mensaje enviado"}
