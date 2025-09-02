import os
import csv
import time
from datetime import datetime
from opcua import Client


class OPCUAClientLogger:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.client = Client(endpoint)
        self.nodes = []

        # For tracking hourly file
        self.current_hour = None
        self.current_file = None
        self.writer = None

    def connect(self):
        print(f"[OPC Client] Connecting to {self.endpoint} ...")
        self.client.connect()
        print("[OPC Client] Connected successfully.")

        # Subscribe to tags Tag1..Tag10 under Objects/ProcessData
        root = self.client.get_root_node()
        objects = root.get_child(["0:Objects", "2:ProcessData"])
        for i in range(1, 11):
            node = objects.get_child([f"2:Tag{i}"])
            self.nodes.append(node)
        print(f"[OPC Client] Subscribed to {len(self.nodes)} tags.")

    def disconnect(self):
        if self.current_file:
            self.current_file.close()
        self.client.disconnect()
        print("[OPC Client] Disconnected.")

    def get_log_filename(self):
        """Return filename based on current date and hour."""
        return f"OPC_Log_{datetime.now().strftime('%Y-%m-%d_%H')}.csv"

    def ensure_log_file(self, filename):
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(filename):
            with open(filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                header = ["Timestamp (24hr)", "Timestamp (Epoch UTC)"] + [f"Tag{i}" for i in range(1, 11)]
                writer.writerow(header)

    def log_data(self, interval=1):
        try:
            while True:
                # Check if new hour, create new file
                hour = datetime.now().strftime("%Y-%m-%d_%H")
                if hour != self.current_hour:
                    if self.current_file:
                        self.current_file.close()

                    self.current_hour = hour
                    filename = self.get_log_filename()
                    self.ensure_log_file(filename)
                    self.current_file = open(filename, mode="a", newline="")
                    self.writer = csv.writer(self.current_file)
                    print(f"[LOG] Logging to {filename}")

                # Collect timestamps
                now = datetime.now()
                timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
                epoch_time = int(time.time())

                # Read tag values
                values = []
                for node in self.nodes:
                    try:
                        val = node.get_value()
                    except Exception as e:
                        val = None
                        print(f"[WARN] Failed to read {node}: {e}")
                    values.append(val)

                # Write row
                row = [timestamp_str, epoch_time] + values
                self.writer.writerow(row)
                self.current_file.flush()

                print(f"[LOG] {row}")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("[OPC Client] Logging stopped by user.")
        finally:
            self.disconnect()


if __name__ == "__main__":
    endpoint = "opc.tcp://localhost:4840/freeopcua/server/"
    client_logger = OPCUAClientLogger(endpoint)
    client_logger.connect()
    client_logger.log_data(interval=1)  # log every 1 second
