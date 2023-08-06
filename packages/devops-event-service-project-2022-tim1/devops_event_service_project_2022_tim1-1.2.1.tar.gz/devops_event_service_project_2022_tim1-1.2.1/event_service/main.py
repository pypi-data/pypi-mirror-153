from fastapi import FastAPI, Query
from fastapi_contrib.conf import settings
from sqlalchemy import create_engine
from kafka import KafkaConsumer
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from jaeger_client import Config
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from prometheus_fastapi_instrumentator.metrics import Info

import uvicorn
import datetime
import time
import json
import threading
import os

DB_USERNAME = os.getenv('DB_USERNAME', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'event_service_db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')
KAFKA_HOST = os.getenv('KAFKA_HOST', 'kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT', '9092')
KAFKA_EVENTS_TOPIC = os.getenv('KAFKA_EVENTS_TOPIC', 'events')
EVENTS_URL = '/api/events'

app = FastAPI(title='Event Service API')
db = create_engine(f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

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
        service_name="event_service",
        validate=True,
        scope_manager=AsyncioScopeManager()
    )

    app.state.tracer = config.initialize_tracer()
    app.tracer = app.state.tracer

setup_opentracing(app)

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

class Event(BaseModel):
    id: Optional[int] = Field(description='Event ID')
    date: Optional[datetime.datetime] = Field(description='Event Date')
    type: str = Field(description='Event Type')
    data: Dict = Field(description='Event Data')

class NavigationLinks(BaseModel):
    base: str = Field('http://localhost:9000/api', description='API base URL')
    prev: Optional[str] = Field(None, description='Link to the previous page')
    next: Optional[str] = Field(None, description='Link to the next page')

class EventResponse(BaseModel):
    results: List[Event]
    links: NavigationLinks
    offset: int
    limit: int
    size: int

def record_action(status: int, message: str, span):
    print("{0:10}{1}".format('ERROR:' if status >= 400 else 'INFO:', message))
    span.set_tag('http_status', status)
    span.set_tag('message', message)

@app.get(EVENTS_URL)
def read_events(search: str = Query(''), offset: int = Query(0), limit: int = Query(7)):
    with app.tracer.start_span('Read Events Request') as span:
        try:
            span.set_tag('http_method', 'GET')
            total_events = len(list(db.execute(f'select * from events where lower(type) like %s', (f'%{search.lower()}%',))))
            events = list(db.execute(f'select * from events where lower(type) like %s order by date desc offset {offset} limit {limit}', (f'%{search.lower()}%',)))
            
            prev_link = f'/events?search={search}&offset={offset - limit}&limit={limit}' if offset - limit >= 0 else None
            next_link = f'/events?search={search}&offset={offset + limit}&limit={limit}' if offset + limit < total_events else None
            links = NavigationLinks(prev=prev_link, next=next_link)
            results = [Event.parse_obj(dict(event)) for event in events]
            
            record_action(200, 'Request successful', span)
            return EventResponse(results=results, links=links, offset=offset, limit=limit, size=len(results))
        except Exception as e:
            record_action(500, 'Request failed', span)
            raise e            


def register_events_consumer():
    def poll():
        while True:
            try:
                consumer = KafkaConsumer(KAFKA_EVENTS_TOPIC, bootstrap_servers=[f'{KAFKA_HOST}:{KAFKA_PORT}'])
                break
            except:
                time.sleep(3)

        for data in consumer:
            try:
                event = Event.parse_obj(json.loads(data.value.decode('utf-8')))
                db.execute('insert into events (date, type, data) values (current_timestamp, %s, %s)', (event.type, str(event.data or {}).replace("'", '"').replace('None', 'null').replace('True', 'true').replace('False', 'false')))
            except:
                pass

    threading.Thread(target=poll).start()


def run_service():
    register_events_consumer()
    uvicorn.run(app, host='0.0.0.0', port=8003)


if __name__ == '__main__':
    run_service()
