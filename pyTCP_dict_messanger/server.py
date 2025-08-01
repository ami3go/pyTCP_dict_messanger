import socket
import struct
import json
import binascii
import threading
import time

class TCPServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.host = host
        self.port = port
        self.server_socket = None
        self.start_byte = 0xA5
        self.stop_byte = 0x5A
        self.__data_dict_new = {}
        self.__data_dict_current = {}
        self.client_socket = None

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"TCP server listening on {self.host}:{self.port}")

        self.client_socket, address = self.server_socket.accept()
        print(f"Connection from {address} established")

        while True:
            try:
                if self.__data_dict_new != self.__data_dict_current:
                    data = self.pack_data(self.__data_dict_new)
                    self.client_socket.sendall(data)
                    self.__data_dict_current = self.__data_dict_new
            except ConnectionResetError:
                print(f"Connection lost")
                break
            # try:
            #
            #     data = self.pack_data(self.__data_dict_new)
            #     self.client_socket.sendall(data)
            # except ConnectionResetError:
            #     print(f"Connection lost")
            #     break

        self.client_socket.close()

    def pack_data(self, data_dict):
        data = json.dumps(data_dict).encode()
        crc = binascii.crc32(data) & 0xFFFFFFFF
        packed_data = struct.pack('>BII', self.start_byte, len(data), crc) + data + struct.pack('>B', self.stop_byte)
        return packed_data

    @property
    def data_dict(self):
        return self.__data_dict_new

    @data_dict.setter
    def data_dict(self, update_dict):
        self.__data_dict_new = update_dict

if __name__ == "__main__":
    server = TCPServer()
    thread = threading.Thread(target=server.start_server)
    thread.start()

    time.sleep(1)  # Wait for the server to start

    for i in range(100):
        data = {"A1":i, "A2":0, "A4":i+1,"Stop": 0}
        server.data_dict = data
        time.sleep(1)