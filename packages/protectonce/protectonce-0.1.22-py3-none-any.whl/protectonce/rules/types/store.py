class DataStore:
    def __init__(self) -> None:
        self.response_bytes = b''
    
    def store_response_body(self, response_bytes):
        self.response_bytes = b''.join([self.response_bytes, response_bytes])

_data_store = {}
 
def get_data_store(session_id):
    data_store = _data_store.get(session_id, None)
    if(data_store):
        return data_store
    _data_store[session_id] = DataStore()
    return _data_store[session_id]

def release_data_store(session_id):
    data_store = _data_store.get(session_id, None)
    if data_store:
        _data_store[session_id] = None