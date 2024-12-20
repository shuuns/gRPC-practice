from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc
import datetime


class ExampleService(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        client_ip = context.peer()
        timestamp = datetime.datetime.now()
        print(f'[{timestamp}] Received request from {client_ip} by {request.name}')
        return example_pb2.HelloResponse(message=f'Hello, {request.name}!')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()