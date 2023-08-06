from Supplychain.Generic.timer import Timer
import os
import uuid

from azure.identity import DefaultAzureCredential
from azure.digitaltwins.core import DigitalTwinsClient


class ADTWriter(Timer):

    def send_twin(self, twin: dict) -> dict:
        digital_twin_client = DigitalTwinsClient(os.environ["AZURE_DIGITAL_TWINS_URL"], self.azure_credentials)
        new_item = dict()
        for key in twin.keys():
            if type(twin[key]) is not dict or twin[key]:
                new_item[key] = twin[key]
        new_item.setdefault('$id', str(uuid.uuid1()))
        item_id = twin['$id'].replace(" ", "")
        return digital_twin_client.upsert_digital_twin(item_id,
                                                       new_item)

    def send_relation(self, relation: dict) -> dict:
        digital_twin_client = DigitalTwinsClient(os.environ["AZURE_DIGITAL_TWINS_URL"], self.azure_credentials)
        relation['$sourceId'] = relation['$sourceId'].replace(" ", "")
        relation['$targetId'] = relation['$targetId'].replace(" ", "")
        relation.setdefault('$relationshipId', str(uuid.uuid1()))
        relation['$relationshipId'] = relation['$relationshipId'].replace(" ", "")
        new_item = dict()
        for key in relation.keys():
            if type(relation[key]) is not dict or relation[key]:
                new_item[key] = relation[key]
        return digital_twin_client.upsert_relationship(relation['$sourceId'],
                                                       relation['$relationshipId'],
                                                       new_item)

    def send_items(self,
                   items: list):
        self.reset()
        for item in items:
            _ = self.send_twin(item) if '$sourceId' not in item else self.send_relation(item)
        self.display_message(f"Sent {len(items)} items in " + "{time_since_start:6.4f}s")

    def purge_adt(self, query: str = 'SELECT * FROM digitaltwins', delete_relation: bool = True):
        digital_twin_client = DigitalTwinsClient(os.environ["AZURE_DIGITAL_TWINS_URL"], self.azure_credentials)
        self.display_message("Querying twins")
        twin_list = []
        for item in digital_twin_client.query_twins(query):
            twin_id = str(item['$dtId'])
            twin_list.append(twin_id)
            current_length = len(twin_list)
            if current_length % 100 == 0:
                self.display_message(f"Found {current_length} twins")
        self.display_message(f"Found a total of {len(twin_list)} twins")
        if delete_relation:
            self.display_message("Deleting relationships")
            for twin_id in twin_list:
                for relation in digital_twin_client.list_relationships(twin_id):
                    relation_id = relation['$relationshipId']
                    digital_twin_client.delete_relationship(twin_id, relation_id)
        self.display_message("Deleting twins")
        for twin_id in twin_list:
            digital_twin_client.delete_digital_twin(twin_id)
        self.display_message("Purge complete")

    def __init__(self, force_purge: bool = False):
        Timer.__init__(self, "[ADT Writer]")
        self.azure_credentials = DefaultAzureCredential()
        if force_purge:
            self.display_message("Forcing purge of ADT")
            self.purge_adt()
