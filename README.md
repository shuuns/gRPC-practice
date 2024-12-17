1. 安裝必要的套件：
- 安裝 grpcio 和 grpcio-tools。

```shell
pip install grpcio grpcio-tools
```

2. 定義 .proto 文件：
- 建立一個 .proto 文件來定義服務和消息。

```
syntax = "proto3";

package example;

service ExampleService {
    rpc SayHello (HelloRequest) returns (HelloResponse);
}

message HelloRequest {
    string name = 1;
}

message HelloResponse {
    string message = 1;
}
```

3. 生成 Python 代碼：
- 使用 grpcio-tools 生成 Python 代碼。
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. example.proto
```

4. 實現服務端：
- 實現 gRPC 服務端代碼。
```
from concurrent import futures
import grpc
import example_pb2
import example_pb2_grpc

class ExampleService(example_pb2_grpc.ExampleServiceServicer):
    def SayHello(self, request, context):
        return example_pb2.HelloResponse(message=f'Hello, {request.name}!')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    example_pb2_grpc.add_ExampleServiceServicer_to_server(ExampleService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

5. 實現客戶端：
- 實現 gRPC 客戶端代碼。

```
import grpc
import example_pb2
import example_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = example_pb2_grpc.ExampleServiceStub(channel)
        response = stub.SayHello(example_pb2.HelloRequest(name='World'))
        print(f'Client received: {response.message}')

if __name__ == '__main__':
    run()
```

6. 運行服務端和客戶端：
- 先運行服務端，再運行客戶端來測試。

