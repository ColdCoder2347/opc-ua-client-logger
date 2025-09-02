from server.opcua_server import OPCUAServer
from client.opcua_client import OPCUAClient
import multiprocessing
import time

def run_server(stop_event):
    server = OPCUAServer()
    server.start(stop_event)  # pass the stop_event to the server

def run_client():
    endpoint = "opc.tcp://localhost:4840/freeopcua/server/"
    client = OPCUAClient(endpoint)

    time.sleep(3)  # wait for server to start
    client.connect()

    try:
        for i in range(5):
            print(f"Client Read Temperature: {client.read_temperature()}")
            time.sleep(2)
    finally:
        client.disconnect()

if __name__ == "__main__":
    stop_event = multiprocessing.Event()  # event to signal server to stop

    server_process = multiprocessing.Process(target=run_server, args=(stop_event,))
    client_process = multiprocessing.Process(target=run_client)

    server_process.start()
    client_process.star_
