import os
import json
import grpc
import sales_pb2
import sales_pb2_grpc
import logging
from concurrent import futures
from datetime import datetime
from flask import Flask, jsonify
import threading

app = Flask(__name__)

class SalesService(sales_pb2_grpc.SalesServiceServicer):
    def ProcessSale(self, request, context):      
        sale_data = {
            "item": request.item,
            "quantity": request.quantity,
            "price": request.price,
            "date": request.date
        }

        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db', 'sales_data.json'), 'a') as json_file:
            json.dump(sale_data, json_file)
            json_file.write('\n')

        print(f"Sale data {sale_data}")

        return sales_pb2.ConfirmationReply(
            message=f"Sale data: {sale_data}"
        )
        
    def GetStatistics(self):
        sales_data = []

        # Loading Sales Data
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db', 'sales_data.json'), 'r') as json_file:
            for line in json_file:
                sale_data = json.loads(line)
                sales_data.append(sale_data)

        statistics = {}    
        for sale in sales_data:
            date = datetime.strptime(sale['date'], '%Y-%m-%dT%H:%M:%S%z')
            month_key = f"{date.year}-{date.strftime('%m')}"
            item = sale['item']

            # Historic Statistics
            if item not in statistics:
                statistics[item] = {
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'total_sales': 0,
                    'monthly': {}
                }
            
            statistics[item]['total_quantity'] += sale['quantity']
            statistics[item]['total_revenue'] += sale['quantity'] * sale['price']
            statistics[item]['total_sales'] += 1
            
            # Monthly Statistics
            if month_key not in statistics[item]['monthly']:
                statistics[item]['monthly'][month_key] = {
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'total_sales': 0
                }
            
            statistics[item]['monthly'][month_key]['total_quantity'] += sale['quantity']
            statistics[item]['monthly'][month_key]['total_revenue'] += sale['quantity'] * sale['price']
            statistics[item]['monthly'][month_key]['total_sales'] += 1

        # Calculating Avg per sale
        for item_data in statistics.values():
            if item_data['total_sales'] > 0:
                item_data['average_per_sale'] = item_data['total_quantity'] / item_data['total_sales']
            else:
                item_data['average_per_sale'] = 0
            
            for month_data in item_data['monthly'].values():
                if month_data['total_sales'] > 0:
                    month_data['average_per_sale'] = month_data['total_quantity'] / month_data['total_sales']
                else:
                    month_data['average_per_sale'] = 0
    
        # Removing total_sales keys
        for item_data in statistics.values():
            item_data.pop('total_sales', None)
            for month_data in item_data['monthly'].values():
                month_data.pop('total_sales', None)
        
        return statistics

def serve_grpc():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sales_pb2_grpc.add_SalesServiceServicer_to_server(SalesService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

@app.route('/sales_statistics', methods=['GET'])
def get_sales_statistics():
    service = SalesService()
    statistics = service.GetStatistics()
    return jsonify(statistics)

if __name__ == "__main__":
    logging.basicConfig()
    grpc_server_thread = threading.Thread(target=serve_grpc)
    grpc_server_thread.start()
    app.run(debug=True, port=50052)