import os
import json
import grpc
import sales_pb2
import sales_pb2_grpc
import logging
from concurrent import futures

sales_data = []

class SalesService(sales_pb2_grpc.SalesServiceServicer):
    def ProcessSale(self, request, context):
        global sales_data
        sales_data.append({
            "item": request.item,
            "quantity": request.quantity,
            "price": request.price,
            "date": request.date
        })
        print(f"Sale: item {request.item}, quantity {request.quantity}, price {request.price}, date {request.date}")
        return sales_pb2.ConfirmationReply(
            message=f"Sale: item {request.item}, quantity {request.quantity}, price {request.price}, date {request.date}. Sales data: {sales_data}"
        )

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sales_pb2_grpc.add_SalesServiceServicer_to_server(SalesService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()