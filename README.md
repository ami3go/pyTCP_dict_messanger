TCP messanger that allow to send and receive dictionary. 
This ways it is easy to exchange data between diffirent python programs. 

For example one program connectol one equipment, another program control another equipment but log function need to know when each change happens 

Application 1 -> send data to log appication

Application 2 -> send data to log application

log application capture every change in single timeline. 


***Freatures:***
- Start and stop bits
- CRC cehck for each package 


  
On server side, actually sending happens only when package updated, to reduce network trafic.  
On client side datat recieved in background in order not to block application. 
function ``` client.get_last_received_data() ``` return last retunred message. 
There is a flag ``` .data_updated ``` that sets when new package arrive and recent when you first read the data. 

***Server example:*** 
```python
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
```

***Client example:*** 
```python

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
```

***Result:***
```python
Connected to 127.0.0.1:12345
Received data: {'A1': 3, 'A2': 0, 'A4': 4, 'Stop': 0}
Received data: {'A1': 3, 'A2': 0, 'A4': 4, 'Stop': 0}
Received data: {'A1': 3, 'A2': 0, 'A4': 4, 'Stop': 0}
Received data: {'A1': 3, 'A2': 0, 'A4': 4, 'Stop': 0}
Received data: {'A1': 3, 'A2': 0, 'A4': 4, 'Stop': 0}
Received data: {'A1': 3, 'A2': 0, 'A4': 4, 'Stop': 0}
Received data: {'A1': 4, 'A2': 0, 'A4': 5, 'Stop': 0}
```
