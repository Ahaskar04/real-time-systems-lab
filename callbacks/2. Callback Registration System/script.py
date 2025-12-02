class Producer:
    def __init__(self):
        self._callbacks = []

    def register(self, callback):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def unregister(self, callback):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def emit_data_ready(self, data):
        # iterate over a snapshot to allow safe modification
        for callback in list(self._callbacks):
            callback(data)
def log_plain(data):
    print(f"[LOG] {data}")

def log_upper(data):
    print(f"[LOUD LOG] {data.upper()}")

def count_chars(data):
    print(f"[COUNT] {len(data)} characters")

if __name__ == "__main__":
    producer = Producer()

    # add plugins
    producer.register(log_plain)
    producer.register(log_upper)
    producer.register(count_chars)

    print("=== First emission ===")
    producer.emit_data_ready("callbacks are powerful")

    # remove one plugin dynamically
    producer.unregister(log_upper)

    print("\n=== Second emission (after removing log_upper) ===")
    producer.emit_data_ready("dynamic plugins")
