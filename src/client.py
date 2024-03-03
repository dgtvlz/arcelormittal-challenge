import os
import json
import grpc
import sales_pb2
import sales_pb2_grpc
import logging

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sales_pb2_grpc.SalesServiceStub(channel)
        response = stub.ProcessSale(sales_pb2.SalesMessage(
            item='apple',
            quantity=7,
            price=5.2,
            date="2023-01-02T00:20:51+00:00"
            )
        )
        print("Sales client received: " + response.message)


if __name__ == "__main__":
    logging.basicConfig()
    run()