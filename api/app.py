from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import pika
import json

app = FastAPI()
security = HTTPBasic()

USERNAME = "oscar"
PASSWORD = "oscar123"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

@app.post("/message")
async def send_message(request: Request, username: str = Depends(get_current_user)):
    body = await request.json()
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="messages", durable=True)
    channel.basic_publish(exchange='', routing_key='messages', body=json.dumps(body))
    connection.close()
    return {"status": "Message sent"}
