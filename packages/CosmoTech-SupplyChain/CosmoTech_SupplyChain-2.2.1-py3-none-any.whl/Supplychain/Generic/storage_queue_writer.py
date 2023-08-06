from azure.storage.queue import QueueClient, TextBase64EncodePolicy
import json
from Supplychain.Generic.timer import Timer


class QueueWriter(Timer):

    def send_items(self, items):
        total_messages = len(items)
        for item in items:
            message = json.dumps(item, separators=(',', ':'))
            self.queue_client.send_message(message)
        self.display_message(f"Sent {total_messages} message{'s' if total_messages > 1 else ''} to the queue.")

    def __init__(self, connect_string: str, queue_name: str):
        Timer.__init__(self, "[Storage Queue Writer]")
        self.queue_client = QueueClient.from_connection_string(connect_string,
                                                               queue_name=queue_name,
                                                               message_encode_policy=TextBase64EncodePolicy())
