from message_service.main import list_messages
from mock import patch
import mock
from datetime import date


class TestDB:
    def connect(self):
        return self
    def execute(self, sql, params):
        return []
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, tb):
        pass


testDB = TestDB()

@patch("message_service.main.db", testDB)
def test_list_companies_active():
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:        
        res = list_messages(0, 'room')
        assert res['offset'] == 0
        assert res['limit'] == 10
        assert res['size'] == 0
        db_spy.assert_called()
        db_spy.assert_called_with(''
        ' '.join(f"""select * from message where room = %s order by date asc offset %s limit %s""".split()), ('room', 0, 10))
