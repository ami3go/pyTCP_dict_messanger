from pyTCP_dict_messanger.client import TCPClient
import time
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