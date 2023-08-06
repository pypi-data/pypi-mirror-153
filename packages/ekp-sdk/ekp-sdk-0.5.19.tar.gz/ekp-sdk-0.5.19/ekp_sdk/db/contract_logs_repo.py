from ekp_sdk.db.mg_client import MgClient
from pymongo import DESCENDING, UpdateOne
import time


class ContractLogsRepo:
    def __init__(
            self,
            mg_client: MgClient
    ):
        self.mg_client = mg_client

        self.collection = self.mg_client.db['contract_logs']
        self.collection.create_index("transactionHash", unique=True)
        self.collection.create_index([("blockNumber", DESCENDING)])
        self.collection.create_index([("timeStamp", DESCENDING)])
        self.collection.create_index("address")

    def get_latest(self, address):
        return list(
            self.collection.find(
                {"address": address}
            )
            .sort("blockNumber", -1)
            .limit(1)
        )

    def find_since_block_number(
        self,
        block_number,
        limit,
        source_contract_address=None
    ):
        start = time.perf_counter()
        query = {"blockNumber": {"$gte": block_number}}

        if source_contract_address is not None:
            query["address"] = source_contract_address

        results = list(
            self.collection
            .find(query)
            .sort("blockNumber")
            .limit(limit)
        )

        print(
            f"⏱  [ContractLogsRepo.find_since_block_number({block_number})] {time.perf_counter() - start:0.3f}s"
        )

        return results

    def save(self, logs):
        start = time.perf_counter()

        self.collection.bulk_write(
            list(map(lambda log: UpdateOne(
                {"transactionHash": log["transactionHash"]}, {"$set": log}, True), logs))
        )

        print(
            f"⏱  [ContractLogsRepo.save({len(logs)})] {time.perf_counter() - start:0.3f}s"
        )
