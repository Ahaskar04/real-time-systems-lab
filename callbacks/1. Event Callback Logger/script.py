class Producer:
    def __init__(self):
        self._callbacks = []

    def register(self, callback):
        self._callbacks.append(callback)

    def emit_data_ready(self, data):
        for callback in self._callbacks:
            callback(data)

def log_plain(data):
        print(f"[LOG] {data}")

def log_upper(data):
    print(f"[LOUD LOG] {data.upper()}")

def count_chars(data):
        print(f"[COUNT] {len(data)} characters")

if __name__ == "__main__":
    producer = Producer()

    producer.register(log_plain)
    producer.register(log_upper)
    producer.register(count_chars)

    producer.emit_data_ready("callbacks are powerful")
