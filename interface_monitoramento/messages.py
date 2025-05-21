from collections import deque

messagens = deque(maxlen=20)

def add_message(topic, payload):
    from datetime import datetime
    messagens.append({
        'topic': topic,
        'payload': payload,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    

def get_messages():
    return list(messagens)

def post_message(topic, payload):
    from datetime import datetime
    messagens.append({
        'topic': topic,
        'payload': payload,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
