from opcua import Server, ua
import random
import datetime
import time

class OPCUAServer:
    def __init__(self, endpoint="opc.tcp://localhost:4840/freeopcua/server/"):
        self.server = Server()
        self.server.set_endpoint(endpoint)

        # Register namespace
        uri = "http://exactspace.local/opcua"
        self.idx = self.server.register_namespace(uri)

        # Create objects node
        self.objects = self.server.get_objects_node()
        self.tags = {}

    def setup_tags(self):
        """
        Create 10 dynamic tags under the 'ProcessData' object.
        """
        process_obj = self.objects.add_object(self.idx, "ProcessData")
        for i in range(1, 11):
            tag_name = f"Tag{i}"
            self.tags[tag_name] = process_obj.add_variable(
                self.idx, tag_name, 0.0, ua.VariantType.Double
            )
            self.tags[tag_name].set_writable()

    def start(self, stop_event=None):
        """
        Start the OPC UA server and continuously update tags until stop_event is set.
        """
        self.setup_tags()
        self.server.start()
        print(f"OPC UA Server started at {self.server.endpoint}")

        try:
            while stop_event is None or not stop_event.is_set():
                self.update_tags()
                time.sleep(1)
        finally:
            self.stop()

    def stop(self):
        """
        Stop the OPC UA server.
        """
        self.server.stop()
        print("OPC UA Server stopped.")

    def update_tags(self):
        """
        Update all tags with random values for simulation.
        """
        for i in range(1, 11):
            tag_name = f"Tag{i}"
            new_value = round(random.uniform(10, 100), 2)
            self.tags[tag_name].set_value(new_value)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Updated tags with new values.")
