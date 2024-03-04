import os
import json
import grpc
from grpc_compiled import sales_pb2
from grpc_compiled import sales_pb2_grpc
import logging
import sys

def run(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        with grpc.insecure_channel('grpc-server:50051') as channel:
            stub = sales_pb2_grpc.SalesServiceStub(channel)
            response = stub.ProcessSale(sales_pb2.SalesMessage(
                item=data['item'],
                quantity=data['quantity'],
                price=data['price'],
                date=data['date']
                )
            )
            print("Sales client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    if len(sys.argv) != 2:
        print("Usage: python3 client.py <json_file_path>")
        sys.exit(1)
    json_file_path = sys.argv[1]
    run(json_file_path)