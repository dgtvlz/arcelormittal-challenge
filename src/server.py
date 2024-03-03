import os
import json
import grpc
import sales_pb2
import sales_pb2_grpc
import logging
from concurrent import futures
from collections import defaultdict
from datetime import datetime

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

    def GetSalesStatistics(self, request, context):
        global sales_data
        
        monthly_data = self.CalculateStatistics(sales_data)
        json_data = json.dumps(monthly_data, indent=4)

        return sales_pb2.ConfirmationReply(message=json_data)
        
    def CalculateStatistics(self, sales_data):
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
            statistics[item]['total_revenue'] += round((sale['quantity'] * sale['price']),2)
            statistics[item]['total_sales'] += 1
            
            # Monthly Statistics
            if month_key not in statistics[item]['monthly']:
                statistics[item]['monthly'][month_key] = {
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'total_sales': 0
                }
            
            statistics[item]['monthly'][month_key]['total_quantity'] += sale['quantity']
            statistics[item]['monthly'][month_key]['total_revenue'] += round((sale['quantity'] * sale['price']),2)
            statistics[item]['monthly'][month_key]['total_sales'] += 1

        # Calculating Avg per sale
        for item_data in statistics.values():
            if item_data['total_quantity'] > 0:
                item_data['average_per_sale'] = round((item_data['total_revenue'] / item_data['total_quantity']),2)
            else:
                item_data['average_per_sale'] = 0
            
            for month_data in item_data['monthly'].values():
                if month_data['total_quantity'] > 0:
                    month_data['average_per_sale'] = round((month_data['total_revenue'] / month_data['total_quantity']),2)
                else:
                    month_data['average_per_sale'] = 0
    
        # Removing total_sales keys
        for item_data in statistics.values():
            item_data.pop('total_sales', None)
            for month_data in item_data['monthly'].values():
                month_data.pop('total_sales', None)
        
        return statistics

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