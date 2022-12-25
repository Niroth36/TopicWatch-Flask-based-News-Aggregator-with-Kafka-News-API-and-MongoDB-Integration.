from kafka import KafkaProducer
from kafka.errors import KafkaError

topics = ['technology', 'business', 'politics', 'science', 'health', 'sports', 'entertainment', 'environment']

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Asynchronous by default
future = producer.send('my-topic', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout = 10)
except KafkaError:
    # Decide what to do if produce request failed
    # log.exception()
    pass

# Successful 