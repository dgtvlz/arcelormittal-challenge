import pytest
import grpc
from grpc_compiled import sales_pb2
from grpc_compiled import sales_pb2_grpc
from server import SalesService  # Import the SalesService class from server
from concurrent import futures

@pytest.fixture(scope="module")
def grpc_channel():
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    port = "[::]:50051"
    # Add the SalesService to the server
    sales_pb2_grpc.add_SalesServiceServicer_to_server(SalesService(), server)
    server.add_insecure_port(port)
    
    # Start server
    server.start()
    channel = grpc.insecure_channel(port)

    # Yield the channel to the test function
    yield channel

    # Stop server
    server.stop(0)

# Define a test function to test the sale processing
def test_process_sale(grpc_channel):
    stub = sales_pb2_grpc.SalesServiceStub(grpc_channel)
    # Call the ProcessSale RPC method with test data
    response = stub.ProcessSale(sales_pb2.SalesMessage(
        item="Test",
        quantity=10,
        price=50.0,
        date="2024-03-05T12:00:00Z"
    ))
    # Compare the response message with the expected output
    assert response.message == "Sale data: {'item': 'Test', 'quantity': 10, 'price': 50.0, 'date': '2024-03-05T12:00:00Z'}"
