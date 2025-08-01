import socket
import struct
import json
import binascii
import threading
import time

class TCPClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.client_socket = None
        self.start_byte = 0xA5
        self.stop_byte = 0x5A
        self.last_received_data = None
        self.is_running = False
        self.lock = threading.Lock()

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
        except ConnectionRefusedError:
            print(f"Connection to {self.host}:{self.port} refused")
            return False
        return True

    def read_data(self):
        try:
            data = bytearray()
            while self.is_running:
                chunk = self.client_socket.recv(1024)
                if not chunk:
                    break
                data.extend(chunk)
                while True:
                    start_index = data.find(self.start_byte)
                    if start_index == -1:
                        break
                    if len(data) < start_index + 9:
                        break
                    length = struct.unpack('>I', data[start_index + 1:start_index + 5])[0]
                    if len(data) < start_index + 9 + length + 1:
                        break
                    stop_byte = data[start_index + 9 + length]
                    if stop_byte == self.stop_byte:
                        crc = struct.unpack('>I', data[start_index + 5:start_index + 9])[0]
                        actual_data = data[start_index + 9:start_index + 9 + length]
                        calculated_crc = binascii.crc32(actual_data) & 0xFFFFFFFF
                        if calculated_crc == crc:
                            data_dict = json.loads(actual_data.decode())
                            with self.lock:
                                self.last_received_data = data_dict
                        else:
                            print("CRC error")
                    else:
                        print("Invalid stop byte")
                    data = data[start_index + 9 + length + 1:]
        except ConnectionResetError:
            print("Connection to server lost")

    def start(self):
        if self.connect_to_server():
            self.is_running = True
            threading.Thread(target=self.read_data).start()

    def stop(self):
        self.is_running = False

    def get_last_received_data(self):
        with self.lock:
            return self.last_received_data

if __name__ == "__main__":
    client = TCPClient()
    client.start()

    try:
        while True:
            data = client.get_last_received_data()
            if data is not None:
                print(f"Received data: {data}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        client.stop()