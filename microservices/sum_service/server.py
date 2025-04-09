import grpc
from microservices import calculator_pb2
from microservices import calculator_pb2_grpc
from concurrent import futures


class SumService(calculator_pb2_grpc.CalculatorServicer):
    def Add(self, request, context):
        result = request.num1 + request.num2
        return calculator_pb2.OperationResponse(result=result)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(SumService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Sum Service running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
