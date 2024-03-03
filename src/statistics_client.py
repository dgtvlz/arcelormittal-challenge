import os
import json
import grpc
import sales_pb2
import sales_pb2_grpc
import logging
import google.protobuf.empty_pb2

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = sales_pb2_grpc.SalesServiceStub(channel)
        response = stub.GetSalesStatistics(google.protobuf.empty_pb2.Empty())
        print(response.message)

if __name__ == "__main__":
    logging.basicConfig()
    run()