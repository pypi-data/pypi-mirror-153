from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_contrib.conf import settings
from sqlalchemy import create_engine
from kafka import KafkaProducer
import uvicorn
import socketio
from datetime import datetime
from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info
import os
import time
import json


KAFKA_HOST = os.getenv('KAFKA_HOST', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_EVENTS_TOPIC = os.getenv('KAFKA_EVENTS_TOPIC', 'events')
KAFKA_NOTIFICATIONS_TOPIC = os.getenv('KAFKA_NOTIFICATIONS_TOPIC', 'notifications')
JWT_SECRET = os.getenv('JWT_SECRET', 'jwt_secret')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')


db = create_engine('postgresql://postgres:postgres@message_service_db:5432/postgres')
sio = socketio.AsyncServer(cors_allowed_origins='http://localhost:8000', async_mode='asgi')
app = FastAPI(title='Message Service API')
kafka_producer = None


def setup_opentracing(app):
    config = Config(
        config={
            "local_agent": {
                "reporting_host": settings.jaeger_host,
                "reporting_port": settings.jaeger_port
            },
            "sampler": {
                "type": settings.jaeger_sampler_type,
                "param": settings.jaeger_sampler_rate,
            },
            "trace_id_header": settings.trace_id_header
        },
        service_name="message_service",
        validate=True,
        scope_manager=AsyncioScopeManager()
    )

    app.state.tracer = config.initialize_tracer()
    app.tracer = app.state.tracer


def http_404_requests():
    METRIC = Counter(
        "http_404_requests",
        "Number of times a 404 request has occured.",
        labelnames=("path",)
    )

    def instrumentation(info: Info):
        if info.response.status_code == 404:
            METRIC.labels(info.request.url).inc()

    return instrumentation


def http_unique_users():
    METRIC = Counter(
        "http_unique_users",
        "Number of unique http users.",
        labelnames=("user",)
    )

    def instrumentation(info: Info):
        try:
            user = f'{info.request.client.host} {info.request.headers["User-Agent"]}'
        except:
            user = f'{info.request.client.host} Unknown'
        METRIC.labels(user).inc()

    return instrumentation


instrumentator = Instrumentator(excluded_handlers=["/metrics"])
instrumentator.add(metrics.default())
instrumentator.add(metrics.combined_size())
instrumentator.add(http_404_requests())
instrumentator.add(http_unique_users())
instrumentator.instrument(app).expose(app)


setup_opentracing(app)
socketio_app = socketio.ASGIApp(sio, app)


def register_kafka_producer():
    global kafka_producer
    while True:
        try:
            kafka_producer = KafkaProducer(bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            break
        except:
            time.sleep(3)


def record_action(status: int, message: str, span):
    print("{0:10}{1}".format('ERROR:' if status >= 400 else 'INFO:', message))
    span.set_tag('http_status', status)
    span.set_tag('message', message)


def record_event(type: str, data: dict):
    kafka_producer.send(KAFKA_EVENTS_TOPIC, {
        'type': type,
        'data': data
    })


def save_message(message, roomName, timestamp):
    with app.tracer.start_span('Save Message') as span:
        try:
            span.set_tag('socket_event', 'Save message')
            
            db.execute("""
            insert into message (date, content, sender_id, recipient_id, room) values (%s, %s, %s, %s, %s)
            """, (timestamp, message['content'], message['sender_id'], message['recipient_id'], roomName))

            kafka_producer.send(KAFKA_NOTIFICATIONS_TOPIC, {'type': 'message', 'user_id': message['recipient_id'], 'message': message['sender'] + ": " + message['content']})
            record_action(200, 'Request successful', span)
            record_event('Message Saved', dict(message))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


def list_messages(offset: int, room: str):
    messages = list(db.execute("""select * from message where room = %s order by date asc offset %s limit %s""", (room, offset, 10)))
    results = [{'id': message['id'], 'content': message['content'], 'sender_id': message['sender_id'], 'recipient_id': message['recipient_id'], 'date': message['date'].strftime('%d-%m-%Y, %H:%M:%S')} for message in messages]
    return {'results': results, 'offset': offset, 'limit': 10, 'size': len(results)}


@sio.event
def connect(sid, environ):
    with app.tracer.start_span('Socket Connect') as span:
        try:
            span.set_tag('socket_event', 'Connect')
            
            print("connect: ", sid)
            
            record_action(200, 'Request successful', span)
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@sio.event
def disconnect(sid):
    with app.tracer.start_span('Socket Disconnect') as span:
        try:
            span.set_tag('socket_event', 'Disconnect')
            
            print('disconnect ', sid)
            
            record_action(200, 'Request successful', span)
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@sio.event
def join(sid, roomName):
    with app.tracer.start_span('Socket Join Room') as span:
        try:
            span.set_tag('socket_event', 'Join Room')
            
            sio.enter_room(sid, roomName)
            
            record_action(200, 'Request successful', span)
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@sio.event
def leave(sid, roomName):
    with app.tracer.start_span('Socket Leave Room') as span:
        try:
            span.set_tag('socket_event', 'Leave Room')
            
            sio.leave_room(sid, roomName)
            
            record_action(200, 'Request successful', span)
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


@sio.on('message')
async def chat_message(sid, data, roomName):
    timestamp = datetime.now()
    save_message(data, roomName, timestamp)
    await sio.emit('message', {'content': data['content'], 'sender_id': data['sender_id'], 'recipient_id': data['recipient_id'], 'date': timestamp.strftime('%d-%m-%Y, %H:%M:%S')}, room=roomName)


@sio.on('init')
async def init(sid, data, roomName):
    with app.tracer.start_span('List Messages') as span:
        try:
            span.set_tag('socket_event', 'List messages')

            messages = list_messages(data['offset'], roomName)
            await sio.emit('init', messages, room=sid)

            record_action(200, 'Request successful', span)
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e


app.mount('/', socketio_app)


def run_service():
    register_kafka_producer()
    uvicorn.run(app, host="0.0.0.0", port=8012)


if __name__ == '__main__':
    run_service()
