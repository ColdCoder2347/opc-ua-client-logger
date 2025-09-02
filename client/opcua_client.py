import time
import os
import csv
from datetime import datetime
from opcua import Client


class OPCUAClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.client = Client(self.endpoint)
        self.nodes = []

    def connect(self):
        print(f"[OPC Client] Connecting to {self.endpoint} ...")
        self.client.connect()
        print("[OPC Client] Connected successfully.")

        # Get 10 tags from server (assuming Tag1..Tag10 are under Objects)
        root = self.client.get_root_node()
        objects = root.get_child(["0:Objects"])
        for i in range(1, 11):
            node = objects.get_child([f"2:Tag{i}"])
            self.nodes.append(node)
        print(f"[OPC Client] Subscribed to {len(self.nodes)} tags.")

    def disconnect(self):
        self.client.disconnect()
        print("[OPC Client] Disconnected.")

    def get_log_filename(self):
        """Return filename based on current date and hour."""
        current_hour = datetime.now().strftime("%Y-%m-%d_%H")
        filename = f"OPC_Log_{current_hour}.csv"
        return filename

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
                # Collect timestamp
                now = datetime.now()
                timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
                epoch_time = int(time.time())

                # Collect tag values
                values = []
                for node in self.nodes:
                    val = node.get_value()
                    values.append(val)

                # Prepare row
                row = [timestamp_str, epoch_time] + values

                # Write to hourly log file
                filename = self.get_log_filename()
                self.ensure_log_file(filename)

                with open(filename, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(row)

                print(f"[LOG] {row}")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("[OPC Client] Logging stopped by user.")
        finally:
            self.disconnect()
