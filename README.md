# arcelormittal-challenge

## Overview

This repository contains a client and server gRPC application for managing sales data. The server communicates with the client via gRPC, and with an API provides statistics based on the sales data received.

## Requirements

- Docker
- Python
- Protocol Buffers compiler (protoc)

## Setup

1. Create a Docker network:

```bash
docker network create grpc-network
```

2. Build the server Docker image:

```bash
docker build -t arcelor-grpc-server -f ServerDockerfile .
```

3. Build the client Docker image:

```bash
docker build -t arcelor-grpc-client -f ClientDockerfile .
```

## Running the Server

Execute the following command to run the server:

```bash
docker run -d --name grpc-server --network grpc-network -p 50051:50051 -p 50052:50052 -v db:/app/db arcelor-grpc-server
```

The port 50051 correspond to the gRPC Server, and the port 50052 corresponds to the Flask API.

The server utilizes a JSON file `sales_data.json` in the `db` directory as its "database". By default, it is loaded with data from the `data` directory. To start with a fresh database, consider emptying this file before running the server.

## Running the Client

Run the client using the following command:

```bash
docker run --network grpc-network -i arcelor-grpc-client < /path/to/local/json/file.json
```

For example:

```bash
docker run --network grpc-network -i arcelor-grpc-client < data/2023/1/10/00261.json
```

The json file must have the following format:
```json
{"date": string datetime, "quantity": int, "item": string, "price": float}
```

Example:
```json
{"date": "2023-01-31T06:03:17+00:00", "quantity": 5, "item": "papaya", "price": 7.3}
```

## Calling the Statistics API

You can call the statistics API using curl:

```bash
curl http://localhost:50052/sales_statistics
```

## How It Works

- The client and server communicate via gRPC. Protocol Buffers scripts are compiled and can be found in `grpc_compiled`.
- The `sales.proto` file is compiled using the following command:

```bash
python3 -m grpc_tools.protoc -I../proto \
    --python_out=../grpc_compiled \
    --pyi_out=../grpc_compiled \
    --grpc_python_out=../grpc_compiled \
    ../proto/sales.proto
```

- After compilation, we manually adjust the import in `grpc_compiled/sales_pb2_grpc.py` to match the directory.
```python
import grpc_compiled.sales_pb2 as sales__pb2
```
- The client receives a JSON from stdin, connects to the server, and pushes the `SalesMessage`.
- The server receives the message from the client and saves it in `db/sales_data.json`.
- Additionally, the server exposes an API using Flask. The API reads `db/sales_data.json` and generates statistics based on the sales data.

The API response provides statistics in JSON format, including total quantities, averages per sale, total revenue, and monthly statistics for each product.

## Future Improvements

- Replace the `sales_data.json` file with a database solution like MongoDB to improve scalability and data management.
- Implement a GitHub Actions pipeline to automate Docker build and push to a Docker registry.