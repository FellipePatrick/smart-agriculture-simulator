from collections import deque

messagens = deque(maxlen=100)

def add_message(topic, payload):
    from datetime import datetime
    messagens.append({
        'topic': topic,
        'payload': payload,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    

def get_messages():
    return list(messagens)
