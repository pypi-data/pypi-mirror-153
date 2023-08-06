from event_service.main import app, EVENTS_URL
from fastapi.testclient import TestClient
from mock import patch

class TestDB:
    def execute(self, sql, params):
        return []

client = TestClient(app)
testDB = TestDB()


@patch('event_service.main.db', testDB)
def test_read_events():
    with patch.object(testDB, 'execute', wraps=testDB.execute) as db_spy:        
        res = client.get(EVENTS_URL)
        assert res.status_code == 200
        db_spy.assert_called()
        db_spy.assert_called_with('select * from events where lower(type) like %s order by date desc offset 0 limit 7', ('%%',))
        
@patch('event_service.main.db', testDB)
def test_read_events_with_offset():
    with patch.object(testDB, 'execute', wraps=testDB.execute) as db_spy:        
        res = client.get(f'{EVENTS_URL}?offset=7')
        assert res.status_code == 200
        db_spy.assert_called()
        db_spy.assert_called_with('select * from events where lower(type) like %s order by date desc offset 7 limit 7', ('%%',))

@patch('event_service.main.db', testDB)
def test_read_events_with_limit():
    with patch.object(testDB, 'execute', wraps=testDB.execute) as db_spy:        
        res = client.get(f'{EVENTS_URL}?limit=10')
        assert res.status_code == 200
        db_spy.assert_called()
        db_spy.assert_called_with('select * from events where lower(type) like %s order by date desc offset 0 limit 10', ('%%',))

@patch('event_service.main.db', testDB)
def test_search_events_by_type():
    with patch.object(testDB, 'execute', wraps=testDB.execute) as db_spy:        
        res = client.get(f'{EVENTS_URL}?search=TYPE')
        assert res.status_code == 200        
        db_spy.assert_called()
        db_spy.assert_called_with('select * from events where lower(type) like %s order by date desc offset 0 limit 7', ('%type%',))
