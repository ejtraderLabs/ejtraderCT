
class Buffer:
    def __init__(self):
        self._buffer = bytearray()

    def write(self, data: bytes):
        self._buffer.extend(data)

    def read(self, size: int):
        data = self._buffer[:size]
        self._buffer[:size] = b""
        return data

    def peek(self, size: int):
        return self._buffer[:size]

    def count(self):
        return len(self._buffer)

    def __len__(self):
        return len(self._buffer)