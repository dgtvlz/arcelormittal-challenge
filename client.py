import os
import json
import grpc
from grpc_compiled import sales_pb2
from grpc_compiled import sales_pb2_grpc
import logging
import sys

def run():
    """
    Sales client application.
    Reads JSON data from stdin, creates a gRPC channel to communicate with the Sales server.
    Sends a SalesMessage request containing the JSON data.
    """
    data = json.load(sys.stdin)
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
    run()