from pyTCP_dict_messanger.server import TCPServer
import time
import threading
if __name__ == "__main__":
    server = TCPServer()
    thread = threading.Thread(target=server.start_server)
    thread.start()

    time.sleep(1)  # Wait for the server to start

    for i in range(100):
        data = {"A1":i, "A2":0, "A4":i+1,"Stop": 0}
        server.data_dict = data
        time.sleep(1)