from sqlalchemy import create_engine
from kafka import KafkaProducer

import pytest
import requests
import time
import json


db = create_engine('postgresql://postgres:postgres@localhost:5436/postgres')
kafka_producer = None
EVENTS_URL = 'http://localhost:8003/api/events'


@pytest.fixture(scope='session', autouse=True)
def do_something(request):
    time.sleep(30)
    global kafka_producer
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:29092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))


def reset_table(number_of_rows=0):
    db.execute('delete from events')
    for i in range(number_of_rows):
        data = str({'name': f'name {i+1}'}).replace("'", '"')
        db.execute(f"insert into events (date, type, data) values (current_timestamp, 'type {i+1}', '{data}')")


def check_events(events: list, limit=7, offset_check=lambda x: 3-x):
    assert len(events) == limit
    for i in range(limit):
        assert events[i]['type'] == f'type {offset_check(i)}'
        assert events[i]['data']['name'] == f'name {offset_check(i)}'


def test_read_events():
    reset_table(3)
    res = requests.get(EVENTS_URL)
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 3

    assert len(body['results']) == 3
    check_events(body['results'], 3)
        
def test_read_events_with_offset():
    reset_table(3)
    res = requests.get(f'{EVENTS_URL}?offset=7')
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] == '/events?search=&offset=0&limit=7'
    assert body['links']['next'] is None
    assert body['offset'] == 7
    assert body['limit'] == 7
    assert body['size'] == 0

    assert len(body['results']) == 0


def test_read_events_with_limit():
    reset_table(3)
    res = requests.get(f'{EVENTS_URL}?limit=7')
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 3

    assert len(body['results']) == 3
    check_events(body['results'], 3)
    

def test_search_events_by_type():
    reset_table(3)
    res = requests.get(f'{EVENTS_URL}?search=TYPE')
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 3

    assert len(body['results']) == 3
    check_events(body['results'], 3)

def test_consuming_events():
    reset_table(0)
    kafka_producer.send('events', {
        'type': 'type 1',
        'data': {
            'name': 'name 1'
        }
    })
    time.sleep(1)
    events = list(db.execute('select * from events'))

    assert len(events) == 1
    assert events[0].type == 'type 1'
    assert events[0].data['name'] == 'name 1'
